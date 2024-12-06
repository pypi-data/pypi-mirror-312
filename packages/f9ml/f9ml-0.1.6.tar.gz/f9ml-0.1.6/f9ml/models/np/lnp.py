import torch
import torch.nn as nn
from torch.distributions.kl import kl_divergence
from torch.nn import functional as F

from f9ml.models.np.base_np import BaseNeuralProcess, MultivariateNormalDiag, NPModule
from f9ml.models.np.cnp import CNPEncoder


class LNPLatentEncoder(nn.Module):
    def __init__(self, encoder_net, eps=1e-3):
        super().__init__()
        self.encoder_net = encoder_net
        self.eps = eps

    def forward(self, r):
        # r = B x 1 x R

        r = r.squeeze(1)  # B x R
        z = self.encoder_net(r)  # B x 2Z
        mu_z, log_var_z = torch.chunk(z, 2, dim=-1)  # B x Z

        return mu_z, self.eps + (1 - self.eps) * F.softplus(log_var_z)


class LNPDecoder(nn.Module):
    def __init__(self, decoder_net, eps=1e-3):
        super().__init__()
        self.decoder_net = decoder_net
        self.eps = eps

    def forward(self, z_samples, x_t):
        # z_samples = S x B x C x R, x_t = B x C x D

        x_t = x_t.unsqueeze(0)  # 1 x B x C x D
        x_t = x_t.expand(z_samples.shape[0], *x_t.shape)  # S x 1 x B x C x D
        x_t = x_t.squeeze(1)  # S x B x C x D

        x = torch.cat([z_samples, x_t], dim=-1)  # S x B x C x (R + D)
        x = x.view(x.shape[0] * x.shape[1] * x.shape[2], -1)  # S * B * C x (R + D)

        x = self.decoder_net(x)  # S * B * C x 2D
        x = x.view(*x_t.shape[:-1], -1)  # S x B x C x 2 * D

        mu_t, log_var_t = torch.chunk(x, 2, dim=-1)  # S x B x C x D

        return mu_t, self.eps + (1 - self.eps) * F.softplus(log_var_t)


class LNP(BaseNeuralProcess):
    def __init__(self, model_conf, data_conf, experiment_conf):
        """Latent Neural Process (LNP) model.

        References
        ----------
        [1] - https://arxiv.org/abs/1807.01622
        [2] - https://github.com/YannDubs/Neural-Process-Family
        [3] - https://pytorch.org/docs/stable/distributions.html#pathwise-derivative

        """
        super().__init__(model_conf, data_conf, experiment_conf)

        self.z_dim = model_conf["z_dim"]
        self.n_z_samples = model_conf["n_z_samples"]
        self.loss_type = model_conf["loss_type"].lower()

        assert self.loss_type in ["npml", "npvi"]

        r_encoder_net = self.create_mlp([self.input_dim] + self.model_conf["r_encoder_layers"] + [self.r_dim])
        z_encoder_net = self.create_mlp([self.r_dim] + self.model_conf["z_encoder_layers"] + [2 * self.z_dim])
        decoder_net = self.create_mlp(
            [self.r_dim + self.input_dim] + self.model_conf["decoder_layers"] + [2 * self.input_dim]
        )

        self.r_encoder = CNPEncoder(r_encoder_net)
        self.z_encoder = LNPLatentEncoder(z_encoder_net)
        self.decoder = LNPDecoder(decoder_net)

        self.z_reshaper = nn.Linear(self.z_dim, self.r_dim)

    def get_loss(self, latent_c_dist, latent_t_dist, pred_dist, y_t, z_samples=None):
        # z_samples = S x B x Z, y_t = B x C x D

        if self.loss_type == "npvi":
            # see original article [1]
            log_prob_pred = pred_dist.log_prob(y_t)  # S x B x C
            sum_log_prob_pred = torch.sum(log_prob_pred, dim=-1)  # S x B
            E_sum_log_prob_pred = torch.mean(sum_log_prob_pred, dim=0)  # B

            kl = kl_divergence(latent_t_dist, latent_c_dist)  # B

            loss = -(E_sum_log_prob_pred - kl)
            loss = loss.mean()  # 1
        else:
            # see losses.py in [2] for an explanation

            # S x B x 1 x Z -> S x B x C x Z -> S x C x B x Z
            z_samples = z_samples.unsqueeze(2)
            z_samples = z_samples.expand(self.n_z_samples, z_samples.shape[1], y_t.shape[1], self.z_dim)
            z_samples = z_samples.permute(0, 2, 1, 3)

            # sum over context points
            log_prob_pred = pred_dist.log_prob(y_t)  # S x B x C
            sum_log_prob_pred = torch.sum(log_prob_pred, dim=-1)  # S x B

            log_prob_c = latent_c_dist.log_prob(z_samples)  # S x C x B
            sum_log_prob_c = torch.sum(log_prob_c, dim=1)  # S x B

            log_prob_t = latent_t_dist.log_prob(z_samples)  # S x C x B
            sum_log_prob_t = torch.sum(log_prob_t, dim=1)  # S x B

            # importance sampling
            sum_log = sum_log_prob_pred + sum_log_prob_c - sum_log_prob_t

            # sum over latent samples
            logsumexp_trick = torch.logsumexp(sum_log, dim=0) - torch.log(torch.tensor(self.n_z_samples).float())  # B
            loss = -logsumexp_trick
            loss = loss.mean()  # 1

        return loss

    def forward(self, x_c, y_c, x_t, y_t=None):
        # note for [2]: p_yCc = pred_dist, q_zCc = latent_c_dist, q_zCct = latent_t_dist

        r = self.r_encoder(x_c, y_c)  # B x 1 x R

        mu_c_z, std_c_z = self.z_encoder(r)  # B x Z
        latent_c_dist = MultivariateNormalDiag(mu_c_z, std_c_z)  # p(z|C)

        if y_t is not None:
            # because we do not have y_t at test time
            r_t = self.r_encoder(x_t, y_t)  # B x 1 x R
            mu_t_z, std_t_z = self.z_encoder(r_t)  # B x Z
            latent_t_dist = MultivariateNormalDiag(mu_t_z, std_t_z)  # p(z|C, T) ~ q(z|D)
            sampling_dist = latent_t_dist
        else:
            latent_t_dist = None
            sampling_dist = latent_c_dist

        # reparemeterization trick
        z_samples_sampled = sampling_dist.rsample([self.n_z_samples])  # S x B x Z

        # x_t = B x C x D
        z_samples = self.z_reshaper(z_samples_sampled)  # S x B x R
        z_samples = z_samples.unsqueeze(2)  # S x B x 1 x R
        z_samples = z_samples.expand(self.n_z_samples, z_samples.shape[1], x_t.shape[1], self.r_dim)  # S x B x C x R

        loc, scale = self.decoder(z_samples, x_t)  # S x B x C x D
        pred_dist = MultivariateNormalDiag(loc, scale)  # p(y|C, T)

        if y_t is not None:
            loss = self.get_loss(latent_c_dist, latent_t_dist, pred_dist, y_t, z_samples_sampled)
        else:
            loss = None

        loc, scale = loc.mean(dim=0), scale.mean(dim=0)

        return loc, scale, loss


class LNPModule(NPModule):
    def __init__(self, model_conf, training_conf, data_conf, model, tracker=None):
        super().__init__(model_conf, training_conf, data_conf, model, tracker=tracker)
