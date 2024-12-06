import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
from f9columnar.plotting import handle_plot_exception
from sklearn.preprocessing import LabelEncoder
from torchmetrics.classification import MulticlassAUROC, MulticlassConfusionMatrix, MulticlassROC
from tqdm import tqdm

from f9ml.models.neural_statistician.utils import kl_diagnormal_diagnormal
from f9ml.training.trackers import Tracker


class NSTracker(Tracker):
    """Neural statistician tracker class."""

    def __init__(
        self, experiment_conf: dict, tracker_path: str, y_labels: list[str] | None = None, classify: bool = False
    ):
        """Initializes the Neural Statistitian Tracker.

        Parameters
        ----------
        experiment_conf : dict
            Dictionary with experiment configuration.
        tracker_path : str
            Path to the tracker.
        y_labels : list[str] | None, optional
            If y_labels are just numbers, you can provide their names, by default None
        classify : bool, optional
            whether to run also a few-shot classification, by default False
        """
        super().__init__(experiment_conf, tracker_path)

        if y_labels is None:
            self.y_labels = ["psh", "pttbar", "pWjets", "pStop"]  # correct order from selection
            logging.warning(f"y_labels not provided, using default values: {self.y_labels}")
        else:
            self.y_labels = y_labels
        if isinstance(self.experiment_conf.get("classify"), bool):
            self.classify = self.experiment_conf["classify"]
        else:
            self.classify = classify

    def make_plotting_dirs(self) -> dict[str, str]:
        out = {"scatter": f"{self.base_dir}/scatter/"}
        if self.classify:
            out["confmats"] = f"{self.base_dir}/confmat/"
            out["rocs"] = f"{self.base_dir}/rocs/"
        return out

    def get_predictions(self, stage: str | None) -> None:
        # load test data and make model predictions
        self.stage = stage

        if stage == "val" or stage is None:
            dl = self.module._trainer.datamodule.val_dataloader()
        elif stage == "test":
            dl = self.module._trainer.datamodule.test_dataloader()
        else:
            raise ValueError(f"Stage must be one of ['val', 'test', None], got {stage} instead!")

        self.contexts = []
        self.contexts_var = []
        all_test = []
        for b in tqdm(dl, desc="Looping over test dataloader for metrics and plotting", leave=False):
            batch = b.cuda()
            # softmax normalisation
            c_mean, c_var = self.module.statistic_network.forward(batch)
            self.contexts.append(c_mean.detach().cpu().numpy())
            if self.classify:
                self.contexts_var.append(c_var.detach().cpu().numpy())
                all_test.append(batch.detach().cpu().numpy())

        # TODO: add a list of distributions to the test dataset
        list_of_distributions = self.module._trainer.datamodule.distributions
        idx = self.module._trainer.datamodule.test_idx if stage == "test" else self.module._trainer.datamodule.val_idx
        self.distributions_list = list_of_distributions[idx]

        if self.classify:
            self.prepare_test_data_for_classification(all_test)
            self.classify_test_data()

    def prepare_test_data_for_classification(self, all_test):
        """
        Prepares test data for classification by processing and transforming the input data.

        Args:
            all_test (list of np.ndarray): A list of numpy arrays containing test data.

        Returns:
            None

        This method performs the following steps:
        1. Concatenates all test data arrays along the first axis.
        2. Identifies unique datasets based on the `distributions_list` attribute.
        3. Extracts unique datasets and other test data.
        4. Computes the mean and log variance of the unique datasets using the `statistic_network`.
        5. Repeats the labels to match the shape of the test data.
        6. Reshapes the other test data for processing.
        7. Computes the mean and log variance of the reshaped test data using the `statistic_network`.
        8. Ensures the shapes of the computed means, log variances, and labels are consistent.
        9. Randomly permutes the computed means, log variances, and labels.
        10. Converts the permuted labels to numpy arrays and stores them.

        Note:
            This method modifies the following attributes of the class:
            - `unique_datasets`
            - `labels`
            - `dists_mean`
            - `dists_logvar`
            - `class_mean`
            - `class_logvar`
        """
        # 1. Concatenate all test data arrays along the first axis
        all_test = np.concatenate(all_test, axis=0)
        # 2. Identify unique datasets based on the `distributions_list` attribute
        _, unique_indices = np.unique(self.distributions_list, return_index=True)
        # 3. Extract unique datasets and other test data
        self.unique_datasets = all_test[unique_indices]
        other_test = all_test[np.setdiff1d(np.arange(all_test.shape[0]), unique_indices)]
        self.labels = self.distributions_list[np.setdiff1d(np.arange(all_test.shape[0]), unique_indices)]
        # 4. Compute the mean and log variance of the unique datasets using the `statistic_network`
        self.dists_mean, self.dists_logvar = self.module.statistic_network.forward(
            torch.tensor(self.unique_datasets).cuda()
        )
        # 5. Repeat the labels to match the shape of the test data
        self.labels = np.repeat(self.labels, all_test.shape[1])
        # 6. Reshape the other test data for processing
        t_sh = other_test.shape
        other_test = other_test.reshape(t_sh[0] * t_sh[1], 1, t_sh[-1])
        # 7. Compute the mean and log variance of the reshaped test data using the `statistic_network`
        self.class_mean, self.class_logvar = self.module.statistic_network.forward(torch.tensor(other_test).cuda())
        # 8. Ensure the shapes of the computed means, log variances, and labels are consistent
        assert self.class_mean.shape[0] == self.labels.shape[0] == self.class_logvar.shape[0]
        # 9. Randomly permute the computed means, log variances, and labels
        p = np.random.permutation(self.labels.shape[0])
        self.class_mean, self.class_logvar, self.labels = (
            self.class_mean[p],
            self.class_logvar[p],
            self.labels[p],
        )
        # 10. Convert the permuted labels to numpy arrays and store them
        label_encoder = LabelEncoder()
        numerical_labels = label_encoder.fit_transform(self.labels)
        self.labels = torch.from_numpy(numerical_labels).to(torch.long)
        # self.labels = torch.from_numpy(self.labels)

    def classify_test_data(self) -> None:
        """
        Classifies the test data using the computed means and log variances of the unique datasets and other test data.
        """
        dkls = []
        for d_mean, d_logvar in zip(self.dists_mean, self.dists_logvar):
            dkls.append(kl_diagnormal_diagnormal(d_mean, d_logvar, self.class_mean, self.class_logvar, sum=False))
        self.predictions = torch.stack(dkls, dim=1).detach().cpu()

    def compute(self, stage: str | None) -> bool:
        """Computes metrics and stores them.

        Parameters
        ----------
        stage : str | None
            Stage of the experiment.

        Returns
        -------
        bool
            True if metrics are computed, False otherwise.
        """
        self.stage, self.current_epoch = stage, self.module.current_epoch

        if self.current_epoch == 0:
            self.on_first_epoch()

        # check if metrics should be calculated this epoch
        if self.metric_evaluation_condition():
            logging.debug(f"Skipping metrics computation for epoch {self.current_epoch}")
            return False

        # get predictions, needs to be implemented
        self.get_predictions(stage)

        return True

    def plot(self) -> bool:
        """Calculates some metrics and plots them."""

        if self.metric_evaluation_condition():
            return False

        self.plot_scatter()
        if self.classify:
            self.confusion_matrix()
            self.roc()

        if self.stage == "test":
            results_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results.txt")
            with open(results_path, "a") as f:
                out = f"{self.experiment_conf['run_name'][:16]:<16}"
                for i in np.concatenate((self.confmat_diag, self.aucs)):
                    out += f"{i:<8.3f}"
                f.write(out + "\n")

        self.module.logger.experiment.log_artifact(local_path=self.base_dir, run_id=self.module.logger.run_id)

        return True

    @handle_plot_exception
    def plot_scatter(self) -> None:
        """Draws a scatter plot of context variables."""
        c_dim = self.contexts[0].shape[1]
        fig = plt.figure()

        colors = ["indianred", "forestgreen", "gold", "cornflowerblue", "darkviolet", "black", "pink"]
        contexts = np.array(self.contexts).reshape(-1, c_dim)
        ax = fig.add_subplot(111, projection="3d" if c_dim >= 3 else None)
        n = len(contexts)
        self.distributions_list = self.distributions_list[:n]
        labels = list(set(self.distributions_list))
        ix = [np.where(self.distributions_list == label) for label in labels]
        assert len(labels) <= len(colors), "Too many labels for the number of colors! Provide more colors."
        if np.all(np.array(labels) == np.arange(len(labels))):
            labels = self.y_labels
        for label, i in enumerate(ix):
            ax.scatter(
                *[contexts[i][:, j] for j in range(min(c_dim, 3))],
                label=labels[label].title(),
                color=colors[label],
            )
        plt.tick_params(
            axis="both",
            which="both",
            bottom="off",
            top="off",
            labelbottom="off",
            right="off",
            left="off",
            labelleft="off",
        )
        if c_dim == 3:
            ax.set_zlim((-3, 3))
        if c_dim <= 3:
            plt.xlim((-3.5, 3))
            plt.ylim((-3, 3))
        plt.legend(loc="upper left")
        plt.tight_layout()

        fig.savefig(f"{self.plotting_dirs['scatter']}confmat_epoch{self.current_epoch:02d}_{self.stage}.pdf")
        plt.close()

    def confusion_matrix(self) -> None:
        """Calculates the confusion matrix and plots it."""

        confmat = MulticlassConfusionMatrix(num_classes=self.dists_mean.shape[0])
        confmat.update(-self.predictions, self.labels)
        conf_counts: np.ndarray = confmat.compute().numpy()
        conf = conf_counts / np.sum(conf_counts, axis=1, keepdims=True)

        # save the matrix as text file
        np.savetxt(
            f"{self.plotting_dirs['confmats']}confmat_epoch{self.current_epoch:02d}_{self.stage}.txt",
            conf_counts,
            fmt="%10.0f",
        )
        self.confmat_diag = np.diag(conf)

        # confusion matrix
        fig, axs = plt.subplots(figsize=(8, 6))
        # labels = ["psh", "pttbar", "pWjets", "pStop"]
        labels = list(set(self.distributions_list))

        sns.heatmap(
            conf,
            annot=True,
            fmt=".3f",
            cmap="viridis",
            xticklabels=[labels[i] for i in range(len(labels))],
            yticklabels=[labels[i] for i in range(len(labels))],
        )
        plt.ylabel("Actual")
        plt.xlabel("Predicted")
        self.module.logger.experiment.log_figure(
            self.module.logger.run_id,
            fig,
            f"{self.plotting_dirs['confmats']}confmat_epoch{self.current_epoch:02d}_{self.stage}.png",
        )
        # save the plot
        fig.savefig(f"{self.plotting_dirs['confmats']}confmat_epoch{self.current_epoch:02d}_{self.stage}.pdf")
        plt.close()

    @handle_plot_exception
    def roc(self) -> None:
        """Plots one ROC - receiver operating characteristic."""
        fig, ax = plt.subplots()

        # calculate false positive rate and true positive rate
        roc_multi = MulticlassROC(num_classes=self.dists_mean.shape[0])
        roc_multi.update(-self.predictions, self.labels)

        auc = MulticlassAUROC(num_classes=self.dists_mean.shape[0], average="none")
        self.aucs = auc(-self.predictions, self.labels).numpy()
        np.savetxt(
            f"{self.plotting_dirs['rocs']}auc_epoch{self.current_epoch:02d}_{self.stage}.txt",
            self.aucs,
            fmt="%5.3f",
        )

        fig, ax = roc_multi.plot(score=True, labels=self.y_labels)
        self.module.logger.experiment.log_figure(
            self.module.logger.run_id,
            fig,
            f"{self.plotting_dirs['rocs']}roc_epoch{self.current_epoch:02d}_{self.stage}.png",
        )
        fig.savefig(f"{self.plotting_dirs['rocs']}roc_epoch{self.current_epoch:02d}_{self.stage}.pdf")
        plt.close()

    def metric_evaluation_condition(self) -> bool:
        return (self.current_epoch + 1) % self.experiment_conf["check_eval_n_epoch"] != 0 and self.stage != "test"


if __name__ == "__main__":
    import ml.neural_statistician.neural_statistitian.main_delcki as main

    main.main()
