import copy
import json
import logging
import os
import time
from abc import abstractmethod

import h5py
import numpy as np
import pandas as pd
from f9columnar.processors import ProcessorsGraph

from f9ml.data_utils.feature_scaling import rescale_continuous_data, rescale_discrete_data
from f9ml.utils.helpers import load_dataset_variables


class DataProcessorsGraph(ProcessorsGraph):
    def __init__(self, copy_processors=False, prune_results=True, identifier=""):
        """Graph of data processors. Defined in F9Columnar.

        Note
        ----
        This class is a wrapper around `ProcessorsGraph` from `F9Columnar`. See docs from submodule for more info.

        """
        super().__init__(copy_processors, prune_results, identifier)


class DataProcessor:
    def __init__(self, name, copy_results=True):
        """Base class for data processors (nodes in a graph).

        Parameters
        ----------
        name : str
            Name of the processor.
        copy_results : bool, optional
            Will deep copy reurned dictionary results by a processor if True.

        Other parameters
        ----------------
        previous_processors : list of DataProcessor
            List of previous processors (looking from a current processor run) in a graph.
        delta_time : float
            Time it took to run a processor.
        _results : dict
            Results of a processor run that is passed to all next connected processors in a graph as kwargs.

        Warning
        -------
        If copy_results is True, it will deep copy all results of a previous processor. This can be slow for large data.
        If you are sure that you don't need to copy results, set copy_results to False. Unexpected behavior can occur if
        you don't copy results in the case of more complicated non-linear graphs.

        """
        self.name = name
        self.copy_results = copy_results

        self.previous_processors = None
        self.delta_time = None
        self._results = None

    @abstractmethod
    def run(self, *args, **kwargs):
        """Needs to be implemented by every processor object."""
        pass

    def _run(self, *args, **kwargs):
        """Internal run method."""
        start_time = time.time()

        if self.copy_results:
            args, kwargs = copy.deepcopy(args), copy.deepcopy(kwargs)
            self._results = self.run(*args, **kwargs)
        else:
            self._results = self.run(*args, **kwargs)

        self.delta_time = time.time() - start_time

        return self


class InputProcessor(DataProcessor):
    def __init__(self, data_dir, file_name, name="input", features=None, features_key="colnames", **kwargs):
        super().__init__(name, **kwargs)
        self.data_dir = data_dir
        self.file_path = os.path.join(data_dir, file_name)

        if features is None:
            features = load_dataset_variables(f"{os.getcwd()}/{data_dir}")[features_key]

        self.features = features

    def run(self):
        logging.debug(f"Input: {self.file_path} with {len(self.features)} features!")
        return {"file_path": self.file_path, "features": self.features}


class OutputProcessor(DataProcessor):
    def __init__(self, name="output", **kwargs):
        super().__init__(name, **kwargs)
        self.data = None
        self.selection, self.scalers = None, None

    def run(self, data, selection=None, scalers=None, **kwargs):
        logging.debug(f"Output data shape: {data.shape}!")
        self.data = data
        self.selection, self.scalers = selection, scalers
        return {"data": self.data, "selection": self.selection, "scalers": self.scalers}


class NpyLoaderProcessor(DataProcessor):
    def __init__(self, name="npy_loader", **kwargs):
        super().__init__(name, **kwargs)

    def run(self, file_path, **kwargs):
        logging.debug(f"Loading data from {file_path}!")
        return {"data": np.load(file_path)}


class HDF5LoaderProcessor(DataProcessor):
    def __init__(
        self,
        dataset_name,
        file_path=None,
        name="hdf5_loader",
        use_pd=False,
        use_disk=False,
        use_piles=False,
        shuffle=False,
        **kwargs,
    ):
        """Processor for loading data from HDF5 files.

        Parameters
        ----------
        dataset_name : str
            Name of the dataset in the HDF5 file. For example, `mc` or `data`.
        file_path : str, optional
            Path to the HDF5 file. If not given, it will be set in the run method.
        name : str, optional
            Name of the processor. Should generally not be changed.
        use_pd : bool, optional
            Use pandas (tables) to load data.
        use_disk : bool, optional
            Use disk to load data in chunks/piles.
        use_piles : bool, optional
            If True it will read piles from the hdf5 file.
        shuffle : bool, optional
            Shuffle data when loading from disk. Used only if use_disk is True. Has different implementations depending
            on the hdf5 file structure.
        """
        super().__init__(name, **kwargs)
        self.dataset_name = dataset_name
        self.file_path = file_path
        self.use_pd = use_pd
        self.use_disk = use_disk
        self.use_piles = use_piles
        self.shuffle = shuffle

        if self.use_piles:
            self.piles_lst = self.get_metadata(self.file_path)["piles"][self.dataset_name]

        self.chunk_size = None
        self.num_workers = None
        self.chunk_data = None

    def get_keys(self):
        """Get keys (subgroups/branches) from the hdf5 file."""
        with h5py.File(self.file_path, "r") as f:
            keys = list(f.keys())
        return keys

    def get_shape(self):
        """Get shape of the dataset in the hdf5 file."""
        with h5py.File(self.file_path, "r") as f:
            if self.use_piles:
                shape = [f[pile].shape for pile in self.piles_lst]
            else:
                shape = f[self.dataset_name].shape

        return shape

    def get_metadata(self, file_path):
        """Get metadata from the hdf5 file."""
        with h5py.File(file_path, "r") as f:
            metadata = json.loads(f["metadata"][()])
        return metadata

    def get_handle(self):
        """Get handle to the hdf5 file."""
        f = h5py.File(self.file_path, "r")
        return f

    def load_all(self, file_path):
        """Load all data from the hdf5 file into memory."""
        self.file_path = file_path

        logging.debug(f"Loading data from {self.file_path}!")

        if self.use_pd:
            data = pd.read_hdf(self.file_path).to_numpy()
        else:
            with h5py.File(self.file_path, "r") as f:
                data = f[self.dataset_name][()]

        return data

    def load_chunk(self):
        """Mostly internal method for loading data in chunks/piles from the hdf5 file."""
        return self.chunk_data

    def run(self, file_path=None, **kwargs):
        """Processor run method."""
        if not self.use_disk:
            return {"data": self.load_all(file_path)}
        else:
            return {"data": self.load_chunk()}


