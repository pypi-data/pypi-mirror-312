import logging
import os
from abc import ABC, abstractmethod


class Tracker(ABC):
    def __init__(self, experiment_conf, tracker_path):
        self.experiment_conf = experiment_conf
        self.tracker_path = tracker_path

        self.module = None

        self.current_epoch = None  # current epoch number
        self.plotting_dirs = None  # directories for saving plots
        self.stage = None  # set in get_predictions

        self.base_dir = f"{self.tracker_path}/{self.experiment_conf['run_name']}/"
        logging.debug(f"Tracker base directory: {self.base_dir}")

    def __call__(self, module):
        self.module = module
        return self

    def on_first_epoch(self):
        """Create directories if they don't exist yet, should be called after the first epoch in compute method."""
        self.create_dirs()

    def create_dirs(self):
        """Creates the directories where the plots will be saved."""
        self.plotting_dirs = self.make_plotting_dirs()

        # create directories if they don't exist yet
        for d in list(self.plotting_dirs.values()):
            if not os.path.exists(d):
                logging.debug(f"Creating tracker directory after first epoch: {d}")
                os.makedirs(d)

    @abstractmethod
    def make_plotting_dirs(self):
        """Create a dictionary of directories for different plotting graphs."""
        pass

    @abstractmethod
    def get_predictions(self, stage):
        """Needs to be implemented for different tasks. Basically, it is the forward of the model."""
        return None

    @abstractmethod
    def compute(self, stage):
        self.stage, self.current_epoch = stage, self.module.current_epoch

        if self.current_epoch == 0:
            self.on_first_epoch()

        # check if metrics should be calculated this epoch
        if self.current_epoch % self.experiment_conf["check_metrics_n_epoch"] != 0 and self.stage != "test":
            logging.debug(f"Skipping metrics computation for epoch {self.current_epoch}")
            return False

        # get predictions, needs to be implemented
        self.get_predictions(stage)

        return True

    @abstractmethod
    def plot(self):
        """Plot the metrics."""
        self.module.logger.experiment.log_artifact(local_path=self.base_dir, run_id=self.module.logger.run_id)
        return None
