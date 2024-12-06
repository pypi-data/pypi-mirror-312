import logging

import h5py
import numpy as np
import torch
from torch.utils.data import Dataset, IterableDataset


class NpDataset(Dataset):
    def __init__(self, processors, split_idx, save_scalers=False, get_labels=False):
        """General dataset class for numpy data. The data is processed by the processors graph and split into train,
        validation and test sets. The data is then returned as a torch.Tensor. All data is loaded into memory.

        Parameters
        ----------
        processors: dict of DataProcessor
            Data processors.
        split_idx : np.array
            Indices of the data split (train, test or val).
        save_scalers : bool, optional
            Save scalers in dataset object.
        get_labels : bool, optional
            Use labels, if False return X, if True return X and y labels.
        """
        super().__init__()
        self.save_scalers, self.scalers = save_scalers, {}
        self.get_labels = get_labels

        output_processor = processors["output"]
        data, self.selection, scalers = output_processor.data, output_processor.selection, output_processor.scalers

        data = data[split_idx]

        if self.save_scalers:
            self.scalers = scalers

        if get_labels:
            features = self.selection[self.selection["type"] != "label"]
            labels = self.selection[self.selection["type"] == "label"]

            self.X = torch.from_numpy(data[:, features.index]).to(torch.float32)
            self.y = torch.from_numpy(data[:, labels.index]).to(torch.float32)
        else:
            self.X = torch.from_numpy(data).to(torch.float32)
            self.y = None

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        if self.y is not None:
            return self.X[idx], self.y[idx]
        else:
            return self.X[idx]


class SplitHDF5DataGenerator:
    def __init__(
        self,
        processors_graph,
        file_path,
        hdf5_loader,
        shape,
        chunks_idx,
        split_idx,
        n_chunks,
        worker_id=0,
        save_scalers=False,
        get_labels=False,
        return_graph=False,
    ):
        self.processors_graph = processors_graph
        self.file_path = file_path
        self.hdf5_loader = hdf5_loader

        self.dataset_name = self.hdf5_loader.dataset_name
        self.chunk_size = self.hdf5_loader.chunk_size
        self.shuffle = self.hdf5_loader.shuffle

        self.shape = shape
        self.chunks_idx = chunks_idx
        self.split_idx = split_idx
        self.n_chunks = n_chunks

        self.worker_id = worker_id
        self.save_scalers, self.scalers = save_scalers, {}
        self.get_labels = get_labels
        self.return_graph = return_graph

        self.selection = None
        self.features_idx, self.labels_idx = None, None

        self.current_item, self.current_chunk_idx = 0, 0
        self.current_shape = self.chunks_idx[self.current_chunk_idx].shape

    def _run_processors_graph(self, chunk_data):
        self.hdf5_loader.chunk_data = chunk_data
        fitted_processors = self.processors_graph.fit()

        outputs = fitted_processors["output"]

        if self.save_scalers:
            if self.current_chunk_idx not in self.scalers:
                self.scalers[self.current_chunk_idx] = outputs.scalers

        if self.selection is None:
            self.selection = outputs.selection

        return fitted_processors

    def _load_chunk(self):
        """Load the next chunk of data that fits into memory from disk.

        Returns
        -------
        np.array
            Chunk of data.
        """
        if self.current_chunk_idx == self.n_chunks:
            raise StopIteration

        logging.debug(f"Loading chunk {self.current_chunk_idx}/{len(self.chunks_idx) - 1} on worker {self.worker_id}!")

        chunk_idx = self.chunks_idx[self.current_chunk_idx]

        if self.shuffle:
            chunk_data = np.empty((len(chunk_idx), self.shape[1]), dtype=np.float32)

            with h5py.File(self.file_path, "r") as f:
                for i in range(len((chunk_idx))):
                    random_idx = self.split_idx[self.current_chunk_idx][i]
                    chunk_data[i, :] = f[self.dataset_name][random_idx]
        else:
            with h5py.File(self.file_path, "r") as f:
                idx = self.split_idx[self.current_chunk_idx]
                chunk_data = f[self.dataset_name][idx]

        fitted_processors = self._run_processors_graph(chunk_data)
        chunk_data = fitted_processors["output"].data

        self.current_chunk_idx += 1
        self.current_shape = chunk_data.shape

        if self.get_labels:
            self.features_idx, self.labels_idx = self._setup_labels()

        return chunk_data

    def __iter__(self):
        return self

    def __next__(self):
        chunk_data = self._load_chunk()

        if self.get_labels:
            chunk_data = (chunk_data[:, self.features_idx], chunk_data[:, self.labels_idx])

        if self.return_graph:
            return chunk_data, self.processors_graph
        else:
            return chunk_data


