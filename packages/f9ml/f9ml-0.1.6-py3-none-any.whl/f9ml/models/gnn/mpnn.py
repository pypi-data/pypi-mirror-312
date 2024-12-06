import torch
import torch.nn as nn
from torch_geometric.nn import BatchNorm, GATv2Conv, GraphNorm, MessagePassing, global_mean_pool

from f9ml.models.gnn.cnn import CNN
from f9ml.models.gnn.gnn_base import BaseGNN


class NormedMPNNBlock(nn.Module):
    def __init__(
        self,
        hidden_dim,
        num_edge_features,
        heads,
        input_dim=None,
        mlp_heads_reduction=False,
        cnn_heads_reduction=False,
        dropout=0.0,
        use_graph_norm=True,
    ):
        """

        References
        ----------
        [1] - https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.models.DeepGCNLayer.html#torch_geometric.nn.models.DeepGCNLayer

        """
        super().__init__()
        self.layers = nn.ModuleList()
        self.heads = heads
        self.hidden_dim = hidden_dim
        self.cnn_heads_reduction = cnn_heads_reduction

        input_dim = input_dim if input_dim is not None else hidden_dim

        if use_graph_norm:
            self.layers.append(GraphNorm(input_dim))
        else:
            self.layers.append(BatchNorm(input_dim))

        self.layers.append(nn.ReLU())

        self.layers.append(
            GATv2Conv(
                input_dim,
                hidden_dim,
                heads=heads,
                edge_dim=num_edge_features,
                dropout=dropout,
                concat=mlp_heads_reduction or cnn_heads_reduction,
            )
        )

        if mlp_heads_reduction:
            self.layers.append(nn.Linear(hidden_dim * heads, hidden_dim))
            self.layers.append(nn.Dropout(0.5))

        if cnn_heads_reduction:
            self.layers.append(CNN(in_channels=1, output_dim=hidden_dim, dropout=dropout))

    def forward(self, x, edge_index, edge_attr, batch):
        for layer in self.layers:
            if isinstance(layer, GraphNorm):
                x = layer(x, batch)
            elif isinstance(layer, GATv2Conv):
                x = layer(x, edge_index, edge_attr)
                if self.cnn_heads_reduction:
                    x = x.reshape(len(batch), 1, self.hidden_dim, self.heads)  # N, C, H, W
            else:
                x = layer(x)

        return x


class ResNormedMPNN(nn.Module):
    def __init__(self, hidden_dim, *args, num_blocks=2, input_dim=None, block_num=None, **kwargs):
        """NormedMPNNBlocks with residual connections.

        TODO: make this less confusing (or write some docs)...

        Parameters
        ----------
        num_blocks : int, optional
            Number of blocks after to add a residual connection, by default 2. If None do not add connection and keep 1 block.
        input_dim : int, optional
            If None use hidden dimension as input, by default None.
        block_num : bool, optional
            Index of this block object in a module list, by default None.
        """
        super().__init__()
        if num_blocks is None:
            self.num_blocks = None
            num_blocks = 1
        else:
            self.num_blocks = num_blocks

        self.block_num = block_num

        self.blocks = nn.ModuleList()

        for i in range(num_blocks):
            if i == 0 and input_dim is not None and self.num_blocks is not None:
                self.blocks.append(nn.Linear(input_dim, hidden_dim))  # input projection

            if self.num_blocks is None:
                self.blocks.append(
                    NormedMPNNBlock(hidden_dim, *args, input_dim=input_dim if i == 0 else None, **kwargs)
                )
            else:
                self.blocks.append(NormedMPNNBlock(hidden_dim, *args, input_dim=None, **kwargs))

    def forward(self, x, edge_index, edge_attr, batch):
        residual = x
        for block in self.blocks:
            if isinstance(block, nn.Linear):
                x = block(x)
                if self.block_num == 0:
                    residual = x
            else:
                x = block(x, edge_index, edge_attr, batch)

        if self.num_blocks is None:
            return x
        else:
            return x + residual


