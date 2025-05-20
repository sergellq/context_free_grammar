import numpy as np


def mse_metric(a, b):
    return np.mean((a.ravel() - b.ravel()) ** 2)


def mae_metric(a, b):
    return np.mean((np.abs(a.ravel() - b.ravel())))


def dispersion_metric(a, b):
    return np.std(list(a) + list(b))
