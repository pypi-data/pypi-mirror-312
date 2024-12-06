import functools
import glob
import logging
import os

import torch
from torch_geometric.data import Data, Dataset, InMemoryDataset
from tqdm import tqdm

from f9ml.utils.helpers import pickle_load, pickle_save


class GraphDataset(Dataset):
    def __init__(
        self,
        root,
        graph_file_name,
        processor=None,
        stage=None,
        **kwargs,
    ):
        """Dataset class for graph datasets which do not fit into memory.

        Note
        ----
        The dataset is processed and saved to the self.processed_dir folder (root + /processed). Every graph is saved as a .pt file.
        Processing is skipped if the files are already present in the self.processed_dir directory.

        Warning
        -------
        The dataset is not loaded into memory. Instead, it is loaded on the fly when needed. This is done by the get() method.
        The drawback is that the graph files take up a lot of space on the disk. The advantage is that the dataset can be very large.

        Warning
        -------
        If the selection is changed in any way (e.g. by changing the features or chaning edges/nodes), the dataset must
        be reprocessed and saved again. Otherwise, the selection will not be applied. This is done most simply by
        deleting the processed files in the self.processed_dir folder.

        Parameters
        ----------
        root : str
            Root directory where the dataset should be saved.
        graph_file_name : str
            Name of the graph files in processed_dir.
        processor : object
            Processor object which contains the methods to process the dataset (e.g. ProcessorChainer).
        stage : str, optional
            Stage of the data to use (e.g. "train", "val", "test"), by default None.

        References
        ----------
        [1] - Creating Graph Datasets: https://pytorch-geometric.readthedocs.io/en/latest/notes/create_dataset.html
        [2] - torch_geometric.data: https://pytorch-geometric.readthedocs.io/en/latest/modules/data.html#torch-geometric-data
        [3] - Example: https://github.com/deepfindr/gnn-project/blob/main/dataset.py

        """
        self.graph_file_name = graph_file_name
        self.processor = processor
        self.stage = stage if stage is not None else "all"
        super().__init__(root, **kwargs)

    def _get_files_from_dir(self, file_dir, ext="pt"):
        """Returns a list of files in the given directory with the given file extension."""
        files = [os.path.basename(f) for f in glob.glob(f"{file_dir}/*_{self.stage}.{ext}")]
        return files

    @property
    def processed_file_names(self):
        """The name of the files (processed_paths) in the self.processed_dir folder that must be present in order to skip processing."""
        processed_files = self._get_files_from_dir(self.processed_dir)
        logging.info(f"Found {len(processed_files)} {self.stage} processed .pt files in {self.processed_dir}")
        return processed_files

    def process(self):
        """Processes the dataset to the self.processed_dir folder."""
        # run processor chainer to get graph data
        graph_data, selection, scalers = self.processor()

        # save selection and scalers
        pickle_save(self.processed_dir, "/selection.p", selection)
        pickle_save(self.processed_dir, "/scalers.p", scalers)

        # check if graph data was split into train/val/test
        # if it was not split, then the graph_data is a dictionary with one key: "all"
        # assume this was done for keys in ["train", "val", "test"] by some spliter processor
        stages = list(graph_data.keys())
        if not any([i in list(graph_data.keys()) for i in ["train", "val", "test"]]):
            stages = ["all"]
            graph_data = {"all": graph_data}

        # loop over stages and make a Data object for each graph in this stage and save it to the processed_dir
        for stage in stages:
            # required
            x = graph_data[stage].get("x")
            edge_indices = graph_data[stage].get("edge_indices")
            edge_attributes = graph_data[stage].get("edge_attributes")

            # optional
            y = graph_data[stage].get("y", None)
            global_x = graph_data[stage].get("global", None)

            logging.info(f"Saving {len(x)} {stage} graphs to {self.processed_dir}")

            pickle_save(self.processed_dir, f"/{stage}_feature_matrix_shape.p", x.shape)

            for idx in tqdm(range(len(x)), desc=f"Saving {stage} graphs"):
                data = Data(
                    x=x[idx],
                    edge_index=edge_indices[idx],
                    edge_attr=edge_attributes[idx] if edge_attributes is not None else None,
                )

                if y is not None:
                    data.y = y[idx][None, :]
                if global_x is not None:
                    data.global_x = global_x[idx][None, :]

                torch.save(data, os.path.join(self.processed_dir, f"{self.graph_file_name}_{idx}_{stage}.pt"))

    @functools.lru_cache()
    def len(self):
        x = pickle_load(self.processed_dir, f"/{self.stage}_feature_matrix_shape.p")
        return x[0]

    def get(self, idx):
        data = torch.load(os.path.join(self.processed_dir, f"{self.graph_file_name}_{idx}_{self.stage}.pt"))
        return data.apply(lambda arr: torch.from_numpy(arr))


