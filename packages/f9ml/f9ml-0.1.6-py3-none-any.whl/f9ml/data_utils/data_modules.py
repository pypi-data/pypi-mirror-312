import logging
import multiprocessing

import lightning as L
import numpy as np
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from tqdm import tqdm

from f9ml.data_utils.datasets import HDF5IterableSplitDataset, NpDataset


def get_splits(n_data, train_split, val_split, shuffle=True):
    """Utility function for splitting data using [`sklearn.model_selection.train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html).

    Parameters
    ----------
    n_data : int
        Number of data points.
    train_split : float
        Percentage (in range 0.0 to 1.0) of data for training.
    val_split : float or None
        Percentage (in range 0.0 to 1.0) of data for validation.
    shuffle : bool, optional
        Shuffle data before splitting.

    Note
    ----
    If `val_split=None`, no test data is returned. If `train_split=1.0`, returns only shuffled training data.

    Warning
    -------
    For large datasets, this function can be slow due to shuffling. It can also use a lot of memory for large datasets
    to store random indices.

    Returns
    -------
    tuple
        Tuple with random indices for training, validation and test data.
    """
    idx = np.arange(n_data)

    if train_split == 1.0:
        if shuffle:
            np.random.shuffle(idx)
        return idx, [], []

    remaining, train_idx = train_test_split(idx, test_size=train_split, shuffle=shuffle)

    if val_split is None:
        return train_idx, remaining, []
    else:
        test_idx, val_idx = train_test_split(idx[remaining], test_size=val_split, shuffle=shuffle)

    logging.debug(f"Created splits with sizes: {len(train_idx)}, {len(val_idx)}, {len(test_idx)}")
    return train_idx, val_idx, test_idx


class BaseDataModule(L.LightningDataModule):
    def __init__(
        self,
        processors_graph,
        train_split=0.7,
        val_split=None,
        save_scalers=False,
        get_labels=False,
        **dataloader_kwargs,
    ):
        """Base class for data modules.

        Parameters
        ----------
        processors_graph : DataProcessorsGraph
            Processors graph with fit() method. Should have output processor as a node at the end.
        train_split : float, optional
            Train split, by default 0.7.
        val_split : float, optional
            Validation split, by default 0.5. If None is passed, no test split is done.
        save_scalers : bool, optional
            Save scalers for data preprocessors.
        get_labels : bool, optional
            Get labels (X and y) from the DataLoader.
        dataloader_kwargs : dict, optional
            Kwargs for torch.utils.data.DataLoader. If `num_workers=-1` will use all available workers.

        Other parameters
        ----------------
        selection : pd.DataFrame
            Selection of data.
        scalers : dict
            Scalers for data preprocessors.
        train_idx : np.ndarray
            Random indices for training data.
        val_idx : np.ndarray
            Random indices for validation data.
        test_idx : np.ndarray
            Random indices for test data.
        train : torch.utils.data.Dataset
            Torch training dataset.
        val : torch.utils.data.Dataset
            Torch validation dataset.
        test : torch.utils.data.Dataset
            Torch test dataset.
        _is_split : bool
            Flag for checking if data is already split to test/val/test.

        """
        super().__init__()

        self.processors_graph = processors_graph
        self.train_split, self.val_split = train_split, val_split
        self.save_scalers = save_scalers
        self.get_labels = get_labels
        self.dataloader_kwargs = dataloader_kwargs

        self.selection, self.scalers = None, None

        self.train_idx, self.val_idx, self.test_idx = None, None, None
        self.train, self.val, self.test = None, None, None
        self._is_split = False

        if self.dataloader_kwargs.get("num_workers") == -1:
            self.dataloader_kwargs["num_workers"] = multiprocessing.cpu_count()

    def prepare_data(self):
        """Lightning internal method to skip."""
        return None

    def teardown(self, stage=None):
        """Teardown method for data module."""
        if stage == "fit" or stage is None:
            self.train, self.val = None, None

        if stage == "test":
            self.test = None

        self.stage = stage

    def train_dataloader(self):
        """Train dataloader setup."""
        return DataLoader(self.train, shuffle=True, **self.dataloader_kwargs)

    def val_dataloader(self):
        """Validation dataloader setup."""
        return DataLoader(self.val, shuffle=False, **self.dataloader_kwargs)

    def test_dataloader(self):
        """Test dataloader setup."""
        return DataLoader(self.test, shuffle=False, **self.dataloader_kwargs)


class MemoryDataModule(BaseDataModule):
    def __init__(self, *args, **kwargs):
        """Memory data module for in-memory data.

        Parameters
        ----------
        *args : tuple
            Arguments for BaseDataModule.
        **kwargs : dict
            Keyword arguments for BaseDataModule.
        """
        super().__init__(*args, **kwargs)

    def setup(self, stage=None):
        """Setup method for data module.

        Parameters
        ----------
        stage : str or None, optional
            Stage of the setup by lightning.
        """
        processors = self.processors_graph.fit()

        self.selection = processors["output"].selection
        self.scalers = processors["output"].scalers

        if not self._is_split:
            self.train_idx, self.val_idx, self.test_idx = get_splits(
                len(processors["output"].data), self.train_split, self.val_split
            )
        else:
            self._is_split = True

        if stage == "fit" or stage is None:
            self.train = NpDataset(
                processors,
                self.train_idx,
                save_scalers=self.save_scalers,
                get_labels=self.get_labels,
            )
            self.val = NpDataset(
                processors,
                self.val_idx,
                save_scalers=self.save_scalers,
                get_labels=self.get_labels,
            )

        if stage == "test":
            self.test = NpDataset(
                processors,
                self.test_idx,
                save_scalers=self.save_scalers,
                get_labels=self.get_labels,
            )