class FeatureSelectorProcessor(DataProcessor):
    def __init__(
        self,
        name="feature_selector",
        drop_types=None,
        drop_names=None,
        drop_labels=None,
        keep_names=None,
        **kwargs,
    ):
        """Base class for feature selection.

        Parameters
        ----------
        drop_types : list of str, optional
            Drop these column types (`label`, `disc`, `cont`, `uni`).
        drop_names : list of str, optional
            Drop these column names.
        drop_labels : list of bool, optional
            Drop these labels.
        keep_names : list of str, optional
            Keep these column names.

        Other parameters
        ----------------
        types : list of str
            Types of columns (`label`, `disc`, `cont`, `uni`).
        selection : pd.DataFrame
            Dataframe of column names and types with selection (True or False).

        Note
        ----
        type_lst = [df[df["type"] == t] for t in self.types]

        """
        super().__init__(name, **kwargs)
        self.drop_types, self.drop_names, self.drop_labels = drop_types, drop_names, drop_labels
        self.keep_names = keep_names

        self.types = ["label", "disc", "cont", "uni"]
        self.features, self.selection = None, None

    def _select_colnames(self) -> pd.DataFrame:
        """Selects column names to keep.

        Returns
        -------
        pd.DataFrame
            Dataframe of column names and types with selection.

        """
        if self.drop_types is None:
            self.drop_types = []
        if self.drop_names is None:
            self.drop_names = []
        if self.keep_names is None:
            self.keep_names = []

        df = pd.DataFrame(
            self.features.items(),
            index=range(len(self.features)),
            columns=["feature", "type"],
        )
        df["select"] = [True for _ in range(len(df))]

        df.loc[df["type"].isin(self.drop_types), "select"] = False
        df.loc[df["feature"].isin(self.drop_names), "select"] = False
        df.loc[df["feature"].isin(self.keep_names), "select"] = True

        return df

    def _select_features(self, data):
        """Selects features from data.

        Parameters
        ----------
        data : np.ndarray
            Data to select features from.

        Returns
        -------
        np.ndarray
            Data with selected features.
        """
        select_idx = self.selection[self.selection["select"] == True].index

        data = data[:, select_idx]

        logging.debug(f"Selected features! Data shape: {data.shape}.")

        if self.drop_labels is not None:
            labels_idx = self.selection[self.selection["type"] == "label"].index

            for label_idx in labels_idx:
                for drop_label in self.drop_labels:
                    mask_label = data[:, label_idx] == drop_label
                    data = data[~mask_label]
                    logging.debug(f"Dropped label {drop_label}! New data shape: {data.shape}.")

        return data

    def run(self, data, features, **kwargs):
        self.features = features

        self.selection = self._select_colnames()
        sel_data = self._select_features(data)

        return {"data": sel_data, "selection": self.selection}


