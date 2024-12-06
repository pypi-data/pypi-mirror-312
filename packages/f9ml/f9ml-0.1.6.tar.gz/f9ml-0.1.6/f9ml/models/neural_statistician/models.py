import torch
from torch import nn
from torch.autograd import Variable

from f9ml.models.neural_statistician.nets import InferenceNetwork, LatentDecoder, ObservationDecoder, StatisticNetwork
from f9ml.models.neural_statistician.utils import (
    gaussian_log_likelihood,
    kl_diagnormal_diagnormal,
    kl_diagnormal_stdnormal,
)
from f9ml.training.modules import Module


# Model
class Statistician(Module):
    def __init__(
        self,
        batch_size: int = 16,
        sample_size: int = 200,
        n_features: int = 1,
        c_dim: int = 3,
        n_hidden_statistic: int = 3,
        hidden_dim_statistic: int = 128,
        n_stochastic: int = 1,
        z_dim: int = 16,
        n_hidden: int = 3,
        hidden_dim: int = 128,
        activation_function: str = "relu",
        print_vars: bool = False,
        tracker: None | object = None,
        training_conf: dict | None = None,
        model_conf: dict = {"output_dim": None},
        alpha_decay_rate: float = 0.5,
        **kwargs,
    ):
        """Initialize the Statistician model.

        Parameters
        ----------
        batch_size : int, optional
            batch size, by default 16
        sample_size : int, optional
            sample_size, by default 200
        n_features : int, optional
            number of features, by default 1
        c_dim : int, optional
            context dimension, by default 3
        n_hidden_statistic : int, optional
            number of hidden layers for residual network in statistic network (decoder), by default 128
        hidden_dim_statistic : int, optional
            dimension of hidden layers in decoder, by default 3
        n_stochastic : int, optional
            number of stochastic units, by default 1
        z_dim : int, optional
            dimension of latent variable, by default 16
        n_hidden : int, optional
            number of hidden layers in each residual network, by default 3
        hidden_dim : int, optional
            hidden dimension, by default 128
        activation_function : int, optional
            the activation function, by default F.relu
        print_vars : bool, optional
            whether it prints variables, by default False
        tracker : None | object, optional
            tracker class instance, by default None
        training_conf : dict | None, optional
            training configuration, by default None
        model_conf : dict, optional
            model configuration, by default {"output_dim": None}
        """
        super().__init__(model_conf, training_conf, model=None, tracker=tracker)
        # data shape
        self.batch_size = batch_size
        self.sample_size = sample_size
        self.n_features = n_features

        # context
        self.c_dim = c_dim
        self.n_hidden_statistic = n_hidden_statistic
        self.hidden_dim_statistic = hidden_dim_statistic

        # latent
        self.n_stochastic = n_stochastic
        self.z_dim = z_dim
        self.n_hidden = n_hidden
        self.hidden_dim = hidden_dim

        self.nonlinearity = getattr(nn, activation_function)
        self.nonlinearity = self.nonlinearity()

        self.alpha = 1.0
        self.alpha_decay_rate = alpha_decay_rate

        # modules
        # statistic network
        statistic_args = (
            self.batch_size,
            self.sample_size,
            self.n_features,
            self.n_hidden_statistic,
            self.hidden_dim_statistic,
            self.c_dim,
            self.nonlinearity,
        )
        self.statistic_network = StatisticNetwork(*statistic_args)

        z_args = (
            self.batch_size,
            self.sample_size,
            self.n_features,
            self.n_hidden,
            self.hidden_dim,
            self.c_dim,
            self.z_dim,
            self.nonlinearity,
        )
        # inference networks
        # one for each stochastic layer
        self.inference_networks = nn.ModuleList([InferenceNetwork(*z_args) for _ in range(self.n_stochastic)])

        # latent decoders
        # again, one for each stochastic layer
        self.latent_decoders = nn.ModuleList([LatentDecoder(*z_args) for _ in range(self.n_stochastic)])

        # observation decoder
        observation_args = (
            self.batch_size,
            self.sample_size,
            self.n_features,
            self.n_hidden,
            self.hidden_dim,
            self.c_dim,
            self.n_stochastic,
            self.z_dim,
            self.nonlinearity,
        )
        self.observation_decoder = ObservationDecoder(*observation_args)

        # initialize weights
        self.apply(self.weights_init)

        # print variables for sanity check and debugging
        if print_vars:
            for i, pair in enumerate(self.named_parameters()):
                name, param = pair
                print("{} --> {}, {}".format(i + 1, name, param.size()))
            print()

    def forward(self, x):
        # statistic network
        c_mean, c_logvar = self.statistic_network(x)
        c = self.reparameterize_gaussian(c_mean, c_logvar)

        # inference networks
        qz_samples = []
        qz_params = []
        z = None
        for inference_network in self.inference_networks:
            z_mean, z_logvar = inference_network(x, z, c)
            qz_params.append([z_mean, z_logvar])
            z = self.reparameterize_gaussian(z_mean, z_logvar)
            qz_samples.append(z)

        # latent decoders
        pz_params = []
        z = None
        for i, latent_decoder in enumerate(self.latent_decoders):
            z_mean, z_logvar = latent_decoder(z, c)
            pz_params.append([z_mean, z_logvar])
            z = qz_samples[i]

        # observation decoder
        zs = torch.cat(qz_samples, dim=1)
        x_mean, x_logvar = self.observation_decoder(zs, c)

        outputs = ((c_mean, c_logvar), (qz_params, pz_params), (x, x_mean, x_logvar))

        return outputs

    def loss(self, outputs):
        c_outputs, z_outputs, x_outputs = outputs
        weight = self.alpha + 1

        # 1. Reconstruction loss
        x, x_mean, x_logvar = x_outputs
        recon_loss = gaussian_log_likelihood(x.view(-1, self.n_features), x_mean, x_logvar)
        recon_loss /= self.batch_size * self.sample_size

        # 2. KL Divergence terms
        kl = 0

        # a) Context divergence
        c_mean, c_logvar = c_outputs
        kl_c = kl_diagnormal_stdnormal(c_mean, c_logvar)
        kl += kl_c

        # b) Latent divergences
        qz_params, pz_params = z_outputs
        shapes = (
            (self.batch_size, self.sample_size, self.z_dim),
            (self.batch_size, 1, self.z_dim),
        )
        for i in range(self.n_stochastic):
            args = (
                qz_params[i][0].view(shapes[0]),
                qz_params[i][1].view(shapes[0]),
                pz_params[i][0].view(shapes[1] if i == 0 else shapes[0]),
                pz_params[i][1].view(shapes[1] if i == 0 else shapes[0]),
            )
            kl_z = kl_diagnormal_diagnormal(*args)
            if torch.isnan(kl_z).any() or torch.isinf(kl_z).any():
                raise ValueError("KL divergence is NaN or Inf")
            kl += kl_z

        kl /= self.batch_size * self.sample_size

        # Variational lower bound and weighted loss
        vlb = recon_loss - kl
        loss = -((weight * recon_loss) - (kl / weight))

        return loss, vlb

    def step(self, batch, optimizer, clip_gradients=True):
        assert self.training is True

        inputs = Variable(batch.cuda())
        outputs = self.forward(inputs)
        loss, vlb = self.loss(outputs, weight=(self.alpha + 1))

        # perform gradient update
        optimizer.zero_grad()
        loss.backward()
        if clip_gradients:
            for param in self.parameters():
                if param.grad is not None:
                    param.grad.data = param.grad.data.clamp(min=-0.5, max=0.5)
        optimizer.step()

        # output variational lower bound
        try:
            return vlb.data[0]
        except IndexError:
            return vlb.item()

    def on_train_epoch_end(self):
        super().on_train_epoch_end()
        self.alpha *= self.alpha_decay_rate

    def _get_loss(self, batch: torch.Tensor) -> torch.Tensor:
        output = self.forward(batch)
        loss = self.loss(output)
        return loss

    def training_step(self, batch: torch.Tensor, *args) -> torch.Tensor:
        loss = self._get_loss(batch)
        self.log("train_loss", loss[0], batch_size=batch.size()[0])
        return loss[0]

    def validation_step(self, batch: torch.Tensor, *args) -> None:
        loss = self._get_loss(batch)
        self.log("val_loss", loss[0], batch_size=batch.size()[0])

    def test_step(self, batch: torch.Tensor, *args) -> None:
        loss = self._get_loss(batch)
        self.log("test_loss", loss[0], batch_size=batch.size()[0])

    def save(self, optimizer, path: str) -> None:
        torch.save(
            {
                "model_state": self.state_dict(),
                "optimizer_state": optimizer.state_dict(),
            },
            path,
        )

    @staticmethod
    def reparameterize_gaussian(mean: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        std = torch.exp(0.5 * logvar)
        eps = Variable(torch.randn(std.size()).cuda())
        return mean + std * eps

    @staticmethod
    def weights_init(m: nn.Module) -> None:
        if isinstance(m, nn.Linear):
            nn.init.xavier_normal_(m.weight.data, gain=nn.init.calculate_gain("relu"))
            nn.init.constant_(m.bias.data, 0)
        elif isinstance(m, nn.BatchNorm1d):
            pass


if __name__ == "__main__":
    import ml.neural_statistician.neural_statistitian.main as main

    main.main()
