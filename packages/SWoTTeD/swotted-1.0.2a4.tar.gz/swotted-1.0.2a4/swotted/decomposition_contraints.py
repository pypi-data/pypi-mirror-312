"""
SWoTTeD Module: decomposition constraints
"""

from functools import reduce
import torch


def sparsity_constraint(var):
    """Sparcity constraint (L1 metric) for a tensor `var`. The lower the better.

    Args:
        var (torch.tensor): a tensor

    Returns:
        float: constraint value
    """
    return torch.norm(var, 1)


def nonnegative_projection(*var):
    """Transform a tensor by replacing the negative values by zeros.

    Inplace transformation of the `var` parameter.

    Args:
        var: collection of tensors or tensor
    """
    for X in var:
        X.data[X.data < 0] = 0


def normalization_constraint(*var):
    """Transform a tensor by replacing the negative values by zeros and
    values greater than 1 by ones.

    Inplace transformation of the `var` parameter.

    Args:
        var: collection of tensors or tensor
    """
    for X in var:
        X.data = torch.clamp(X.data, 0, 1)


def phenotypeSuccession_constraint(Wk, Tw):
    """
    Parameters
    ----------
    Wk: torch.Tensor
        A 3rd order tensor of size :math:`K * rank * (T-Tw+1)`
    """
    O = torch.transpose(torch.stack([torch.eye(Wk[0].shape[0])] * (2 * Tw + 1)), 0, 2)
    penalisation = reduce(
        torch.add,
        [
            torch.sum(
                torch.clamp(
                    Wp * torch.log(10e-8 + torch.conv1d(Wp, O, padding=Tw)), min=0
                )
            )
            for Wp in Wk
        ],
    )
    return penalisation


def phenotype_uniqueness(Ph):
    """Evaluate the redundancy between phenotypes. The larger, the more redundant are 
    the phenotypes.
    It computes the sum of pairwise cosines-similarity (dot products) between phenotypes.

    Args:
        Ph: collection of phenotypes (2D tensors)

    Returns:
        float: constraint value
    """
    Ph = torch.transpose(Ph, 1, 2)
    ps = 0
    for i in range(Ph.shape[0]):
        for p1 in range(Ph.shape[1]):
            for j in range(i + 1, Ph.shape[0]):
                for p2 in range(Ph.shape[1]):
                    ps += torch.dot(Ph[i][p1], Ph[j][p2])

    return ps.data
