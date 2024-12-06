import torch
import torch.nn as nn

from f9ml.nn.mlp import BasicMLP, BasicResMLP
from f9ml.training.modules import Module


class BaseGNN(nn.Module):
    def __init__(self, model_conf):
        """Base torch module for GNN models."""
        super().__init__()
        self.model_conf = model_conf
        self.num_node_features = model_conf["n_node"]
        self.num_edge_features = model_conf["n_edge"]
        self.num_global_features = model_conf["n_global"]
        self.num_layers = model_conf["n_conv_layers"]

        self.hidden_dim = model_conf["emb_dim"]
        self.output_dim = model_conf["output_dim"]
        self.dropout = model_conf["dropout"]

        if self.num_global_features > 0:
            layers = [self.num_global_features] + model_conf["global_mlp_layers"] + [self.hidden_dim]
            self.mlp_global_net = self.create_mlp(layers)
        else:
            self.mlp_global_net = None

        if len(model_conf["classifier_mlp_layers"]) > 0:
            inp = 2 * self.hidden_dim if model_conf["cat_global"] else self.hidden_dim
            layers = [inp] + model_conf["classifier_mlp_layers"] + [self.output_dim]
            self.mlp_classifier = self.create_mlp(layers)
        else:
            self.mlp_classifier = nn.Linear(
                2 * self.hidden_dim if model_conf["cat_global"] else self.hidden_dim, self.output_dim
            )

    def create_mlp(self, layers):
        if self.model_conf["mlp_module"] == "BasicMLP":
            return BasicMLP(
                layers,
                act=self.model_conf["mlp_activation_function"],
                act_out=self.model_conf["mlp_act_out"],
                batchnorm=self.model_conf["mlp_norm"],
                dropout=self.model_conf["mlp_dropout"],
                act_first=self.model_conf["mlp_act_first"],
            )
        elif self.model_conf["mlp_module"] == "BasicResMLP":
            return BasicResMLP(
                layers,
                act=self.model_conf["mlp_activation_function"],
                act_out=self.model_conf["mlp_act_out"],
                batchnorm=self.model_conf["mlp_norm"],
                dropout=self.model_conf["mlp_dropout"],
                act_first=self.model_conf["mlp_act_first"],
                repeats=self.model_conf["mlp_res_repeats"],
            )
        else:
            raise NotImplementedError("The selected mlp module is not implemented.")

    def forward(self):
        raise NotImplementedError("Forward method is not implemented.")


class ClassifierGNN(Module):
    def __init__(self, model_conf, training_conf, model, tracker=None):
        """Base lightning module for GNN models.

        Parameters
        ----------
        params : dict
            Parameters from src.utils.params are passed here.

        References
        ----------
        [1] - https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.models.MLP.html

        """
        super().__init__(model_conf, training_conf, model=model, tracker=tracker)
        self.model = self.model(model_conf)
        self.loss_func = getattr(torch.nn, training_conf["loss"])()
        self.save_hyperparameters(ignore=["tracker", "loss_func"])

    def forward(self, batch):
        yp = self.model(batch.x, batch.global_x, batch.edge_index, batch.edge_attr, batch.batch)
        return yp

    def _get_loss(self, batch):
        yp = self.forward(batch)
        loss = self.loss_func(yp, torch.argmax(batch.y, dim=1))
        return loss

    def training_step(self, batch, batch_idx):
        loss = self._get_loss(batch)
        self.log("train_loss", loss, batch_size=batch.y.size()[0])
        return loss

    def validation_step(self, batch, batch_idx):
        loss = self._get_loss(batch)
        self.log("val_loss", loss, batch_size=batch.y.size()[0])

    def test_step(self, batch, batch_idx):
        loss = self._get_loss(batch)
        self.log("test_loss", loss, batch_size=batch.y.size()[0])
