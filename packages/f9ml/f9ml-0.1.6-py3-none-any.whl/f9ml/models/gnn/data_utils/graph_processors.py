import copy
import logging
import re

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split

from f9ml.models.gnn.data_utils.graph_utils import graph_feynman_diagram
from f9ml.utils.data_utils.legacy_processors import FeatureSelector


class GraphFeatureSelector(FeatureSelector):
    def __init__(self, node_names, node_features, global_features=None, n_data=None, **kwargs):
        super().__init__(**kwargs)
        self.node_names = node_names
        self.node_features = node_features
        self.global_features = global_features
        self.n_data = n_data

    def load_data(self):
        return super().load_data()

    def _select_colnames(self):
        try:
            assert self.drop_types is None and self.drop_names is None
        except AssertionError:
            logging.warning(
                "GraphFeatureSelector received not None of drop_types or drop_names - node features might be wrong!"
            )
        return super()._select_colnames()

    def _node_selection(self):
        """Selects node names from variables selection df using regex."""
        for name, regex in self.node_names.items():
            f = lambda x: True if re.search(regex, x) else False
            sel = self.selection[self.selection["feature"].apply(f)]
            self.selection.loc[sel.index, "node"] = name

        if self.global_features is not None:
            sel = self.selection[self.selection["feature"].isin(self.global_features)]
            self.selection.loc[sel.index, "node"] = "global"

        return self.selection

    def _node_feature_selection(self):
        """Selects node features from variables selection df using regex."""
        self.selection["node_feature"] = np.nan

        for node_name, regex in self.node_features.items():
            f = lambda x: True if re.search(regex, x) else False
            sel = self.selection[self.selection["node"] != "global"]["feature"].apply(f)
            idx = sel[sel == True].index
            self.selection.loc[idx, "node_feature"] = node_name

        return self.selection

    def select_features(self, data):
        self._node_selection()
        self._node_feature_selection()

        # not select only features that have node set to something that's not nan
        self.selection.loc[self.selection["node"].isna(), "select"] = False
        # not select only features that have node_feature set to something that's not nan and are not global
        self.selection.loc[(self.selection["node_feature"].isna()) & (self.selection["node"] != "global"), "select"] = (
            False
        )
        # put back keep names
        self.selection.loc[self.selection["type"].isin(self.keep_names), "select"] = True

        logging.debug(f"Node selection with features:\n{self.selection[self.selection['select'] == True]}")

        select_idx = self.selection[self.selection["select"] == True].index

        # final selection for True only
        self.selection = self.selection[self.selection["select"] == True].reset_index(drop=True)

        data = data[:, select_idx]

        if self.n_data is not None:
            logging.info(f"Selecting only {self.n_data:.2e} data points!")
            data = data[: self.n_data, :]

        return data


