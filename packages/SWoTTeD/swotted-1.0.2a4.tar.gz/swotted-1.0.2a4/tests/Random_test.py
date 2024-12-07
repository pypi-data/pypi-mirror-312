import sys

sys.path.append(".")

from torch.utils.data import DataLoader
from swotted import fastSWoTTeDModule, fastSWoTTeDTrainer, fastSWoTTeDDataset
from swotted.loss_metrics import *

import matplotlib.pyplot as plt
from omegaconf import OmegaConf


if __name__ == "__main__":
    K = 200  #: number of patients
    N = 5  #: number of medical events
    T = 10  #: length of time's stay
    R = 4  #: number of phenotypes to discover
    Tw = 3  #: length of time's window
    
    #generation of a random tensor
    X=torch.bernoulli( torch.ones(K,N,T)*0.2 )

    params = {}
    params["model"] = {}
    params["model"]["non_succession"] = 0.5
    params["model"]["sparsity"] = 0.5
    params["model"]["rank"] = R
    params["model"]["twl"] = Tw
    params["model"]["N"] = N
    params["model"]["metric"] = "Bernoulli"
    params["training"] = {}
    params["training"]["batch_size"] = 40
    params["training"]["nepochs"] = 100
    params["training"]["lr"] = 1e-2
    params["predict"] = {}
    params["predict"]["nepochs"] = 100
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

    # train the model
    trainer = fastSWoTTeDTrainer(
        max_epochs=params["training"]["nepochs"]
    )
    trainer.fit(model=swotted, train_dataloaders=train_loader)

    # visualize the phenotypes
    Ph = swotted.Ph.flip(2).detach().numpy()
    for i in range(R):
        plt.imshow(Ph[i], vmin=0, vmax=1, cmap="binary",interpolation='none')
        plt.ylabel("Drugs")
        plt.xlabel("Time")
        plt.title("Phenotype")
        plt.show()

    # make decomposition with the train model: it projects the X on the phenotypes of the model
    # note that projection can be applied on new data. We use data from the training set for the sake
    # of simplicity
    id = 15
    W = swotted(X[id, :, :].unsqueeze(0))

    # Apply reconstruction
    Y = swotted.model.reconstruct(W,swotted.Ph)

    # Patient decomposition
    plt.subplot(211)
    plt.imshow(X[id].detach().numpy(), vmin=0, vmax=1, cmap="binary",interpolation='none')
    plt.ylabel("Drugs")
    plt.xlabel("Time")
    plt.title("Input matrix")
    plt.subplot(212)
    plt.imshow(Y[0].detach().numpy(), vmin=0, vmax=1, cmap="binary",interpolation='none')
    plt.ylabel("Drugs")
    plt.xlabel("Time")
    plt.title("Pathway")
    plt.title("reconstruction (not reordered)")
    plt.show()