"""
Module of synthetic 3D tensor generation mimicking collections of care pathways. 
The generated tensors are assumed to have three dimensions: idpatient, medical features and time.
"""

import numpy as np
import random
import torch
from datetime import datetime


def genVkWithTemporalWindow(N, R, Tstep):
    """
    Parameters
    ----------
    N : int
        number of medical events
    R : int
        Number of phenotypes
    Tstep : int
        length of time's window

    Returns
    --------
    Tensor
        R matrices of phenotypes of size : :math:̀ N x T`, or a matrice of size :math:̀ R x N`
    """
    Vk = torch.zeros((R, N, Tstep))
    for k in range(R):
        m = random.randint(1, int(N / 4))  # draw a number of medical events
        med = random.sample(
            [i for i in range(N)], m
        )  # select a group of medical events

        for l in med:
            if Tstep == 1:
                Vk[k][l][0] = 1
            else:
                t = random.randint(1, int(Tstep / 2))  # draw a number of days
                days = random.sample(
                    [i for i in range(Tstep)], t
                )  # select a group of days

                for d in days:
                    Vk[k][l][d] = 1

    return Vk


def genUkWithTemporalWidow(K, T, R):
    """
    Parameters
    -----------
    K : int
        number of patients
    T : int
        time (length of time's stay / window)
    R : int
        number of phenotype
    Returns
    --------
    list(torch.Tensor)
        K matrices of patients pathways of size : T x R
    """
    Uk = torch.zeros((K, T, R))
    for k in range(K):
        for t in range(T):
            nbPh = random.randint(1, R)  # draw a number of phenotypes
            lph = random.sample(
                [i for i in range(R)], nbPh
            )  # select a group of nbPh phenotypes
            for p in lph:
                Uk[k][t][p] = 1  # random.uniform(0,1)
    return Uk


def genTensor4DWithTemporalWindow(K, N, T, R, Tstep, noise=0.0, truncate=True):
    """
    Parameters
    ----------
    K : int
        number of patients
    N : int
        number of medical events
    T : int
        length of time's stay
    R : int
        number of phenotype
    Tstep : int
        length of time's window
    noise : float

    Returns
    --------
    list(torch.Tensor)
        K 3D tensors of size (T/Tstep) x N x step
    """
    Uk = genUkWithTemporalWidow(K, T // Tstep, R)  # generate patients pathways
    Vk = genVkWithTemporalWindow(N, R, Tstep)  # generate temporal phenotypes

    tensor4D = torch.tensordot(Uk, Vk, dims=1)
    if truncate:
        tensor4D.data[tensor4D.data > 1] = 1  # truncate values greater than n

    if noise>0:
        Uk += noise * np.random.normal(size=Uk.shape)  # add noise

    return Uk, Vk, tensor4D


def genUkWithSlidingTemporalWidow(K, T, R, Tw):
    """
    Parameters
    -----------
    K : int
        number of patients
    T : int
        time (length of time's stay / window)
    R : int
        number of phenotype
    Tw : int
        length of the phenotype's temporal window

    Returns
    -------
    list(torch.Tensor)
        K matrices of patients pathways of size : R x (T - Tw + 1)
    """
    Uk = torch.zeros((K, R, (T - Tw + 1)))
    for k in range(K):
        for r in range(R):
            for t in range((T - Tw + 1)):
                choice = random.randint(0, 1)
                i = 0
                while choice and i < Tw:
                    if t - i >= 0:
                        if Uk[k][r][t - i] == 1:
                            choice = False
                    if t + i < T - Tw:
                        if Uk[k][r][t + i] == 1:
                            choice = False
                    i = i + 1
                Uk[k][r][t] = choice

    return Uk


def genTensor3DWithSlidingTemporalWindow(K, N, T, R, Tw, noise=0.0, truncate=True):
    """
    Parameters
    ----------
    K : int
        number of patients
    N : int
        number of medical events
    T : int
        length of time's stay
    R : int
        number of phenotype
    Tw : int
        length of time's window
    noise : float

    Returns
    ---------
    list(torch.Tensor)
        K matrices of size  N x T

    """
    Uk = genUkWithSlidingTemporalWidow(K, T, R, Tw)  # generate patients pathways
    Vk = genVkWithTemporalWindow(N, R, Tw)  # generate temporal phenotypes

    if noise>0:
        Uk += noise * np.random.normal(size=Uk.shape)  # add noise

    Y = []
    for p in range(K):
        # create a tensor of windows
        dec = torch.tensordot(Uk[p], Vk, dims=([0], [0]))

        # now ... windows have to be summed
        Yp = torch.zeros((N, T))
        for i in range(T - Tw + 1):
            Yp[:, i : (i + Tw)] += dec[i]

        Y.append(Yp)

    Y = torch.stack(Y)
    if truncate:
        Y.data[Y > 1] = 1  # truncate values greater than 1

    return Uk, Vk, Y


def gen_synthetic_data(
    K=100,
    N=20,
    T=6,
    R_hidden=4,
    Tw_hidden=3,
    sliding_window=False,
    noise=0.0,
    truncate=True,
    **_kwargs
):
    """
    Parameters
    -----------
    K : int
        number of patients
    N : int
        number of medical events
    T: int
        length of time's stay
    R : int
        number of phenotype
    Tw : int
        length of time's window
    sliding_window : bool
        if true genUkwithSlidingTemporalWindow
    noise : float,
        if >0 add a normal noise to the generated tensor

    Returns
    -------
    list(torch.Tensor)
        W: third-order tensor representing pathways
    torch.Tensor
        Ph: third-order tensor prepresenting phenotyes or a matrice of size R x N
    list(torch.Tensor)
        X: a list of K matrices of size  N x T
    dict
        a dictionary containing the parameters used to generate the dataset

    """

    params = {}
    params[
        "source"
    ] = "synthetic"  # this indicates the source of the dataset (its name, version of the generator, etc.)
    params["date"] = datetime.now()  # keep the date at which it has been generated
    # matrix dimensions
    params["K"] = K
    params["N"] = N
    params["T"] = T
    # synthetic data parameters
    params["sliding_window"] = sliding_window
    params["R_hidden"] = R_hidden
    params["Tw_hidden"] = Tw_hidden
    params["noise"] = noise
    params["truncate"] = truncate

    if sliding_window:
        W_, Ph_, dataset = genTensor3DWithSlidingTemporalWindow(
            K, N, T, R_hidden, Tw_hidden, noise, truncate
        )
        X = [dataset[i] for i in range(dataset.shape[0])]

    else:
        W_, Ph_, dataset = genTensor4DWithTemporalWindow(
            K, N, T, R_hidden, Tw_hidden, noise, truncate
        )
        X = [
            torch.cat(tuple([dataset[i][j] for j in range(dataset.shape[1])]), axis=1)
            for i in range(dataset.shape[0])
        ]

    if Tw_hidden == 1:
        Ph_ = torch.squeeze(Ph_, 2)

    return W_, Ph_, X, params