class GraphBuilder:
    def __init__(
        self,
        edge_attributes,
        selection=None,
        graph_type="homogeneous",
        connection_type="all_to_all",
        connection_scheme=None,
        self_connection=False,
        cont_preprocessor=None,
        disc_preprocessor=None,
        to_torch=False,
    ):
        self.edge_attributes = edge_attributes
        self.selection = selection

        assert graph_type in ["homogeneous"], "Graph type not implemented!"
        self.graph_type = graph_type

        assert connection_type in ["all_to_all", "feynman"], "Connection type not implemented!"
        self.connection_type = connection_type
        if connection_type == "feynman":
            assert connection_scheme is not None, "Connection scheme not provided!"
        self.connection_scheme = connection_scheme

        self.self_connection = self_connection
        self.cont_preprocessor, self.disc_preprocessor = cont_preprocessor, disc_preprocessor
        self.to_torch = to_torch

        self.node_names, self.node_features = None, None
        self.scalers = {}

    def __call__(self, data, selection=None, *args, **kwargs):
        assert not (selection is None and self.selection is None), "selection is None!"

        if selection is not None:
            self.selection = selection

        graph_data = self.build_homogeneous_graph(data)

        return graph_data, self.selection, self.scalers

    @staticmethod
    def _get_sorted_features_index(target_lst, reference_lst):
        """Sort target_lst according to reference_lst.

        Dummy example
        -------------
        target_lst = ["a", "b", "c"]
        reference_lst = ["c", "a", "b"]
        sorted_index = [1, 2, 0]

        Jet3 node example for bbVV dataset
        ----------------------------------
        target_lst = ['Pt', 'Eta', 'Phi', 'JetM']
        reference_lst = ['E', 'Eta', 'JetM', 'LepM', 'LepM', 'LepQ', 'LepQ', 'Phi', 'Pt', 'Px', 'Py', 'Pz']
        sorted_index = [8, 1, 7, 2]

        Note for bbVV dataset
        ---------------------
        There are lots of zero columns in the node feature matrix. This is because the node feature matrix is created
        with the assumption that all nodes have the same features and this is not the case for many nodes. For example,
        the Jet3 node has only 4 (it does not have E, px, py, pz) features, while the Jet1 node has 8 features.

        Parameters
        ----------
        target_lst : list
            List of unsorted strings.
        reference_lst : list
            List of strings for target to be sorted against.

        Returns
        -------
        list
            Sorted indices of target_lst.
        """
        sorted_index = []
        checked_reference_lst = copy.deepcopy(reference_lst)

        for target in target_lst:
            ref_idx = checked_reference_lst.index(target)
            sorted_index.append(ref_idx)
            checked_reference_lst[ref_idx] = None

        return sorted_index

    def _get_node_feature_matrix(self, data):
        # select node that are not global and not nan (all the nodes that have a node string)
        nodes_sel = self.selection[~self.selection["node"].isin(["global", np.nan])]
        # get unique node names
        self.node_names = nodes_sel["node"].unique()  # assign node names

        # split into discrete and continuous node features
        disc_node_features = nodes_sel[nodes_sel["type"] == "disc"]["node_feature"].tolist()
        cont_node_features = nodes_sel[nodes_sel["type"] != "disc"]["node_feature"].unique().tolist()

        # unified and sorted node feature name list for x creation
        self.node_features = sorted(disc_node_features + cont_node_features)  # assign node features

        logging.debug(f"Node names: {self.node_names}, node features: {self.node_features}.")

        n_nodes, n_nodes_features = len(self.node_names), len(self.node_features)

        # create empty x node feature matrix
        x = np.zeros((len(data), n_nodes, n_nodes_features), dtype=np.float32)

        # fill x
        for i, node in enumerate(self.node_names):
            node_sel = nodes_sel[(nodes_sel["node"] == node)]  # indices of nodes in data
            feature_sel = node_sel.loc[node_sel.index, "node_feature"]  # node features of node

            sorted_idx = self._get_sorted_features_index(list(feature_sel.values), self.node_features)

            x[:, i, sorted_idx] = data[:, feature_sel.index]

        logging.info(f"Built node feature matrix: {x.shape} with {n_nodes} nodes and {n_nodes_features} features.")

        return x

    def _rescale_node_feature_matrix(self, x):
        """Per node feature rescaling."""

        for i, node_name in enumerate(self.node_names):
            node_sel = self.selection[self.selection["node"] == node_name]
            node_sel = node_sel.sort_values(by="node_feature").reset_index(drop=True)

            t, r = sorted(node_sel["node_feature"].to_list()), self.node_features
            idx = self._get_sorted_features_index(t, r)

            res, res_sel, scaler = self.cont_preprocessor(x[:, i, idx], node_sel)
            res_idx = res_sel.sort_values(by="node_feature").index

            x[:, i, idx] = res[:, res_idx]
            self.scalers[f"node_{node_name}"] = scaler

        return x

    def _get_edge_indices(self, x):
        """Edge indices for fully connected graph (with self loops)."""
        n_nodes = x.shape[1]

        if self.connection_type == "all_to_all":
            edge_indices = np.zeros((len(x), 2, n_nodes**2 if self.self_connection else n_nodes**2 - n_nodes))

            c = 0
            for i in range(n_nodes):
                for j in range(n_nodes):
                    if self.self_connection:
                        edge_indices[:, 0, c] = i
                        edge_indices[:, 1, c] = j
                        c += 1
                    else:
                        if i != j:
                            edge_indices[:, 0, c] = i
                            edge_indices[:, 1, c] = j
                            c += 1

        elif self.connection_type == "feynman":
            edge_idx = graph_feynman_diagram(self.node_names, self.connection_scheme)

            edge_indices = np.zeros((len(x), 2, edge_idx.shape[1]))

            edge_indices[:, 0, :] = edge_idx[0, :]
            edge_indices[:, 1, :] = edge_idx[1, :]

        logging.info(f"Built edge indices matrix: {edge_indices.shape}.")

        return edge_indices.astype(np.int64)

    @staticmethod
    def _wrap_lambda_for_x(lam, x):
        """Apply lambda to the last 3d tensor dimension. This might not be the most memory efficient way to do this."""
        return lam(*[x[:, :, i] for i in range(x.shape[2])])

    def _get_edge_attributes(self, x, edge_indices, rescale=False):
        logging.warning("Building edge attributes with an assumption of a fully connected graph...")

        # df for edge attributes
        insert_colnames = {k: v for (k, v) in zip(self.selection.columns, [np.nan for i in self.selection.columns])}
        insert_colnames["type"], insert_colnames["feature"], insert_colnames["node"] = "cont", "edge", "edge"
        insert_colnames["select"] = True
        sel = pd.DataFrame([insert_colnames for _ in range(edge_indices.shape[2])])

        # edge connection indices (all to all)
        node_i_idx, node_j_idx = edge_indices[0, 0, :], edge_indices[0, 1, :]

        edge_attrs = np.zeros((x.shape[0], edge_indices.shape[2], len(self.edge_attributes)), dtype=np.float32)

        for e, (attr_name, attr) in enumerate(self.edge_attributes.items()):
            logging.info(f"Making edge attribute: {attr_name}")

            lam_exp, features = attr[0], attr[1]
            lam_exp_inputs = np.zeros((len(x), edge_indices.shape[2], len(features)), dtype=np.float32)

            edge_attr_range = np.arange(0, len(features), 1)

            for f_i, f_j in zip(edge_attr_range[::2], edge_attr_range[1::2]):
                feature_i, feature_j = features[f_i], features[f_j]
                feature_i_idx = self.node_features.index(feature_i)
                feature_j_idx = self.node_features.index(feature_j)

                lam_exp_inputs[:, :, f_i] = x[:, node_i_idx, feature_i_idx]
                lam_exp_inputs[:, :, f_j] = x[:, node_j_idx, feature_j_idx]

            edge_attrs[:, :, e] = self._wrap_lambda_for_x(lam_exp, lam_exp_inputs)
            insert_colnames["feature"] = attr_name
            self.selection.loc[len(self.selection)] = insert_colnames

            # rescale edge attributes with cont. preprocessor
            if rescale:
                edge_attrs[:, :, e], _, edge_scaler = self.cont_preprocessor(edge_attrs[:, :, e], sel)
                self.scalers[f"edge_{attr_name}"] = edge_scaler

        return edge_attrs

    def build_homogeneous_graph(self, data):
        # get data annd rescale all discrete features

        data, self.selection, disc_scalers = self.disc_preprocessor(data, self.selection)
        self.scalers["disc"] = disc_scalers

        # select global features and rescale continuous features
        global_features_sel = self.selection[self.selection["node"] == "global"]
        global_features = data[:, global_features_sel.index]
        global_features, _, global_scaler = self.cont_preprocessor(global_features, global_features_sel)
        self.scalers["global"] = global_scaler

        # node features
        x = self._get_node_feature_matrix(data)

        # edge indices
        edge_indices = self._get_edge_indices(x)

        # edge attributes
        if self.edge_attributes is None:
            edge_attrs = None
        else:
            edge_attrs = self._get_edge_attributes(x, edge_indices)

        # rescale x continuous features
        self._rescale_node_feature_matrix(x)

        # get labels
        label_sel = self.selection[self.selection["type"] == "label"]
        y = data[:, label_sel.index]

        if self.to_torch:
            x = torch.from_numpy(x)
            y = torch.from_numpy(y)
            global_features = torch.from_numpy(global_features)
            edge_indices = torch.from_numpy(edge_indices)
            edge_attrs = edge_attrs if edge_attrs is None else torch.from_numpy(edge_attrs)

        if edge_attrs is not None:
            return {
                "x": x,
                "y": y,
                "global": global_features,
                "edge_indices": edge_indices,
                "edge_attributes": edge_attrs,
            }
        else:
            return {
                "x": x,
                "y": y,
                "global": global_features,
                "edge_indices": edge_indices,
            }

    def build_heterogeneous_graph(self, data):
        raise NotImplementedError


