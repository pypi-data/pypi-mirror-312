import numpy as np
import scipy.linalg as sp_linalg
import torch
import torch.nn as nn
from torch.nn import functional as F


class Flow(nn.Module):
    def __init__(self):
        """Base class for all flows.

        Forward and inverse must also return log of Jacobian determinant summed over feature dimension.

        Basic idea is taken from [1] (note that original code is very buggy).

        Note
        ----
        forward - generative direction
        inverse - normalzing direction (assumed when training)

        References
        ----------
        [1] - Normalizing flows with PyTorch: https://github.com/acids-ircam/pytorch_flows

        """
        super().__init__()
        # True if uses masking and implements set_mask
        self.mask = False
        # if False forward is proper nn.Module forward else use inverse in NormalizingFlow base class
        self.normalizing_direction = True

    def forward(self):
        raise NotImplementedError

    def inverse(self):
        raise NotImplementedError


class BatchNormFlow(Flow):
    def __init__(self, features, eps=1e-5, momentum=0.1):
        """Transform that performs batch normalization.

        References
        ----------
        [1] - https://github.com/bayesiains/nflows/blob/master/nflows/transforms/normalization.py

        """
        super().__init__()
        self.normalizing_direction = False
        self.momentum = momentum
        self.eps = eps
        constant = np.log(np.exp(1 - eps) - 1)
        self.unconstrained_weight = nn.Parameter(constant * torch.ones(features))
        self.bias = nn.Parameter(torch.zeros(features))

        self.register_buffer("running_mean", torch.zeros(features))
        self.register_buffer("running_var", torch.zeros(features))

    @property
    def weight(self):
        return F.softplus(self.unconstrained_weight) + self.eps

    def forward(self, inputs):
        if inputs.dim() != 2:
            raise ValueError("Expected 2-dim inputs, got inputs of shape: {}".format(inputs.shape))

        if self.training:
            mean, var = inputs.mean(0), inputs.var(0)
            self.running_mean.mul_(1 - self.momentum).add_(mean.detach() * self.momentum)
            self.running_var.mul_(1 - self.momentum).add_(var.detach() * self.momentum)
        else:
            mean, var = self.running_mean, self.running_var

        outputs = self.weight * ((inputs - mean) / torch.sqrt((var + self.eps))) + self.bias

        logabsdet_ = torch.log(self.weight) - 0.5 * torch.log(var + self.eps)
        logabsdet = torch.sum(logabsdet_) * inputs.new_ones(inputs.shape[0], 1)

        return outputs, logabsdet

    def inverse(self, inputs):
        # Batch norm inverse should only be used in eval mode, not in training mode.
        outputs = torch.sqrt(self.running_var + self.eps) * ((inputs - self.bias) / self.weight) + self.running_mean

        logabsdet_ = -torch.log(self.weight) + 0.5 * torch.log(self.running_var + self.eps)
        logabsdet = torch.sum(logabsdet_) * inputs.new_ones(inputs.shape[0], 1)

        return outputs, logabsdet


class ReverseFlow(Flow):
    def __init__(self, forward_dim, inverse_dim=None, repeats=1):
        super().__init__()
        self.normalizing_direction = False

        self.permute = torch.arange(forward_dim - 1, -1, -1).repeat(1, repeats).squeeze()

        if inverse_dim is None:
            self.inverse_permute = torch.argsort(self.permute)
        else:
            permute_ = torch.arange(inverse_dim - 1, -1, -1)
            self.inverse_permute = torch.argsort(permute_)

    def forward(self, z):
        return z[:, self.permute], torch.zeros_like(z).sum(dim=-1, keepdim=True)

    def inverse(self, z):
        return z[:, self.inverse_permute], torch.zeros_like(z).sum(dim=-1, keepdim=True)


class Conv1x1PLU(nn.Module):
    def __init__(self, dim, device="cpu"):
        """Invertible 1x1 convolution using LU decomposition.

        References
        ----------
        [1] - https://github.com/tonyduan/normalizing-flows/blob/master/nf/flows.py

        """
        super().__init__()
        self.normalizing_direction = False
        self.device = device
        self.dim = dim

        W, _ = sp_linalg.qr(np.random.randn(dim, dim))
        P, L, U = sp_linalg.lu(W)

        self.P = torch.tensor(P, dtype=torch.float, device=self.device)
        self.L = nn.Parameter(torch.tensor(L, dtype=torch.float, device=self.device))
        self.S = nn.Parameter(torch.tensor(np.diag(U), dtype=torch.float, device=self.device))
        self.U = nn.Parameter(torch.triu(torch.tensor(U, dtype=torch.float, device=self.device), diagonal=1))

    def forward(self, x):
        L = torch.tril(self.L, diagonal=-1) + torch.diag(torch.ones(self.dim, device=self.L.device))
        U = torch.triu(self.U, diagonal=1)

        W = self.P @ L @ (U + torch.diag(self.S))
        z = x @ W

        log_det = torch.sum(torch.log(torch.abs(self.S)))

        return z, log_det * x.new_ones(x.shape[0], 1)

    def inverse(self, z):
        L = torch.tril(self.L, diagonal=-1) + torch.diag(torch.ones(self.dim, device=self.L.device))
        U = torch.triu(self.U, diagonal=1)

        W = self.P @ L @ (U + torch.diag(self.S))
        W_inv = torch.inverse(W)
        x = z @ W_inv

        log_det = -torch.sum(torch.log(torch.abs(self.S)))

        return x, log_det * z.new_ones(z.shape[0], 1)
