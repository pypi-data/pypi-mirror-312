from hydronaut.experiment import Experiment

import sys

sys.path.append(".")

from torch.utils.data import DataLoader
from model.swotted import swottedModule, swottedTrainer
from model.utils import Subset
from model.loss_metrics import *
from experiments.gen_data import gen_synthetic_data


import numpy as np
import time
import matplotlib.pyplot as plt

import pickle


class SyntheticDatasetExperiment(Experiment):
    """Hydronaut experiment representing an experiment with synthetic datasets

    The experiment generates a random dataset with planted temporal phenotypes, and then
    it uses the SWoTTeD on the synthetic dataset to extract phenotypes.
    The extraction is evaluated on a test set.

    All the parameters of the experiments (experiments, dataset and SWoTTeD parameters)
    have to be located in the `conf` directory

    To run this experiment,:
    ```bash
    export HYDRONAUT_CONFIG=experiments/conf/experiment1.yaml
    hydronaut-run```

    """

    def gen_image(self, Ph_, filename="phenotypes.png"):
        """Create a PNG image to compare the extracted phenotypes.

        This function reorders the phenotypes.

        Parameters
        ==========
        Ph_ : torch.Tensor
            list of phenotypes to figure out.
        filename: str
            name of the file to generate (default: 'phenotype.png')"""
        reordered_pheno, _ = self.swotted.reorderPhenotypes(Ph_, tw=self.swotted.twl)
        R = len(Ph_)
        fig, axs = plt.subplots(R, 2)
        for i in range(R):
            axs[i, 0].imshow(
                Ph_[i], cmap="gray", vmin=0, vmax=1, interpolation="nearest"
            )
            axs[i, 0].set_ylabel("Drugs")
            axs[i, 0].set_xlabel("time")
            axs[i, 0].set_title("phenotype")
            axs[i, 1].imshow(
                reordered_pheno[i].detach().numpy(),
                cmap="gray",
                vmin=0,
                vmax=1,
                interpolation="nearest",
            )
            axs[i, 1].set_ylabel("Drugs")
            axs[i, 1].set_xlabel("time")
            axs[i, 1].set_title("result")
        fig.savefig(filename)

    def __call__(self) -> float:
        """Implement the detail of one instance of the Hydronaut experiment.

        This experiment generates several artifacts:
        - `Ph_hidden.pkl`: the hidden phenotypes
        - `Ph.pkl`: the extracted phenotypes
        - ̀ phenotypes.png`:

        Returns
        --------
        float
            Test loss metric
        """

        params = self.config.experiment.params

        K = (
            params.synth_data.K_train + params.synth_data.K_test
        )  #: number of patients to generate
        N = params.synth_data.N  #: number of medical events
        T = params.synth_data.T  #: length of time's stay
        R = params.synth_data.R  #: number of phenotypes
        Tw = params.synth_data.Tw  #: length of time's window
        # id = params.synth_data.id  #: length of time's window

        # Generating synthetic data
        _, Ph_, X, _ = gen_synthetic_data(
            K, N, T, R, Tw, sliding_window=True, noise=0.0, truncate=True
        )

        pickle.dump(Ph_, open("Ph_hidden.pkl", "wb"))
        self.log_artifact("Ph_hidden.pkl", "Ph_hidden")

        # define the model
        self.swotted = swottedModule(params)

        train_data_loader = DataLoader(
            Subset(
                X[: params.synth_data.K_train], np.arange(params.synth_data.K_train)
            ),
            batch_size=params.training.batch_size,
            shuffle=False,
            collate_fn=lambda x: x,
        )
        test_data_loader = DataLoader(
            Subset(X[params.synth_data.K_train :], np.arange(params.synth_data.K_test)),
            batch_size=params.training.batch_size,
            shuffle=False,
            collate_fn=lambda x: x,
        )

        # train the model (`fast_dev_run` is a helpful Trainer arguments for rapid idea iteration)
        trainer = swottedTrainer(fast_dev_run=False, max_epochs=params.training.nepochs)
        before = time.time()
        trainer.fit(model=self.swotted, train_dataloaders=train_data_loader)
        duration = time.time() - before
        self.log_metric("training_time", duration)

        # save model
        pickle.dump(self.swotted.Ph, open("Ph.pkl", "wb"))
        self.log_artifact("Ph.pkl", "Ph_model")

        self.gen_image(Ph_, "phenotypes.png")
        self.log_artifact("phenotypes.png", "Ph_images")

        ret = trainer.test(self.swotted, test_data_loader)
        # ret is a (list of) dictionary that contains the logged values.

        # Log the both metrics
        # self.log_metric('train_loss', ret_fit["train_loss_Ph"])
        self.log_metric("test_loss", ret[0]["test_loss"])

        return ret[0]["test_loss"]


# run Hydronaut with the default parameters
from hydronaut.run import Runner

if __name__ == "__main__":
    Runner()()