class GraphTrainValTestSplitter:
    def __init__(self, train_split=0.7, val_split=0.5):
        self.train_split = train_split
        self.val_split = val_split
        self.splits = ["train", "val", "test"]
        self.split_idx = None

    def get_splits(self, n):
        idx = torch.arange(n)
        remaining, train_idx = train_test_split(idx, test_size=self.train_split)
        test_idx, val_idx = train_test_split(idx[remaining], test_size=self.val_split)
        logging.debug(f"\ntest splits: {test_idx[:5]},\nval splits: {val_idx[:5]},\ntrain splits: {train_idx[:5]}\n")
        return train_idx, val_idx, test_idx

    def __call__(self, graph_data, selection, scalers):
        n = graph_data["x"].shape[0]

        if self.split_idx is None:
            self.split_idx = self.get_splits(n)
        else:
            logging.info("Using already split indices.")

        split_graph_data = {}
        for split, split_idx in zip(self.splits, self.split_idx):
            logging.info(f"Splitting graph data for {split} split of len {len(split_idx)}.")

            split_graph_data[split] = {}
            for k, v in graph_data.items():
                if v is not None:
                    split_graph_data[split][k] = v[split_idx]
                else:
                    logging.critical(f"Graph data {k} is None!")

        return split_graph_data, selection, scalers


