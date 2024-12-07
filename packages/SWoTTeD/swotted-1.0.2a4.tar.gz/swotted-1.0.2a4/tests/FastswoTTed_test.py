import sys

sys.path.append(".")

from torch.utils.data import DataLoader
from swotted import fastSWoTTeDModule, fastSWoTTeDTrainer, fastSWoTTeDDataset
from swotted.utils import Subset
from swotted.loss_metrics import *
from gen_data import gen_synthetic_data

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from omegaconf import OmegaConf


if __name__ == "__main__":
    K = 400  #: number of patients
    N = 10  #: number of medical events
    T = 10  #: length of time's stay
    R = 4  #: number of phenotypes
    Tw = 3  #: length of time's window

    # Generating synthetic data
    W_, Ph_, X, params = gen_synthetic_data(
        K, N, T, R, Tw, sliding_window=True, noise=False, truncate=True
    )

    # create a 3D-tensor required by FastSwotted
    X = torch.stack(X, dim=0)

    params = {}
    params["model"] = {}
    params["model"]["non_succession"] = 0.5
    params["model"]["sparsity"] = 0.5
    params["model"]["rank"] = R
    params["model"]["twl"] = Tw
    params["model"]["N"] = N
    params["model"]["metric"] = "Bernoulli"
    params["training"] = {}
    params["training"]["batch_size"] = 50
    params["training"]["nepochs"] = 800
    params["training"]["lr"] = 1e-2
    params["predict"] = {}
    params["predict"]["nepochs"] = 400
    params["predict"]["lr"] = 1e-2

    config = OmegaConf.create(params)

    # define the model
    swotted = fastSWoTTeDModule(config)

    train_loader = DataLoader(
        fastSWoTTeDDataset(X),
        batch_size=params["training"]["batch_size"],
        shuffle=False,
        collate_fn=lambda x: x,
    )

    # train the model (hint: here are some helpful Trainer arguments for rapid idea iteration)
    trainer = fastSWoTTeDTrainer(
        fast_dev_run=False, max_epochs=params["training"]["nepochs"]
    )
    trainer.fit(model=swotted, train_dataloaders=train_loader)

    # visualize the phenotype
    reordered_pheno, reordered_pathways = swotted.reorderPhenotypes(Ph_, tw=Tw)
    for i in range(R):
        plt.subplot(121)
        sns.heatmap(Ph_[i], vmin=0, vmax=1, cmap="binary")
        plt.ylabel("Drugs")
        plt.xlabel("time")
        plt.title("phenotype")
        plt.subplot(122)
        sns.heatmap(reordered_pheno[i].detach().numpy(), vmin=0, vmax=1, cmap="binary")
        plt.ylabel("Drugs")
        plt.xlabel("time")
        plt.title("result")
        plt.show()

    # make decomposition with the train model: it projects the X on the phenotypes of the model
    # note that projection can be applied on new data. We use data from the training set for the sake
    # of the simplicity
    id = 15
    W = swotted(X[id, :, :].unsqueeze(0))
    _, W = swotted.reorderPhenotypes(Ph_, W)

    # Visual comparison of the care pathways
    plt.subplot(211)
    sns.heatmap(W_[id], vmin=0, vmax=1, cmap="binary")
    plt.ylabel("Drugs")
    plt.xlabel("time")
    plt.subplot(212)
    sns.heatmap(W[0].detach().numpy(), vmin=0, vmax=1, cmap="binary")
    plt.ylabel("Drugs")
    plt.xlabel("time")
    plt.title("reconstruction (not reordered)")
    plt.show()

    # we can also forecast the end of the :
    id = 15
    pred = swotted.forecast(X[id, :, :-1].unsqueeze(0))

    # Visual comparison of the care pathways
    plt.subplot(211)
    sns.heatmap(X[id, :, -1].unsqueeze(0), vmin=0, vmax=1, cmap="binary")
    plt.ylabel("Drugs")
    plt.xlabel("time")
    plt.subplot(212)
    sns.heatmap(pred[0].unsqueeze(0), vmin=0, vmax=1, cmap="binary")
    plt.ylabel("Drugs")
    plt.xlabel("time")
    plt.title("Forecast")
    plt.show()