class DiskDataModule(BaseDataModule):
    def __init__(
        self,
        *args,
        return_graph=False,
        train_num_workers,
        val_num_workers=None,
        test_num_workers=None,
        **kwargs,
    ):
        """Disk data module for data stored on disk.

        Parameters
        ----------
        return_graph : bool, optional
            Return processors graph.
        train_num_workers : int
            Number of workers for training data.
        val_num_workers : int or None, optional
            Number of workers for validation data. If None, uses `train_num_workers`.
        test_num_workers : int or None, optional
            Number of workers for test data. If None, uses `train_num_workers`.

        Note
        ----
        Chunk size is internally set to batch size in HDF5Dataset and should not be set in DataLoader.

        """
        super().__init__(*args, **kwargs)
        self.return_graph = return_graph

        self.num_workers, self.use_piles, self.shuffle, self.drop_last = None, None, None, None

        self.hdf_loader = self.processors_graph.processors["hdf5_loader"]

        self._num_workers_setup(train_num_workers, val_num_workers, test_num_workers)
        self._hdf5_loader_setup()

        self.piles_splits_dct = None

        if self.use_piles:
            self._setup_pile_splits()

    def _num_workers_setup(self, train_num_workers, val_num_workers, test_num_workers):
        """Setup number of workers for dataloaders."""

        if val_num_workers is None:
            val_num_workers = train_num_workers
        if test_num_workers is None:
            test_num_workers = train_num_workers

        self.num_workers = [train_num_workers, val_num_workers, test_num_workers]
        self.num_workers = [multiprocessing.cpu_count() if i == -1 else i for i in self.num_workers]
        self.dataloader_kwargs.pop("num_workers", None)

    def _hdf5_loader_setup(self):
        """Setup HDF5 loader processor for disk data."""

        self.hdf_loader.file_path = self.processors_graph.processors["input"].file_path

        batch_size = self.dataloader_kwargs.pop("batch_size", None)
        assert batch_size is not None, "Batch size must be provided for disk data module."

        self.hdf_loader.chunk_size = batch_size

        self.use_piles = self.hdf_loader.use_piles
        self.shuffle = self.hdf_loader.shuffle
        self.drop_last = self.dataloader_kwargs.pop("drop_last", False)

    def _setup_pile_splits(self):
        piles_lst = self.hdf_loader.piles_lst
        piles_shapes = self.hdf_loader.get_shape()

        self.piles_splits_dct = {"train_idx": {}, "val_idx": {}, "test_idx": {}}

        for pile_name, pile_shape in tqdm(zip(piles_lst, piles_shapes), total=len(piles_lst), desc="Splitting piles"):
            train_idx, val_idx, test_idx = get_splits(
                pile_shape[0],
                self.train_split,
                self.val_split,
                shuffle=self.shuffle,
            )
            self.piles_splits_dct["train_idx"][pile_name] = train_idx
            self.piles_splits_dct["val_idx"][pile_name] = val_idx
            self.piles_splits_dct["test_idx"][pile_name] = test_idx

    def setup(self, stage=None):
        """Setup method for data module.

        Parameters
        ----------
        stage : str or None, optional
            Stage of the setup by lightning.
        """

        if not self.use_piles and not self._is_split:
            self.train_idx, self.val_idx, self.test_idx = get_splits(
                self.hdf_loader.get_shape()[0],
                self.train_split,
                self.val_split,
                shuffle=self.shuffle,
            )
        else:
            self._is_split = True

        ds_kwargs = {
            "save_scalers": self.save_scalers,
            "get_labels": self.get_labels,
            "return_graph": self.return_graph,
            "drop_last": self.drop_last,
        }

        if stage == "fit" or stage is None:
            self.train = HDF5IterableSplitDataset(
                self.processors_graph,
                split_idx=self.train_idx if not self.use_piles else self.piles_splits_dct["train_idx"],
                **ds_kwargs,
            )
            self.val = HDF5IterableSplitDataset(
                self.processors_graph,
                split_idx=self.val_idx if not self.use_piles else self.piles_splits_dct["val_idx"],
                **ds_kwargs,
            )

        if stage == "test":
            self.test = HDF5IterableSplitDataset(
                self.processors_graph,
                split_idx=self.test_idx if not self.use_piles else self.piles_splits_dct["test_idx"],
                **ds_kwargs,
            )

    def train_dataloader(self):
        """Train dataloader setup."""
        return DataLoader(
            self.train, num_workers=self.num_workers[0], batch_size=None, drop_last=False, **self.dataloader_kwargs
        )

    def val_dataloader(self):
        """Validation dataloader setup."""
        return DataLoader(
            self.val, num_workers=self.num_workers[1], batch_size=None, drop_last=False, **self.dataloader_kwargs
        )

    def test_dataloader(self):
        """Test dataloader setup."""
        return DataLoader(
            self.test, num_workers=self.num_workers[2], batch_size=None, drop_last=False, **self.dataloader_kwargs
        )
