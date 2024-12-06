import lightning as L
from torch_geometric.loader import DataLoader

from f9ml.models.gnn.data_utils.graph_datasets import GraphDataset, GraphInMemoryDataset


class GraphDataModule(L.LightningDataModule):
    def __init__(self, processor, root=None, graph_file_name=None, dataset=GraphDataset, **dataloader_kwargs):
        """Base class for graph data modules. Uses disk dataset storage.

        Parameters
        ----------
        processor : object
            Processor object which contains the methods to process the dataset (e.g. ProcessorChainer).
        root : str, optional
            Root directory where the dataset should be saved, by default None.
        graph_file_name : str, optional
            Name of the graph files in processed_dir, by default None.
        dataset : object, optional
            Dataset class to use, by default GraphDataset.

        References
        ----------
        [1] - https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader
        [2] - https://pytorch.org/docs/stable/data.html#torch.utils.data.SubsetRandomSampler
        [3] - https://towardsdatascience.com/pytorch-basics-sampling-samplers-2a0f29f0bf2a

        """
        super().__init__()
        self.processor = processor
        self.dataset = dataset
        self.root, self.graph_file_name = root, graph_file_name

        self.dataloader_kwargs = dataloader_kwargs

    def prepare_data(self):
        pass

    def setup(self, stage=None):
        if stage == "fit" or stage is None:
            self.train_dataset = self.dataset(
                processor=self.processor,
                root=self.root,
                graph_file_name=self.graph_file_name,
                stage="train",
            )
            self.val_dataset = self.dataset(
                processor=self.processor,
                root=self.root,
                graph_file_name=self.graph_file_name,
                stage="val",
            )
        if stage == "test":
            self.test_dataset = self.dataset(
                processor=self.processor,
                root=self.root,
                graph_file_name=self.graph_file_name,
                stage="test",
            )

    def teardown(self, stage=None):
        if stage == "fit":
            self.train_dataset = None
            self.val_dataset = None
        if stage == "test":
            self.test_dataset = None

    def train_dataloader(self):
        return DataLoader(self.train_dataset, shuffle=True, **self.dataloader_kwargs)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, shuffle=False, **self.dataloader_kwargs)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, shuffle=False, **self.dataloader_kwargs)


class GraphInMemoryDataModule(GraphDataModule):
    def __init__(self, processor, dataset=GraphInMemoryDataset, make_data_lst=False, **dataloader_kwargs):
        """Data module for graph datasets that are stored in memory.

        Parameters
        ----------
        processor : object
            Processor object which contains the methods to process the dataset (e.g. ProcessorChainer).
        dataset : object, optional
            Dataset class to use, by default GraphInMemoryDataset.
        make_data_lst : bool, optional
            Whether to make a list of data objects for each graph in the dataset, by default False.

        """
        super().__init__(processor, dataset=dataset, **dataloader_kwargs)
        self.make_data_lst = make_data_lst
        self.selection, self.scalers = None, None

    def setup(self, stage=None):
        graph_data, self.selection, self.scalers = self.processor()

        assert any(
            [i in list(graph_data.keys()) for i in ["train", "val", "test"]]
        ), "Data must be split into train/val/test"

        if stage == "fit" or stage is None:
            self.train_dataset = self.dataset(
                graph_data,
                stage="train",
                make_data_lst=self.make_data_lst,
            )
            self.val_dataset = self.dataset(
                graph_data,
                stage="val",
                make_data_lst=self.make_data_lst,
            )
        if stage == "test":
            self.test_dataset = self.dataset(
                graph_data,
                stage="test",
                make_data_lst=self.make_data_lst,
            )
