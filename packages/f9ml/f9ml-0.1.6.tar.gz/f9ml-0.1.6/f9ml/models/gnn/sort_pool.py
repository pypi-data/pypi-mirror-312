import torch
import torch.nn.functional as F
from torch.nn import Conv1d, Linear
from torch_geometric.nn import GATv2Conv, SAGEConv, SortAggregation

from f9ml.models.gnn.gnn_base import BaseGNN


class SortPoolGNN(BaseGNN):
    def __init__(
        self,
        *args,
        k=30,
        conv_out_channels=32,
        conv_kernel_size=5,
        pool_kernel_size=2,
        **kwargs,
    ):
        """https://muhanzhang.github.io/papers/AAAI_2018_DGCNN.pdf

        TODO: add edge attributes to SAGEConv
        TODO: add more conv1d and maxpool1d layers

        Parameters
        ----------
        k : int
            The number of nodes to hold for each graph, see [1].
        conv_out_channels : int
            Number of output channels of the convolutional layer, see [4, 5].
        conv_kernel_size : int
            Kernel size of the convolutional layer, see [4].
        pool_kernel_size : int
            Kernel size of the maxpooling layer, see [5].

        Note
        ----
        If include_transformer is True, then GATConv is used, otherwise SAGEConv is used.

        References
        ----------
        [1] - https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.aggr.SortAggregation.html#torch_geometric.nn.aggr.SortAggregation
        [2] - https://github.com/pyg-team/pytorch_geometric/blob/master/benchmark/kernel/sort_pool.py
        [3] - https://stellargraph.readthedocs.io/en/stable/demos/graph-classification/dgcnn-graph-classification.html
        [4] - https://pytorch.org/docs/stable/generated/torch.nn.Conv1d.html
        [5] - https://pytorch.org/docs/stable/generated/torch.nn.MaxPool1d.html

        """
        super().__init__(*args, **kwargs)
        self.k = k
        self.heads = self.model_conf["heads"]
        self.mlp_heads_reduction = self.model_conf["mlp_heads_reduction"]
        self.cat_global = self.model_conf["cat_global"]

        if self.mlp_classifier is None:
            self.mlp_classifier = Linear(
                2 * self.hidden_dim if self.mlp_global_net else self.hidden_dim, self.output_dim
            )

        self.convs = torch.nn.ModuleList()
        for i in range(self.num_layers):
            if self.model_conf.get("include_transformer"):
                self.convs.append(
                    GATv2Conv(
                        self.num_node_features if i == 0 else self.hidden_dim,
                        self.hidden_dim,
                        heads=self.heads,
                        dropout=self.dropout,
                        edge_dim=self.num_edge_features,
                        concat=self.mlp_heads_reduction,
                    )
                )
                if self.mlp_heads_reduction:
                    self.convs.append(Linear(self.heads * self.hidden_dim, self.hidden_dim))
            else:
                self.convs.append(SAGEConv(self.num_node_features if i == 0 else self.hidden_dim, self.hidden_dim))

        self.pool = SortAggregation(k=self.k)
        self.conv1d = Conv1d(self.hidden_dim, conv_out_channels, conv_kernel_size)
        self.maxpool1d = torch.nn.MaxPool1d(kernel_size=pool_kernel_size)
        self.lin1 = Linear(conv_out_channels * (self.k - conv_kernel_size + 1) // pool_kernel_size, self.hidden_dim)

    def reset_parameters(self):
        for conv in self.convs:
            conv.reset_parameters()

        self.conv1d.reset_parameters()
        self.lin1.reset_parameters()

        self.mlp_classifier.reset_parameters()

        if self.mlp_global_net:
            self.mlp_global_net.reset_parameters()

    def forward(self, x, global_x, edge_index, edge_attr, batch):
        for conv in self.convs:
            if isinstance(conv, GATv2Conv):
                x = F.relu(conv(x, edge_index, edge_attr))
            elif isinstance(conv, Linear):
                x = F.relu(conv(x))
            else:
                x = F.relu(conv(x, edge_index))

        x = self.pool(x, batch)
        x = x.view(len(x), self.k, -1).permute(0, 2, 1)
        x = self.conv1d(x)
        x = self.maxpool1d(x)
        x = F.relu(x)
        x = x.view(len(x), -1)  # flatten
        x = F.relu(self.lin1(x))
        x = F.dropout(x, p=0.5, training=self.training)

        if self.mlp_global_net:
            g = self.mlp_global_net(global_x)
            if self.cat_global:
                x = torch.cat([g, x], dim=1)
            else:
                x = x + g

        x = self.mlp_classifier(x)

        return x
