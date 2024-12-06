import copy
import logging

import lightning as L
import torch


class Module(L.LightningModule):
    def __init__(
        self,
        model_conf,
        training_conf,
        model,
        loss_func=None,
        tracker=None,
        split_idx_dct=None,
        scalers=None,
        selection=None,
    ):
        """Base class for MLP models in pytorch-lightning.

        Note
        ----
        If model is passed as None, you need to redefine forward function in your class.

        Parameters
        ----------
        params : dict
            Parameters from src.utils.params are passed here.
        model : nn.Module
            Torch model to use.
        loss_func : method
            Loss function to use.
        tracker : object
            Class for tracking (plots and metrices).
        split_idx_dct : dict
            Dictionary with split indices for train, val and test datasets.
        scalers : dict
            Dictionary with scalers for the data feature scaling.
        selection : pd.DataFrame
            Dictionary with the selection of features used in the model.

        References
        ----------
        [1] - https://pytorch.org/docs/stable/generated/torch.compile.html

        """
        super().__init__()
        self.model_conf = model_conf
        self.training_conf = training_conf
        self.output_dim = model_conf.get("output_dim")
        self.loss_func = loss_func
        self.tracker = tracker

        if self.training_conf.get("compile", False):
            logging.info("[b][red]Torch compile is ON! Model will be compiled in default mode.[/red][/b]")
            self.uncompiled_model = copy.deepcopy(model)  # need for saving with state_dict
            self.model = torch.compile(model, mode="default")
        else:
            self.uncompiled_model = None
            self.model = model

        if self.tracker is not None:
            self.tracker = self.tracker(self)  # initialize tracker

        # save split indices and scalers, if available, on train start from datamodule
        self.split_idx_dct, self.scalers, self.selection = split_idx_dct, scalers, selection

    def configure_optimizers(self):
        optimizer = getattr(torch.optim, self.training_conf["optimizer"])
        optimizer = optimizer(
            self.parameters(),
            lr=self.training_conf["learning_rate"],
            weight_decay=self.training_conf["weight_decay"],
        )

        if self.training_conf["scheduler"]["scheduler_name"]:
            get_scheduler = getattr(torch.optim.lr_scheduler, self.training_conf["scheduler"]["scheduler_name"])
            scheduler = get_scheduler(optimizer, **self.training_conf["scheduler"]["scheduler_params"])
            scheduler_dct = {
                "optimizer": optimizer,
                "lr_scheduler": {
                    "scheduler": scheduler,
                    "monitor": "val_loss",
                    "interval": self.training_conf["scheduler"]["interval"],
                },
            }
            return scheduler_dct
        else:
            return {"optimizer": optimizer}

    def forward(self, batch):
        yp = self.model(batch[0])
        return yp

    def _get_loss(self, batch):
        yp = self.forward(batch)
        loss = self.loss_func(batch[1], yp)
        return loss

    def training_step(self, batch, *args):
        loss = self._get_loss(batch)
        self.log("train_loss", loss, batch_size=batch[0].size()[0])
        return loss

    def validation_step(self, batch, *args):
        loss = self._get_loss(batch)
        self.log("val_loss", loss, batch_size=batch[0].size()[0])

    def test_step(self, batch, *args):
        loss = self._get_loss(batch)
        self.log("test_loss", loss, batch_size=batch[0].size()[0])

    def on_train_start(self):
        dm = self._trainer.datamodule

        try:
            train_idx, val_idx, test_idx = dm.train_idx, dm.val_idx, dm.test_idx
            self.split_idx_dct = {"train_idx": train_idx, "val_idx": val_idx, "test_idx": test_idx}
        except Exception:
            pass

        try:
            self.scalers = dm.scalers
        except Exception:
            pass

        try:
            self.selection = dm.selection
        except Exception:
            pass

        self.logger.experiment.log_text(self.logger.run_id, str(self), "model_str.txt")

    def on_train_end(self):
        dm = self._trainer.datamodule

        try:
            train, val = dm.train, dm.val
            self.splits = [train.splits, val.splits]
        except Exception:
            pass

        try:
            train, val = dm.train, dm.val
            self.scalers = [train.scalers, val.scalers]
        except Exception:
            pass

    def on_train_epoch_end(self):
        if self.training_conf["scheduler"]["scheduler_name"]:
            reduce_lr_on_epoch = self.training_conf["scheduler"]["reduce_lr_on_epoch"]
            if reduce_lr_on_epoch is not None:
                self.lr_schedulers().base_lrs = [self.lr_schedulers().base_lrs[0] * reduce_lr_on_epoch]

    def on_validation_epoch_end(self):
        if self.tracker:
            self.tracker.compute(stage="val")
            self.tracker.plot()

    def on_test_start(self):
        if self.tracker:
            self.tracker.compute(stage="test")
            self.tracker.plot()
