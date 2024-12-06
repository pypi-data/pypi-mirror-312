import numpy as np
import pandas as pd

from f9ml.data_utils.data_modules import BaseDataModule, NpDataset, get_splits
from f9ml.data_utils.processors import DataProcessorsGraph


class NSDataModule(BaseDataModule):
    def __init__(self, processor: DataProcessorsGraph, data_processor_name: str, **kwargs):
        """Memory data module for in-memory data."""
        super().__init__(processor, **kwargs)
        self.data_processor_name = data_processor_name

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
        self.distributions = processors[self.data_processor_name].distributions

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