class AttentionMPNN(BaseGNN):
    def __init__(self, model_conf):
        """Attention GNN with residual connections and batch normalizations.

        See also: https://pytorch-geometric.readthedocs.io/en/latest/modules/nn.html#normalization-layers

        References
        ----------
        [1] - Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift: https://arxiv.org/abs/1502.03167
        [2] - Deep Residual Learning for Image Recognition: https://arxiv.org/abs/1512.03385
        [3] - Graph Attention Networks: https://arxiv.org/abs/1710.10903
        [4] - DeeperGCN: All You Need to Train Deeper GCNs: https://arxiv.org/abs/2006.07739
        [5] - GraphNorm: A Principled Approach to Accelerating Graph Neural Network Training: https://arxiv.org/abs/2009.03294

        """
        super().__init__(model_conf)
        self.heads = model_conf["heads"]
        self.cat_global = model_conf["cat_global"]

        self.convs = nn.ModuleList()

        for i in range(self.num_layers):
            self.convs.append(
                ResNormedMPNN(
                    self.hidden_dim,
                    self.num_edge_features,
                    self.heads,
                    input_dim=self.num_node_features if i == 0 else None,
                    num_blocks=self.model_conf["num_res_blocks"],
                    mlp_heads_reduction=self.model_conf["mlp_heads_reduction"],
                    cnn_heads_reduction=self.model_conf["cnn_heads_reduction"],
                    dropout=self.dropout,
                    use_graph_norm=self.model_conf["graph_norm"],
                    block_num=i,
                )
            )

    def forward(self, x, global_x, edge_index, edge_attr, batch):
        for conv in self.convs:
            x = conv(x, edge_index, edge_attr, batch)

        x = global_mean_pool(x, batch)

        if self.mlp_global_net:
            g = self.mlp_global_net(global_x)
            if self.cat_global:
                x = torch.cat([g, x], dim=1)
            else:
                x = x + g

        x = self.mlp_classifier(x)

        return x


class EdgeModel(nn.Module):
    def __init__(self, num_edge_features, hidden_dim):
        super().__init__()
        self.edge_mlp = nn.Sequential(
            nn.Linear(num_edge_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def forward(self, edge_attr):
        return self.edge_mlp(edge_attr)


class NodeModel(MessagePassing):
    def __init__(self, num_node_features, num_edge_features, hidden_dim):
        super().__init__(aggr="mean")
        self.node_mlp = nn.Sequential(
            nn.Linear(num_node_features + hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.edge_mlp = EdgeModel(num_edge_features, hidden_dim)
        self.own_node_mlp = nn.Sequential(
            nn.Linear(num_node_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def forward(self, x, edge_index, edge_attr):
        edge_attr = self.edge_mlp(edge_attr)
        return self.propagate(edge_index, x=x, edge_attr=edge_attr) + self.own_node_mlp(x)

    def message(self, x_j, edge_attr):
        return torch.cat((x_j, edge_attr), dim=-1)

    def update(self, aggr_out):
        return self.node_mlp(aggr_out)


class NodeModelMPNN(BaseGNN):
    def __init__(self, model_conf):
        """This is a pytorch-lightning implementation of a message passing neural network introduced in [1] with some additions.

        Note
        ----
        The model inherits MessagePassing module found in [2]. Additionally this class has an option to include GATConv layer [3].

        References
        ----------
        [1] - https://journals.aps.org/prd/abstract/10.1103/PhysRevD.104.056003
        [2] - https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.conv.MessagePassing.html#torch_geometric.nn.conv.MessagePassing
        [3] - https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.conv.GATConv.html

        """
        super().__init__(model_conf)
        self.cat_global = model_conf["cat_global"]

        self.convs = nn.ModuleList()
        for i in range(self.num_layers):
            input_dim = self.num_node_features if i == 0 else self.hidden_dim

            if model_conf["batch_norm"]:
                self.convs.append(BatchNorm(input_dim))
            elif model_conf["graph_norm"]:
                self.convs.append(GraphNorm(input_dim))
            else:
                pass

            if model_conf["batch_norm"] or model_conf["graph_norm"]:
                self.convs.append(nn.ReLU())

            self.convs.append(NodeModel(input_dim, self.num_edge_features, self.hidden_dim))

            if model_conf["batch_norm"] is False and model_conf["graph_norm"] is False:
                self.convs.append(nn.ReLU())

        if model_conf["batch_norm"]:
            self.convs.append(BatchNorm(input_dim))
        elif model_conf["graph_norm"]:
            self.convs.append(GraphNorm(input_dim))

    def forward(self, x, global_x, edge_index, edge_attr, batch):
        for conv in self.convs:
            if isinstance(conv, (BatchNorm, nn.ReLU)):
                x = conv(x)
            elif isinstance(conv, GraphNorm):
                x = conv(x, batch)
            else:
                x = conv(x, edge_index, edge_attr)

        x = global_mean_pool(x, batch)  # readout layer

        if self.mlp_global_net:
            g = self.mlp_global_net(global_x)
            if self.cat_global:
                x = torch.cat([g, x], dim=1)
            else:
                x = x + g

        x = self.mlp_classifier(x)  # train a classifier based on graph embeddings

        return x
