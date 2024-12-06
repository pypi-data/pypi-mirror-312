import torch
import torch.nn as nn
from torch.nn import functional as F

from f9ml.models.np.base_np import BaseNeuralProcess, MultivariateNormalDiag, NPModule


class CNPEncoder(nn.Module):
    def __init__(self, encoder_net):
        super().__init__()
        self.encoder_net = encoder_net

    def forward(self, x_c, y_c):
        batch_size, context_size, dim = x_c.shape  # B, C, D

        x = torch.cat([x_c, y_c], dim=1)  # B x (C + T) x D
        x = x.view(batch_size * 2 * context_size, dim)  # B * 2C x D

        r = self.encoder_net(x)  # B * 2C x R
        r = r.view(batch_size, 2 * context_size, r.shape[1])  # B x (C + T) x R

        r_agg = torch.mean(r, dim=1, keepdim=True)  # B x 1 x R

        return r_agg


class CNPDecoder(nn.Module):
    def __init__(self, decoder_net, eps=1e-3):
        super().__init__()
        self.decoder_net = decoder_net
        self.eps = eps

    def forward(self, r, x_t):
        batch_size, n_context, _ = x_t.shape  # B x C x D

        # r = B x 1 x R
        # target dependent representation
        r = r.expand(batch_size, n_context, r.shape[-1])  # B x C x R

        x = torch.cat([x_t, r], dim=-1)  # B x C x (R + D)
        x = x.view(batch_size * n_context, -1)  # B * C x (R + D)

        x = self.decoder_net(x)  # B * C x 2 * D
        x = x.view(batch_size, n_context, -1)  # B x C x 2 * D

        mu_t, log_var_t = torch.chunk(x, 2, dim=-1)  # B x C x D

        return mu_t, self.eps + (1 - self.eps) * F.softplus(log_var_t)


class CNP(BaseNeuralProcess):
    def __init__(self, model_conf, data_conf, experiment_conf):
        """Conditional Neural Process (LNP) model.

        References
        ----------
        [1] - https://arxiv.org/abs/1807.01613
        [2] - https://github.com/YannDubs/Neural-Process-Family
        [3] - https://github.com/JuHyung-Son/Neural-Process

        """
        super().__init__(model_conf, data_conf, experiment_conf)

        encoder_net = self.create_mlp([self.input_dim] + self.model_conf["encoder_layers"] + [self.r_dim])
        decoder_net = self.create_mlp(
            [self.r_dim + self.input_dim] + self.model_conf["decoder_layers"] + [2 * self.input_dim]
        )

        self.encoder = CNPEncoder(encoder_net)
        self.decoder = CNPDecoder(decoder_net)

    def get_loss(self, loc, scale, y_t):
        log_prob = MultivariateNormalDiag(loc, scale).log_prob(y_t)
        neg_log_prob = -torch.sum(log_prob, dim=0).mean()
        return neg_log_prob

    def forward(self, x_c, y_c, x_t, y_t=None):
        r_agg = self.encoder(x_c, y_c)
        loc, scale = self.decoder(r_agg, x_t)

        if y_t is not None:
            loss = self.get_loss(loc, scale, y_t)
        else:
            loss = None

        return loc, scale, loss


class CNPModule(NPModule):
    def __init__(self, model_conf, training_conf, data_conf, model, tracker=None):
        super().__init__(model_conf, training_conf, data_conf, model, tracker=tracker)