class PiledHDF5DataGenerator:
    def __init__(
        self,
        processors_graph,
        file_path,
        hdf5_loader,
        piles_lst,
        piles_shapes,
        split_idx,
        drop_last=False,
        worker_id=0,
        save_scalers=False,
        get_labels=False,
        return_graph=False,
    ):
        self.processors_graph = processors_graph
        self.file_path = file_path

        self.hdf5_loader = hdf5_loader
        self.dataset_name = self.hdf5_loader.dataset_name
        self.chunk_size = self.hdf5_loader.chunk_size

        self.piles_lst = piles_lst
        self.piles_shapes = piles_shapes
        self.split_idx = split_idx
        self.drop_last = drop_last

        self.worker_id = worker_id

        self.save_scalers, self.scalers = save_scalers, {}
        self.get_labels = get_labels
        self.return_graph = return_graph

        self.selection = None
        self.features_idx, self.labels_idx = None, None

        self.current_pile_idx, self.current_chunk_idx, self.chunks_in_pile = 0, 0, 0
        self.pile_data = None

    def _run_processors_graph(self, pile_data):
        self.hdf5_loader.chunk_data = pile_data
        fitted_processors = self.processors_graph.fit()

        outputs = fitted_processors["output"]

        if self.save_scalers:
            if self.current_chunk_idx not in self.scalers:
                self.scalers[self.current_pile_idx] = outputs.scalers

        if self.selection is None:
            self.selection = outputs.selection

        return fitted_processors

    def _setup_labels(self):
        features = self.selection[self.selection["type"] != "label"]
        labels = self.selection[self.selection["type"] == "label"]

        features_idx, labels_idx = features.index, labels.index

        return features_idx, labels_idx

    def _load_pile(self):
        if self.current_pile_idx == len(self.piles_lst):
            raise StopIteration

        logging.debug(f"Loading pile {self.current_pile_idx}/{len(self.piles_lst) - 1} on worker {self.worker_id}!")

        pile = self.piles_lst[self.current_pile_idx]

        idx = self.split_idx[pile]
        np.random.shuffle(idx)

        with h5py.File(self.file_path, "r") as f:
            pile_data = f[pile][:]
            pile_data = pile_data[idx]

        fitted_processors = self._run_processors_graph(pile_data)
        self.pile_data = fitted_processors["output"].data

        curerent_pile_shape = self.pile_data.shape

        if curerent_pile_shape[0] < self.chunk_size and not self.drop_last:
            logging.warning(f"Chunk size {self.chunk_size} > pile size {curerent_pile_shape[0]}, skipping!")

        self.chunks_in_pile = curerent_pile_shape[0] // self.chunk_size
        if self.drop_last and not curerent_pile_shape[0] % self.chunk_size == 0:
            self.chunks_in_pile -= 1

        self.current_pile_idx += 1

        if self.get_labels:
            self.features_idx, self.labels_idx = self._setup_labels()

        return self.pile_data

    def __iter__(self):
        return self

    def __next__(self):
        if self.chunks_in_pile == self.current_chunk_idx or self.chunks_in_pile <= 0:
            self._load_pile()
            self.current_chunk_idx = 0
        else:
            self.current_chunk_idx += 1

        chunk_pile_data = self.pile_data[
            self.current_chunk_idx * self.chunk_size : (self.current_chunk_idx + 1) * self.chunk_size
        ]

        if self.get_labels:
            chunk_pile_data = (chunk_pile_data[:, self.features_idx], chunk_pile_data[:, self.labels_idx])

        if self.return_graph:
            return chunk_pile_data, self.processors_graph
        else:
            return chunk_pile_data


