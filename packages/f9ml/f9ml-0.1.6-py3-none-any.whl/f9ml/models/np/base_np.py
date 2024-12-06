from abc import ABC, abstractmethod

import torch.nn as nn
from torch.distributions import Normal
from torch.distributions.independent import Independent

from f9ml.nn.mlp import BasicMLP, BasicResMLP
from f9ml.training.modules import Module


def MultivariateNormalDiag(loc, scale_diag):
    """Multi variate Gaussian with a diagonal covariance function (on the last dimension)."""

    if loc.dim() < 1:
        raise ValueError("loc must be at least one-dimensional.")

    return Independent(Normal(loc, scale_diag), 1)


class BaseNeuralProcess(nn.Module, ABC):
    def __init__(self, model_conf, data_conf, experiment_conf):
        """Base class for all Neural Processes.

        References
        ----------
        [1] - https://github.com/YannDubs/Neural-Process-Family
        [2] - https://github.com/JuHyung-Son/Neural-Process
        [3] - https://github.com/geniki/neural-processes

        """
        super().__init__()
        self.model_conf, self.data_conf, self.experiment_conf = model_conf, data_conf, experiment_conf

        self.input_dim = data_conf["input_dim"]
        self.r_dim = model_conf["r_dim"]

    def create_mlp(self, layers):
        if self.model_conf["mlp_module"] == "BasicMLP":
            return BasicMLP(
                layers,
                act=self.model_conf["activation"],
                act_out=self.model_conf["act_out"],
                batchnorm=self.model_conf["batchnorm"],
                dropout=self.model_conf["dropout"],
                act_first=self.model_conf["act_first"],
            )
        elif self.model_conf["mlp_module"] == "BasicResMLP":
            return BasicResMLP(
                layers,
                act=self.model_conf["activation"],
                act_out=self.model_conf["act_out"],
                batchnorm=self.model_conf["batchnorm"],
                dropout=self.model_conf["dropout"],
                act_first=self.model_conf["act_first"],
                repeats=self.model_conf["repeats"],
            )
        else:
            raise NotImplementedError("The selected mlp module is not implemented.")

    @abstractmethod
    def get_loss(self, *args, **kwargs):
        pass

    @abstractmethod
    def forward(self, x_c, y_c, x_t, y_t):
        pass


def make_meta_dataset(x, y, n_context, y_t=True):
    """Meta dataset creation.

    Meta-dataset is defined as M = D_i for N tasks, where D_i = (x_c, y_c, x_t, y_t). Tensors x, y have a shape of
    (B, C, D), where B is the batch size, C is the number of context points and D is the dimensionality of the data.

    Parameters
    ----------
    x : torch.Tensor
        Independent variable.
    y : torch.Tensor
        Dependent variable.
    n_context : int
        Number of context points.
    y_t : bool, optional
        Flag if in training mode (where we have y_t), by default True

    Returns
    -------
    (x_c, y_c, x_t, y_t) or (x_c, y_c, x_t)
        Meta-dataset tuple.

    """
    assert x.shape[0] % (2 * n_context) == 0

    if y_t:
        x_c, y_c = x[: len(x) // 2], y[: len(y) // 2]
        x_t, y_t = x[len(x) // 2 :], y[len(y) // 2 :]

        batch_size = x.shape[0] // (2 * n_context)

        meta_dataset = (
            x_c.view(batch_size, n_context, x.shape[1]),
            y_c.view(batch_size, n_context, y.shape[1]),
            x_t.view(batch_size, n_context, x.shape[1]),
            y_t.view(batch_size, n_context, y.shape[1]),
        )
    else:
        assert y.shape[0] == x.shape[0] // 2

        x_c, y_c = x[: len(x) // 2], y
        x_t = x[len(x) // 2 :]

        batch_size = x.shape[0] // (2 * n_context)

        meta_dataset = (
            x_c.view(batch_size, n_context, x.shape[1]),
            y_c.view(batch_size, n_context, y.shape[1]),
            x_t.view(batch_size, n_context, x.shape[1]),
        )

    return meta_dataset


class NPModule(Module, ABC):
    def __init__(self, model_conf, training_conf, data_conf, model, tracker=None):
        super().__init__(model_conf, training_conf, model, loss_func=None, tracker=tracker)
        self.data_conf = data_conf
        self.save_hyperparameters(ignore=["loss_func", "tracker", "model"])
        self.n_context = data_conf["n_context"]

    def make_meta_dataset(self, x, y):
        return make_meta_dataset(x, y, self.n_context)

    def on_train_start(self):
        super().on_train_start()

        dm = self._trainer.datamodule
        x, y = next(iter(dm.train_dataloader()))

        meta_dataset = self.make_meta_dataset(x, y)

        shape = meta_dataset[0].shape

        self.logger.experiment.log_text(
            self.logger.run_id,
            f"Meta dataset dimensions: B={shape[0]}, C={shape[1]}, D={shape[2]}.",
            "meta_dataset_info.txt",
        )

    def training_step(self, batch, *args):
        x, y = batch

        x_c, y_c, x_t, y_t = self.make_meta_dataset(x, y)

        _, _, loss = self.model.forward(x_c, y_c, x_t, y_t)

        self.log("train_loss", loss)

        return {"loss": loss}

    def validation_step(self, batch, *args):
        x, y = batch

        x_c, y_c, x_t, y_t = self.make_meta_dataset(x, y)

        _, _, loss = self.model.forward(x_c, y_c, x_t, y_t)

        self.log("val_loss", loss)

        return {"loss": loss}

    def test_step(self, batch, *args):
        pass
