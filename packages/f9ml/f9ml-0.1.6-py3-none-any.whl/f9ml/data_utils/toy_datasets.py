import matplotlib.pyplot as plt
import numpy as np
import sklearn.datasets
import torch
from sklearn.utils import shuffle as util_shuffle
from torch.utils.data import Dataset

from f9ml.data_utils.legacy_data_modules import DataModule


class DensityToys:
    density_toys = [
        "swissroll",
        "circles",
        "rings",
        "moons",
        "4gaussians",
        "8gaussians",
        "pinwheel",
        "2spirals",
        "checkerboard",
        "line",
        "cos",
        "fmf_normal",
        "fmf_uniform",
        "simple_regression",
    ]

    def __init__(self, data_name, data_size, seed=None):
        if data_name not in self.density_toys:
            raise ValueError(f"Data name {data_name} not in {self.density_toys}")
        else:
            self.data_name = data_name

        self.data_size = data_size
        self.random_state = np.random.RandomState(seed)

    def __call__(self, **kwargs):
        if self.data_name == "swissroll":
            return self.swissroll()
        elif self.data_name == "circles":
            return self.circles()
        elif self.data_name == "rings":
            return self.rings()
        elif self.data_name == "moons":
            return self.moons()
        elif self.data_name == "4gaussians":
            return self.gaussians4()
        elif self.data_name == "8gaussians":
            return self.gaussians8()
        elif self.data_name == "pinwheel":
            return self.pinwheel()
        elif self.data_name == "2spirals":
            return self.spirals()
        elif self.data_name == "checkerboard":
            return self.checkerboard()
        elif self.data_name == "line":
            return self.line()
        elif self.data_name == "cos":
            return self.cos()
        elif self.data_name == "fmf_uniform":
            return self.fmf_uniform()
        elif self.data_name == "fmf_normal":
            return self.fmf_normal()
        elif self.data_name == "simple_regression":
            return self.simple_regression(**kwargs)
        else:
            raise NameError

    def swissroll(self):
        dataset = sklearn.datasets.make_swiss_roll(n_samples=self.data_size, noise=1.0)[0]
        dataset = dataset.astype("float32")[:, [0, 2]]
        dataset /= 5
        return dataset

    def circles(self):
        dataset = sklearn.datasets.make_circles(n_samples=self.data_size, factor=0.5, noise=0.08)[0]
        dataset = dataset.astype("float32")
        dataset *= 3
        return dataset

    def rings(self):
        n_samples4 = n_samples3 = n_samples2 = self.data_size // 4
        n_samples1 = self.data_size - n_samples4 - n_samples3 - n_samples2

        linspace4 = np.linspace(0, 2 * np.pi, n_samples4, endpoint=False)
        linspace3 = np.linspace(0, 2 * np.pi, n_samples3, endpoint=False)
        linspace2 = np.linspace(0, 2 * np.pi, n_samples2, endpoint=False)
        linspace1 = np.linspace(0, 2 * np.pi, n_samples1, endpoint=False)

        circ4_x = np.cos(linspace4)
        circ4_y = np.sin(linspace4)
        circ3_x = np.cos(linspace4) * 0.75
        circ3_y = np.sin(linspace3) * 0.75
        circ2_x = np.cos(linspace2) * 0.5
        circ2_y = np.sin(linspace2) * 0.5
        circ1_x = np.cos(linspace1) * 0.25
        circ1_y = np.sin(linspace1) * 0.25

        dataset = (
            np.vstack(
                [np.hstack([circ4_x, circ3_x, circ2_x, circ1_x]), np.hstack([circ4_y, circ3_y, circ2_y, circ1_y])]
            ).T
            * 3.0
        )
        dataset = util_shuffle(dataset, random_state=self.random_state)

        dataset = dataset + self.random_state.normal(scale=0.08, size=dataset.shape)

        return dataset.astype("float32")

    def moons(self):
        dataset = sklearn.datasets.make_moons(n_samples=self.data_size, noise=0.1)[0]
        dataset = dataset.astype("float32")
        dataset = dataset * 2 + np.array([-1, -0.2], dtype="float32")
        return dataset

    def gaussians4(self):
        scale = 4.0
        centers = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        centers = [(scale * x, scale * y) for x, y in centers]

        dataset = []
        for _ in range(self.data_size):
            point = self.random_state.randn(2) * 0.5
            idx = self.random_state.randint(4)
            center = centers[idx]
            point[0] += center[0]
            point[1] += center[1]
            dataset.append(point)

        dataset = np.array(dataset, dtype="float32")
        dataset /= 1.414

        return dataset

    def gaussians8(self):
        scale = 4.0
        centers = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1.0 / np.sqrt(2), 1.0 / np.sqrt(2)),
            (1.0 / np.sqrt(2), -1.0 / np.sqrt(2)),
            (-1.0 / np.sqrt(2), 1.0 / np.sqrt(2)),
            (-1.0 / np.sqrt(2), -1.0 / np.sqrt(2)),
        ]
        centers = [(scale * x, scale * y) for x, y in centers]

        dataset = []
        for i in range(self.data_size):
            point = self.random_state.randn(2) * 0.5
            idx = self.random_state.randint(8)
            center = centers[idx]
            point[0] += center[0]
            point[1] += center[1]
            dataset.append(point)

        dataset = np.array(dataset, dtype="float32")
        dataset /= 1.414

        return dataset

    def pinwheel(self):
        radial_std = 0.3
        tangential_std = 0.1
        num_classes = 5
        num_per_class = self.data_size // 5
        rate = 0.25
        rads = np.linspace(0, 2 * np.pi, num_classes, endpoint=False)

        features = self.random_state.randn(num_classes * num_per_class, 2) * np.array([radial_std, tangential_std])
        features[:, 0] += 1.0
        labels = np.repeat(np.arange(num_classes), num_per_class)

        angles = rads[labels] + rate * np.exp(features[:, 0])
        rotations = np.stack([np.cos(angles), -np.sin(angles), np.sin(angles), np.cos(angles)])
        rotations = np.reshape(rotations.T, (-1, 2, 2))
        dataset = 2 * self.random_state.permutation(np.einsum("ti,tij->tj", features, rotations))
        return dataset.astype(np.float32)

    def spirals(self):
        n = np.sqrt(np.random.rand(self.data_size // 2, 1)) * 540 * (2 * np.pi) / 360
        d1x = -np.cos(n) * n + np.random.rand(self.data_size // 2, 1) * 0.5
        d1y = np.sin(n) * n + np.random.rand(self.data_size // 2, 1) * 0.5
        dataset = np.vstack((np.hstack((d1x, d1y)), np.hstack((-d1x, -d1y)))) / 3
        dataset += np.random.randn(*dataset.shape) * 0.1
        return np.array(dataset, dtype="float32")

    def checkerboard(self):
        x1 = np.random.rand(self.data_size) * 4 - 2
        x2_ = np.random.rand(self.data_size) - np.random.randint(0, 2, self.data_size) * 2
        x2 = x2_ + (np.floor(x1) % 2)
        dataset = np.concatenate([x1[:, None], x2[:, None]], 1) * 2
        return np.array(dataset, dtype="float32")

    def line(self):
        x = self.random_state.rand(self.data_size) * 5 - 2.5
        y = x
        dataset = np.stack((x, y), 1)
        return dataset

    def cos(self):
        x = self.random_state.rand(self.data_size) * 5 - 2.5
        y = np.sin(x) * 2.5
        dataset = np.stack((x, y), 1)
        return dataset

    def fmf_uniform(self):
        n = self.data_size // 34
        # F
        fmf1 = self._get_block(0, 5, n)

        fmf2 = self._get_block(2, 0, n)
        fmf2[:, 0] += 1
        fmf2[:, 1] += 4

        fmf3 = self._get_block(2, 0, n)
        fmf3[:, 0] += 1
        fmf3[:, 1] += 2

        # M
        fmf4 = self._get_block(0, 4, n)
        fmf4[:, 0] += 4

        fmf5 = self._get_block(5, 0, n)
        fmf5[:, 0] += 4
        fmf5[:, 1] += 4

        fmf6 = self._get_block(0, 4, n)
        fmf6[:, 0] += 8

        fmf7 = self._get_block(0, 4, n)
        fmf7[:, 0] += 6

        # F
        fmf8 = self._get_block(0, 5, n)
        fmf8[:, 0] += 10

        fmf9 = self._get_block(2, 0, n)
        fmf9[:, 0] += 1 + 10
        fmf9[:, 1] += 4

        fmf10 = self._get_block(2, 0, n)
        fmf10[:, 0] += 1 + 10
        fmf10[:, 1] += 2

        fmf_lst = [fmf1, fmf2, fmf3, fmf4, fmf5, fmf6, fmf7, fmf8, fmf9, fmf10]
        fmf_arr = np.concatenate(fmf_lst)

        fmf_arr[:, 0] -= 6.5
        fmf_arr[:, 1] -= 2.5
        fmf_arr[:, 0] *= 0.65
        fmf_arr[:, 1] *= 1.65

        return fmf_arr.astype(np.float32)

    def fmf_normal(self):
        n = 10
        n_rng = self.data_size // 400
        sigma_x, sigma_y = 0.4, 0.4

        f1 = self._random_line(n * 5, n_rng, mn=0, mx=5, sigma_x=sigma_x, sigma_y=sigma_y, line="vertical")
        f2 = self._random_line(n * 3, n_rng, mn=0, mx=3, sigma_x=sigma_x, sigma_y=sigma_y, line="horizontal", shift=5)
        f3 = self._random_line(n * 2, n_rng, mn=0, mx=2, sigma_x=sigma_x, sigma_y=sigma_y, line="horizontal", shift=3)

        f = np.concatenate((f1, f2, f3))

        m1 = self._random_line(n * 5, n_rng, mn=0, mx=5, sigma_x=sigma_x, sigma_y=sigma_y, line="vertical", shift=4)
        m2 = self._random_line(n * 5, n_rng, mn=4, mx=8, sigma_x=sigma_x, sigma_y=sigma_y, line="horizontal", shift=5)
        m3 = self._random_line(n * 5, n_rng, mn=0, mx=5, sigma_x=sigma_x, sigma_y=sigma_y, line="vertical", shift=6)
        m4 = self._random_line(n * 5, n_rng, mn=0, mx=5, sigma_x=sigma_x, sigma_y=sigma_y, line="vertical", shift=8)

        fm = np.concatenate((f, m1, m2, m3, m4))

        f21 = self._random_line(n * 5, n_rng, mn=0, mx=5, sigma_x=sigma_x, sigma_y=sigma_y, line="vertical", shift=10)
        f22 = self._random_line(
            n * 3, n_rng, mn=10, mx=13, sigma_x=sigma_x, sigma_y=sigma_y, line="horizontal", shift=5
        )
        f23 = self._random_line(
            n * 2, n_rng, mn=10, mx=12, sigma_x=sigma_x, sigma_y=sigma_y, line="horizontal", shift=3
        )

        fmf = np.concatenate((fm, f21, f22, f23)) * 0.5
        fmf[:, 0] = fmf[:, 0] - 3
        fmf[:, 1] = fmf[:, 1] - 1.3

        return fmf.astype(np.float32)

    def simple_regression(self, dim=1):
        all_x_lst, all_y_lst = [], []

        for _ in range(dim):
            all_x = np.arange(-5, 5, 10 / self.data_size).reshape(-1, 1).astype(np.float32)
            all_y = np.exp(np.cos(all_x)) ** 3 * 2 * np.sin(all_x) - np.sin(all_x) * np.cos(all_x)
            all_x_lst.append(all_x)
            all_y_lst.append(all_y)

        all_x_cat = np.concatenate(all_x_lst, axis=-1)
        all_y_cat = np.concatenate(all_y_lst, axis=-1)

        all_y_cat = all_y_cat / np.abs(np.max(all_y_cat))

        return np.concatenate([all_x_cat, all_y_cat], axis=-1)

    @staticmethod
    def _random_line(n, n_rng, mn=-4, mx=4, sigma_x=1, sigma_y=1, line="vertical", shift=0):
        n = int(n)
        if line == "vertical":
            xs, ys = np.ones(n) * shift, np.linspace(mn, mx, n)
        elif line == "horizontal":
            xs, ys = np.linspace(mn, mx, n), np.ones(n) * shift
        else:
            raise ValueError

        pts_x, pts_y = np.zeros((n, n_rng)), np.zeros((n, n_rng))

        for i, (x, y) in enumerate(zip(xs, ys)):
            x_rng = np.random.normal(x, sigma_x, size=n_rng)
            y_rng = np.random.normal(y, sigma_y, size=n_rng)

            pts_x[i, :] = x_rng
            pts_y[i, :] = y_rng

        pts_x, pts_y = pts_x.flatten(), pts_y.flatten()
        return np.concatenate((pts_x[:, None], pts_y[:, None]), axis=1)

    @staticmethod
    def _get_block(nx, ny, n):
        blocks = []
        block_f = lambda n: np.random.uniform(0, 1, size=(n, 2))

        for x in range(nx):
            block = block_f(n)
            block[:, 0] += x
            blocks.append(block)

        for y in range(ny):
            block = block_f(n)
            block[:, 1] += y
            blocks.append(block)

        return np.concatenate(blocks)


def plot_all_toys(n_data=1000, save=False):
    fig, axs = plt.subplots(4, 4, figsize=(12, 12))
    axs = axs.flatten()

    density_toys = [
        "swissroll",
        "circles",
        "rings",
        "moons",
        "4gaussians",
        "8gaussians",
        "pinwheel",
        "2spirals",
        "checkerboard",
        "line",
        "cos",
        "fmf_normal",
        "fmf_uniform",
        "simple_regression",
    ]

    for i, name in enumerate(density_toys):
        z = DensityToys(name, n_data)()

        axs[i].set_title(name)
        axs[i].hexbin(z[:, 0], z[:, 1])

    if save:
        fig.tight_layout()
        plt.savefig("docs/density_toys.png", dpi=300)
        plt.close(fig)


class ToyDataset(Dataset):
    def __init__(self, data, predict_idx=None):
        if not torch.is_tensor(data):
            data = torch.from_numpy(data).to(torch.float32)

        self.predict_idx = predict_idx

        if predict_idx is not None:
            predict_mask = torch.ones_like(data).to(torch.bool)
            predict_mask[:, predict_idx] = False
            self.data = data[predict_mask]
            self.y = data[~predict_mask]
        else:
            self.data = data
            self.y = None

        if len(self.data.shape) == 1:
            self.data = self.data.unsqueeze(1)

            if self.y is not None:
                self.y = self.y.unsqueeze(1)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if self.predict_idx is not None:
            return self.data[idx], self.y[idx]
        else:
            return self.data[idx]


class ToyDataModule(DataModule):
    def __init__(
        self,
        data_name,
        data_size,
        seed=None,
        predict_idx=None,
        train_split=0.7,
        val_split=0.2,
        **dataloader_kwargs,
    ):
        super().__init__(
            processor=None, dataset_class=ToyDataset, train_split=train_split, val_split=val_split, **dataloader_kwargs
        )
        self.data_name = data_name
        self.data_size = data_size
        self.seed = seed
        self.predict_idx = predict_idx

    def setup(self, stage=None):
        data = DensityToys(self.data_name, self.data_size, self.seed)()

        self._get_splits(len(data))

        if stage == "fit" or stage is None:
            self.train = self.dataset(data[self.train_idx], self.predict_idx)
            self.val = self.dataset(data[self.val_idx], self.predict_idx)
        if stage == "test":
            self.test = self.dataset(data[self.test_idx], self.predict_idx)


if __name__ == "__main__":
    plot_all_toys(save=True)