class GraphInMemoryDataset(InMemoryDataset):
    def __init__(self, graph_data, stage=None, make_data_lst=False, **kwargs):
        """Dataset class for graph datasets which fit into memory.

        Parameters
        ----------
        graph_data : dict
            Dictionary of graph data. Must contain keys "x", "edge_indices", and "edge_attributes". If it is split
            into train/val/test, then it must contain keys "train", "val", and "test" that again have the same dicts as values.
        stage : str, optional
            Current stage of this dataset, by default None
        make_data_lst : bool, optional
            Whether to make a list of data objects for each graph in the dataset, by default False.
        """
        self.graph_data = graph_data
        self.stage = stage
        self.make_data_lst = make_data_lst
        super().__init__(root="", **kwargs)

    @property
    def raw_file_names(self):
        return []

    @property
    def processed_file_names(self):
        return []

    def process(self):
        """Process graph data and keep in it in memory. Does not use collate functionality of pytorch geometric."""

        if self.stage is not None:
            graph_data = self.graph_data[self.stage]

        # required
        self.x = torch.from_numpy(graph_data.get("x"))
        self.edge_indices = torch.from_numpy(graph_data.get("edge_indices"))
        self.edge_attributes = graph_data.get("edge_attributes")

        if self.edge_attributes is not None:
            self.edge_attributes = torch.from_numpy(self.edge_attributes)

        # optional
        self.y = graph_data.get("y", None)
        self.global_x = graph_data.get("global", None)

        # unpacked all graph data, so delete it
        del self.graph_data

        if self.y is not None:
            self.y = torch.from_numpy(self.y)
        if self.global_x is not None:
            self.global_x = torch.from_numpy(self.global_x)

        logging.info(f"Loaded {len(self.x)} {self.stage} graphs into memory.")

        # if True, make a list of Data objects, else just make them on the fly in get()
        if self.make_data_lst:
            logging.info(f"Making a list of Data objects for {self.stage} graphs.")
            self.data_lst = []
            for idx in tqdm(range(len(self.x))):
                data = Data(
                    x=self.x[idx],
                    edge_index=self.edge_indices[idx],
                    edge_attr=self.edge_attributes[idx] if self.edge_attributes is not None else None,
                )

                if self.y is not None:
                    data.y = self.y[idx][None, :]
                if self.global_x is not None:
                    data.global_x = self.global_x[idx][None, :]

                self.data_lst.append(data)

            self.x = None
            self.edge_indices = None
            self.edge_attributes = None
            self.y = None
            self.global_x = None

    def len(self):
        if self.make_data_lst:
            return len(self.data_lst)
        else:
            return len(self.x)

    def get(self, idx):
        if self.make_data_lst:
            return self.data_lst[idx]
        else:
            data = Data(
                x=self.x[idx],
                edge_index=self.edge_indices[idx],
                edge_attr=self.edge_attributes[idx] if self.edge_attributes is not None else None,
            )
            data.y = self.y[idx][None, :]
            data.global_x = self.global_x[idx][None, :]

            return data