if __name__ == "__main__":
    from f9ml.custom.bbVV.process_bbVV_dataset import bbVVNpyProcessor
    from f9ml.models.gnn.data_utils.graph_utils import digraph_to_nx
    from f9ml.utils.data_utils.legacy_processors import Preprocessor, ProcessorChainer
    from f9ml.utils.helpers import set_df_print
    from f9ml.utils.loggers import setup_logger

    set_df_print()

    setup_logger()

    npy_proc = bbVVNpyProcessor(
        "ml/data/hhbbvv/",
        base_file_name="hhbbvv_data",
        keep_ratio=1.0,
        shuffle=True,
    )

    # all mass points
    mx = [0.0, 350.0, 500.0, 750.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0]
    ms = [0.0, 170.0, 240.0, 400.0, 550.0, 750.0, 1000.0, 1500.0, 2000.0, 2500.0]

    # all mass regions
    mr = ["SH0", "SH1", "SH2", "SH3", "SH4", "SH5"]

    node_names = {
        "Jet1": r"^Jet1",
        "Jet2": r"^Jet2",
        "BJet1": r"^BJet1",
        "BJet2": r"^BJet2",
        "Neu": r"^(MET|METPhi)$",  # MET or METPhi
        "Lep": r"^Lep(M|Pt|Phi|Eta)",  # does not start with LepBJet, LepNeu, LepJetDR and contains Lep
        "LepNeu": r"^LepNeu(DPhi|M|Phi)$",  # starts with LepNeu and contains DPhi, M, Phi after it at the end
        "diJet": r"^diJet",
        "WW": r"^WW(?!MT)",  # does not contain MT after WW
        "diHiggs": r"^diHiggs(?!MT)",
        "BB": r"^BB(M|Pt|Phi|Eta|DR|DEta|DPhi)",
    }

    node_features = {
        "Pt": r"(Pt$)|(MET$)",
        "Eta": r"Eta$",
        "Phi": r"Phi$",
        "M": r"^(?!LepM).*M$",
        "DR": r"DR$",
        "DEta": r"DEta$",
        "DPhi": r"DPhi$",
    }

    # connection_scheme = {
    #     "diHiggs": ["BB", "WW"],
    #     "BB": ["BJet1", "BJet2"],
    #     "WW": ["diJet", "LepNeu"],
    #     "diJet": ["Jet1", "Jet2"],
    #     "LepNeu": ["Neu", "Lep"],
    # }

    connection_scheme = {
        "BJet1": ["BB"],
        "BJet2": ["BB"],
        "BB": ["diHiggs"],
        "Jet1": ["diJet"],
        "Jet2": ["diJet"],
        "diJet": ["WW"],
        "WW": ["diHiggs"],
        "Lep": ["LepNeu"],
        "Neu": ["LepNeu"],
        "LepNeu": ["WW"],
    }

    edge_attrs = None

    global_features = [
        "NJets",
        "Higgsness",
        "Topness",
        "loglttbar",
        "logldihiggs",
        "METBJetDPhi_min",
        "METBJetDPhi_max",
        "LepBJetDRmin",
        "LepBJetDRmax",
        "LepJetDRmin",
        "LepJetDRmax",
    ]

    f_sel = GraphFeatureSelector(
        node_names=node_names,
        node_features=node_features,
        global_features=global_features,
        keep_names=["label", "mass_region", "mass_point"],
        n_data=10**5,
    )

    disc_pre = Preprocessor(
        cont_rescale_type=None,
        disc_rescale_type="onehot",
        no_process=["mass_region", "mass_point", "label", "cont", "uni"],
    )

    cont_pre = Preprocessor(
        cont_rescale_type="logit_normal",
        disc_rescale_type=None,
        no_process=["mass_region", "mass_point", "label", "disc"],
    )

    g_build = GraphBuilder(
        graph_type="homogeneous",
        self_connection=False,
        connection_type="feynman",
        connection_scheme=connection_scheme,
        edge_attributes=edge_attrs,
        cont_preprocessor=cont_pre,
        disc_preprocessor=disc_pre,
    )

    g_split = GraphTrainValTestSplitter(train_split=0.7, val_split=0.5)

    chainer = ProcessorChainer(npy_proc, f_sel, g_build, g_split)
    graph_data, selection, scalers = chainer()

    digraph_to_nx(graph_data["train"]["x"], graph_data["train"]["edge_indices"], g_build, draw=True)

    print("\nSELECTION:\n", selection)
    print(f"\nLABELS:\n{selection[selection['type'] == 'label']}")

    print("\nGRAPH TRAIN INFO:")
    for k, v in graph_data["train"].items():
        print(k, v.shape)
