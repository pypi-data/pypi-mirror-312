import matplotlib.pyplot as plt
import numpy as np
import torch
from f9columnar.plotting import handle_plot_exception, make_subplots_grid
from tqdm import tqdm

from f9ml.stats.two_sample_tests import two_sample_plot
from f9ml.training.trackers import Tracker
from f9ml.utils.helpers import iqr_remove_outliers


class FlowTracker(Tracker):
    def __init__(self, experiment_conf, tracker_path, n_samples=10**5, n_bins=50):
        super().__init__(experiment_conf, tracker_path)
        self.n_samples = n_samples

        self.n_bins = n_bins

        self.density = None
        self.generated = None

    def make_plotting_dirs(self):
        return {
            "density": f"{self.base_dir}/density/",
            "generated": f"{self.base_dir}/generated/",
        }

    def get_predictions(self, stage):
        self.stage = stage

        if stage == "val" or stage is None:
            dl = self.module._trainer.datamodule.val_dataloader()
        elif stage == "test":
            dl = self.module._trainer.datamodule.test_dataloader()
        else:
            raise ValueError(f"Stage must be one of ['val', 'test', None], got {stage} instead!")

        self.density, self.reference = [], []
        for b in tqdm(dl, desc="Looping over test dataloader for metrics and plotting", leave=False):
            x, _ = b
            self.density.append(
                self.module.model.estimate_density(x.to(self.module.model.device), exp=False, mean=False)
            )

        self.density = np.concatenate(self.density).flatten()

        self.reference = dl.dataset.X.cpu().numpy()

        self.generated = self.module.model.sample(self.reference.shape[0])

        torch.cuda.empty_cache()

    def compute(self, stage=None):
        return super().compute(stage)

    def plot(self):
        if self.current_epoch % self.experiment_conf["check_metrics_n_epoch"] != 0:
            return False

        self.density_plot()
        self.gen_vs_ref_plot()

        self.module.logger.experiment.log_artifact(local_path=self.base_dir, run_id=self.module.logger.run_id)

        return True

    @handle_plot_exception
    def density_plot(self):
        fig, ax = plt.subplots()

        ax.hist(
            iqr_remove_outliers(self.density, q1_set=5, q3_set=95),
            bins=self.n_bins,
            histtype="step",
            density=False,
            lw=2,
        )
        ax.set_xlabel("log density")
        ax.set_ylabel("counts")

        plt.tight_layout()
        fig.savefig(f"{self.plotting_dirs['density']}log_density_epoch{self.current_epoch:02d}_{self.stage}.png")
        plt.close()

    @handle_plot_exception
    def gen_vs_ref_plot(self):
        x, y = make_subplots_grid(self.generated.shape[1])
        fig, axs = plt.subplots(x, y, figsize=(4 * y, 3 * x))
        axs = axs.flatten()

        axs = two_sample_plot(
            self.reference,
            self.generated,
            axs,
            n_bins=self.n_bins,
            log_scale=False,
            label=["True", "Generated"],
            density=True,
            lw=2,
            bin_range=(-5, 5),
        )

        plt.tight_layout()
        fig.savefig(f"{self.plotting_dirs['generated']}generated_epoch{self.current_epoch:02d}_{self.stage}.png")
        plt.close()


class FlowToyDensityPlotter:
    def __init__(self, model):
        self.model = model

    def _get_2d_density(self, mesh):
        if self.model.training:
            raise ValueError

        z, jac = self.model.flow(torch.from_numpy(mesh).to(self.model.device))
        sum_jac = sum(jac)
        base = self.model.base_distribution.log_prob(z).sum(dim=-1, keepdim=True)
        log_density = (base + sum_jac).cpu().numpy()

        return np.exp(log_density.flatten())

    @staticmethod
    def _make_2d_mesh(xmin, xmax, mesh_points):
        points = 2 * [np.linspace(xmin, xmax, mesh_points, dtype=np.float32)]
        mesh = np.array(np.meshgrid(*points)).T.reshape(-1, 2)
        return mesh

    @staticmethod
    def _plot_2d_density_helper(xmin, xmax, prob, mesh_points, axs=None, fig=None, colorbar=True):
        if axs is None and fig is None:
            fig, axs = plt.subplots(1, 1)

        im = axs.imshow(prob.reshape(mesh_points, mesh_points).T, origin="lower")

        axs.set_xticks([0, int(mesh_points * 0.25), int(mesh_points * 0.5), int(mesh_points * 0.75), mesh_points])
        axs.set_xticklabels([xmin, int(xmin / 2), 0, int(xmax / 2), xmax])
        axs.set_yticks([0, int(mesh_points * 0.25), int(mesh_points * 0.5), int(mesh_points * 0.75), mesh_points])
        axs.set_yticklabels([xmin, int(xmin / 2), 0, int(xmax / 2), xmax])

        if colorbar:
            fig.colorbar(im, orientation="vertical")

        return fig, axs

    @handle_plot_exception
    def plot_2d_density(self, model, xmin=-4, xmax=4, mesh_points=200, axs=None, fig=None, colorbar=True, save=False):
        mesh = self._make_2d_mesh(xmin, xmax, mesh_points)
        prob = self._get_2d_density(model, mesh)

        fig, axs = self._plot_2d_density_helper(xmin, xmax, prob, mesh_points, axs, fig, colorbar)

        if save:
            fig.tight_layout()
            plt.savefig(save)
            plt.close(fig)

        return prob, mesh, fig, axs