class HDF5IterableSplitDataset(IterableDataset):
    def __init__(
        self,
        processors_graph,
        split_idx=None,
        save_scalers=False,
        get_labels=False,
        return_graph=False,
        drop_last=False,
    ):
        """Create an iterable dataset from an hdf5 file.

        Parameters
        ----------
        processors_graph : DataProcessorsGraph
            Data processors graph.
        split_idx: np.array or dict of np.array, optional
            Indices of the data split (train, test or val). If the hdf5 file is split into piles, split_idx must be a
            dictionary with the pile name as key and the split indices as value.
        save_scalers : bool, optional
            Save scalers as dict with current chunk/pile index as key.
        get_labels : bool, optional
            Use labels, if False return X, if True return X and y labels.
        return_graph : bool, optional
            If True will return (X, fitted graph) or ((X, y), fitted graph).
        drop_last : bool, optional
            Drop the last incomplete batch.

        Note
        ----
        Each hdf5 file must have a dataset with the same name as the one provided in the processors graph. The hdf5 file
        can additionaly be split into piles (each pile is a separate dataset in the hdf5 file). Piles are used for
        efficient shuffling of data and are loaded into memory one at a time. If the hdf5 file is not split into piles,
        the data is split into chunks of size `chunk_size` (equivalent to `batch_size`) and loaded into memory one chunk
        at a time. In this case shuffling is inneficient and should generally be avoided by setting `shuffle=False` in the
        `HDF5Loader` processor.

        Danger
        ------
        Processors graph is fitted on each chunk/pile of data. This means that the preprocessing is done on the fly in
        parallel with the data loading. Scalers are saved in the `processors_graph` object and can be accessed with
        setting `return_graph=True`.

        References
        ----------
        [1] - https://blog.janestreet.com/how-to-shuffle-a-big-dataset/

        """
        super().__init__()
        self.processors_graph = processors_graph
        self.split_idx = split_idx

        self.save_scalers = save_scalers
        self.get_labels = get_labels
        self.return_graph = return_graph

        self.drop_last = drop_last

        self.processors_graph.copy_processors = True  # need to run each processor multiple times

        self.file_path = self.processors_graph.processors["input"].file_path

        self.hdf5_loader = self.processors_graph.processors["hdf5_loader"]
        self.chunk_size = self.hdf5_loader.chunk_size
        self.use_piles = self.hdf5_loader.use_piles

        if self.use_piles is False and self.chunk_size is None:
            raise ValueError("chunk_size must be provided if use_piles is False!")

        if self.use_piles:
            self.piles_lst = self.hdf5_loader.piles_lst
            self.piles_shapes = self.hdf5_loader.get_shape()
            self.shape = (sum([s[0] for s in self.piles_shapes]), self.piles_shapes[0][1])
        else:
            self.n_chunks = self.split_idx.shape[0] // self.chunk_size + 1
            self.shape = (self.split_idx.shape[0], self.hdf5_loader.get_shape()[1])
            self.chunks_idx, self.splits = self._setup_chunks_splits()

    def _setup_chunks_splits(self):
        """Split the data in hdf5 into chunks of size `chunk_size`.

        Returns
        -------
        list of arrays
            Indices of the data chunks.
        """
        idx = np.arange(0, self.split_idx.shape[0], 1)
        sections = [i * self.chunk_size for i in range(1, self.n_chunks, 1)]

        chunks_idx = np.array_split(idx, sections)
        splits = np.array_split(self.split_idx, sections)

        if self.drop_last:
            chunks_idx = chunks_idx[:-1]
            splits = splits[:-1]
            self.n_chunks -= 1

        return chunks_idx, splits

    def _iter_default(self):
        worker_info = torch.utils.data.get_worker_info()

        if worker_info is None:
            worker_id = 0
        else:
            worker_id = worker_info.id

        num_workers = worker_info.num_workers if worker_info is not None else 1
        self.hdf5_loader.num_workers = num_workers

        worker_split_chunks_idx, worker_split_splits, worker_shape_splits = [], [], []

        if len(self.chunks_idx) < num_workers:
            raise ValueError(f"Number of chunks ({len(self.chunks_idx)}) must be < num_workers ({num_workers})!")

        for i in range(num_workers):
            worker_split_chunks_idx.append(self.chunks_idx[i::num_workers])
            worker_split_splits.append(self.splits[i::num_workers])
            worker_shape_splits.append((sum([s.shape[0] for s in worker_split_chunks_idx[-1]]), self.shape[1]))

        return SplitHDF5DataGenerator(
            self.processors_graph,
            self.file_path,
            self.hdf5_loader,
            shape=worker_shape_splits[worker_id],
            chunks_idx=worker_split_chunks_idx[worker_id],
            split_idx=worker_split_splits[worker_id],
            n_chunks=self.n_chunks,
            worker_id=worker_id,
            save_scalers=self.save_scalers,
            get_labels=self.get_labels,
            return_graph=self.return_graph,
        )

    def _iter_piles(self):
        worker_info = torch.utils.data.get_worker_info()

        if worker_info is None:
            worker_id = 0
        else:
            worker_id = worker_info.id

        num_workers = worker_info.num_workers if worker_info is not None else 1
        self.hdf5_loader.num_workers = num_workers

        if len(self.piles_lst) < num_workers:
            raise ValueError(f"Number of piles ({len(self.piles_lst)}) must be < num_workers ({num_workers})!")

        worker_piles_split, worker_piles_shapes_split = [], []

        for i in range(num_workers):
            worker_piles_split.append(self.piles_lst[i::num_workers])
            worker_piles_shapes_split.append(self.piles_shapes[i::num_workers])

        return PiledHDF5DataGenerator(
            self.processors_graph,
            self.file_path,
            self.hdf5_loader,
            piles_lst=worker_piles_split[worker_id],
            piles_shapes=worker_piles_shapes_split[worker_id],
            split_idx=self.split_idx,
            drop_last=self.drop_last,
            worker_id=worker_id,
            save_scalers=self.save_scalers,
            get_labels=self.get_labels,
            return_graph=self.return_graph,
        )

    def __iter__(self):
        if self.use_piles:
            return self._iter_piles()
        else:
            return self._iter_default()
