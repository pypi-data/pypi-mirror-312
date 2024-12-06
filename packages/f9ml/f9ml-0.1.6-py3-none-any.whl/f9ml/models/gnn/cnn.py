import torch.nn as nn


class CNN(nn.Module):
    def __init__(self, params):
        """Convolutional Neural Network for dimensionality reduction.

        Parameters
        ----------
        in_channels : int, optional
           input dimension of the model, by default 1
        output_dim : int, optional
            output dimension, by default 128
        minimal : bool, optional
            type of cnn (simplified or complex), by default True
        dropout : float, optional
            dropout for the model, by default 0.0

        References
        ----------
        [1] - https://medium.com/thecyphy/train-cnn-model-with-pytorch-21dafb918f48
        """
        # TODO: test the reference [1]

        super().__init__()

        output_dim, dropout = params["output_dim"], params["dropout"]

        self.cnn_layers = nn.ModuleList(
            nn.Conv2d(1, 16, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.MaxPool2d(2, stride=4),
            nn.Flatten(),
            nn.Linear(128, output_dim),  # TODO: fix hardcoded
            nn.ReLU(),
            nn.BatchNorm1d(output_dim),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        for layer in self.cnn_layers:
            x = layer(x)
        return x