class DataPreprocessProcessor(DataProcessor):
    def __init__(
        self,
        cont_rescale_type,
        name="preprocessor",
        disc_rescale_type=None,
        no_process=None,
        **kwargs,
    ):
        """General preprocessor for continious and discrete data in numpy arrays.

        Parameters
        ----------
        rescale_type (continuous or discrete) : str
            Rescale type, see `rescale_data` in `ml.common.data_utils.feature_scaling`.
        no_process : list of str, optional
            List of column types to not process (e.g. labels).
        """
        super().__init__(name, **kwargs)
        self.cont_rescale_type, self.disc_rescale_type = cont_rescale_type, disc_rescale_type
        self.no_process = no_process

        self.selection = None
        self.scalers = None

    def preprocess(self, data, selection, no_rescale=False, **kwargs):
        """Preprocess data.

        Parameters
        ----------
        data : np.ndarray
            Data to preprocess.
        selection : pd.DataFrame
            Dataframe of column names and types with selection.

        Returns
        -------
        tuple[np.ndarray, pd.DataFrame, dict]
            (data, selection, scalers)

        """
        if self.no_process is None:
            self.no_process = []

        # make selections where select is True (drop columns where select is False)
        # data is already selected to be disc or cont!
        selection = selection[selection["select"] == True].reset_index(drop=True)

        # make a mask for columns that are not processed and select both processed and not processed columns
        type_mask = selection["type"].isin(self.no_process)
        process_sel = selection[~type_mask]
        other_sel = selection[type_mask]

        # get discrete and continious selections of features (for index and name selection)
        self.disc_sel = process_sel[process_sel["type"] == "disc"]["feature"]
        self.cont_sel = process_sel[process_sel["type"].isin(["cont", "uni"])]["feature"]

        # check case if no discrete features and do disc normalization if discrete features exist
        if len(self.disc_sel) > 0:
            disc_x, disc_scaler, disc_names = self.fit_discrete(data, no_rescale)
        else:
            disc_x, disc_scaler, disc_names = None, None, []

        logging.debug(f"{self.disc_rescale_type} scaled disc_x: {disc_names}")

        # feature scaling for continious features, if they exist
        if len(self.cont_sel) > 0:
            cont_x, cont_scaler, cont_names = self.fit_continuous(data, no_rescale)
        else:
            cont_x, cont_scaler, cont_names = None, None, []

        logging.debug(f"{self.cont_rescale_type} scaled cont_x: {cont_names}")

        # select other features (e.g. labels)
        other_x = data[:, other_sel.index]
        other_names = list(other_sel["feature"].values)

        logging.debug(f"None scaled other_x: {other_names}")

        # concatenate given (preprocessed) features
        if disc_x is None:
            data = np.concatenate((cont_x, other_x), axis=1)
        elif cont_x is None:
            data = np.concatenate((disc_x, other_x), axis=1)
        else:
            data = np.concatenate((disc_x, cont_x, other_x), axis=1)

        # concatenate feature names with correct order and index
        colnames = disc_names + cont_names + other_names

        # make new selection dataframe
        new_selection = pd.DataFrame({k: [] for k in selection.columns})
        for i, colname in enumerate(colnames):
            new_selection.loc[i] = selection[selection["feature"] == colname].iloc[0].to_dict()

        # make scalers dictionary
        scalers = {"disc": disc_scaler, "cont": cont_scaler}

        self.selection = new_selection

        return data, new_selection, scalers

    def fit_discrete(self, data, no_rescale=False):
        """One hot encode discrete features.

        Returns
        -------
        tuple
            (x, onehot_scaler, all_feature_names)
            x is 2d array with columns: onehot encoded discrete features

        Examples
        --------
        Transform this into one hot encoding matrix with 0s and 1s.

        >>> disc_feature_names = {'LepM', 'LepQ', 'NJets'}
        >>> np.unique(x_disc[:, 0]), np.unique(x_disc[:, 1]), np.unique(x_disc[:, 2])
        (array([ 4.,  5.,  6.,  7.,  8.,  9., 10., 11., 12., 13., 14., 15., 16., 17.]), array([0., 1.]), array([-1.,  1.]))

        References
        ----------
        [1] - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html

        """

        disc_idx, disc_names = self.disc_sel.index, list(self.disc_sel.values)
        x_disc = data[:, disc_idx]

        if no_rescale:
            return x_disc, [("none", None)], disc_names

        x_disc_scaled, scaler = rescale_discrete_data(x_disc, self.disc_rescale_type)

        if self.disc_rescale_type == "onehot":
            # get onehot feature names
            onehot_feature_names = []
            for i, feat in enumerate(disc_names):
                n_classes = scaler.categories_[i].shape[0]
                for _ in range(n_classes):
                    onehot_feature_names.append(feat)

            disc_names = onehot_feature_names

        return x_disc_scaled, scaler, disc_names

    def fit_continuous(self, data, no_rescale=False):
        """Fits rescale type to (continious part of) data.

        Returns
        -------
        tuple of 2d array and scaler
            (x, scaler)
        """
        cont_idx, cont_names = self.cont_sel.index, list(self.cont_sel.values)
        x_cont = data[:, cont_idx]

        if no_rescale:
            return x_cont, [("none", None)], cont_names

        x_cont_scaled, scaler = rescale_continuous_data(x_cont, self.cont_rescale_type)
        return x_cont_scaled, scaler, cont_names

    def run(self, data, selection):
        logging.debug(f"Preprocessing data using cont. {self.cont_rescale_type} and disc. {self.disc_rescale_type}.")

        data, self.selection, self.scalers = self.preprocess(data, selection)

        return {"data": data, "selection": self.selection, "scalers": self.scalers}
