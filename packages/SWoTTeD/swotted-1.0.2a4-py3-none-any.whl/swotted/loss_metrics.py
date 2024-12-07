# -*- coding: utf-8 -*-
"""This module contains the alternative losses that can be used
in tensor decomposition tasks.
"""

import torch


class Loss:
    """Difference loss"""

    def compute(self, X, Y):
        return (X - Y).sum()


class Frobenius(Loss):
    """Frobenius loss to be used with data assuming a gaussian distribution
    of their values."""

    def compute(self, X, Y):
        return torch.norm((X - Y), p="fro").sum()


class Poisson(Loss):
    """Frobenius loss to be used with data assuming a Poisson distribution
    of their values (counting attribute)."""

    def compute(self, X, Y):
        return Y.sum() - (X * torch.log(Y.clamp(min=1e-10))).sum()


class Bernoulli(Loss):
    """Frobenius loss to be used with data assuming a bernoulli distribution
    of their values (discrete values)."""

    def compute(self, X, Y):
        return (torch.log(1 + Y.clamp(min=1e-10))).sum() - (
            X * torch.log(Y.clamp(min=1e-10))
        ).sum()
