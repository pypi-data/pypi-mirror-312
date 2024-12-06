import torch
import torch.nn.functional as F
from torch.nn import LayerNorm, Linear, ReLU
from torch_geometric.nn import AttentionalAggregation, DeepGCNLayer, GENConv

from f9ml.models.gnn.gnn_base import BaseGNN


class DeeperGCN(BaseGNN):
    def __init__(self, model_conf):
        """

        References
        ----------
        [1] - https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.conv.GENConv.html#torch_geometric.nn.conv.GENConv
        [2] - https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.models.DeepGCNLayer.html#torch_geometric.nn.models.DeepGCNLayer
        [3] - https://github.com/pyg-team/pytorch_geometric/blob/master/examples/ogbn_proteins_deepgcn.py

        """
        super().__init__(model_conf)
        self.cat_global = model_conf["cat_global"]

        self.node_encoder = Linear(self.num_node_features, self.hidden_dim)

        if self.num_edge_features is not None:
            self.edge_encoder = Linear(self.num_edge_features, self.hidden_dim)
        else:
            self.edge_encoder = None

        self.layers = torch.nn.ModuleList()
        for _ in range(1, self.num_layers + 1):
            conv = GENConv(
                self.hidden_dim,
                self.hidden_dim,
                aggr="softmax",
                t=1.0,
                learn_t=True,
                num_layers=2,
                norm="layer",
            )
            norm = LayerNorm(self.hidden_dim, elementwise_affine=True)
            act = ReLU(inplace=True)

            layer = DeepGCNLayer(conv, norm, act, block="res+", dropout=self.dropout)
            self.layers.append(layer)

        self.post_att = Linear(self.hidden_dim, self.hidden_dim)
        self.att = AttentionalAggregation(Linear(self.hidden_dim, 1))

    def forward(self, x, global_x, edge_index, edge_attr, batch):
        x = self.node_encoder(x)

        if edge_attr:
            edge_attr = self.edge_encoder(edge_attr)

        x = self.layers[0].conv(x, edge_index, edge_attr)

        for layer in self.layers[1:]:
            x = layer(x, edge_index, edge_attr)

        x = self.layers[0].act(self.layers[0].norm(x))
        x = F.dropout(x, p=self.dropout, training=self.training)

        x = self.att(x, batch)
        x = self.post_att(x)
        x = F.dropout(x, p=self.dropout, training=self.training)

        if self.mlp_global_net:
            g = self.mlp_global_net(global_x)
            if self.cat_global:
                x = torch.cat([g, x], dim=1)
            else:
                x = x + g

        x = self.mlp_classifier(x)

        return x
