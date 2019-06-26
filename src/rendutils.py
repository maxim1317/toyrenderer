import numpy as np


def normalize(x):
    x /= np.linalg.norm(x)
    return x


def squared_length(x):
    return np.linalg.norm(x) * np.linalg.norm(x)


def random_in_unit_sphere():
    p = 2 * np.array(
        [
            np.random.uniform(),
            np.random.uniform(),
            np.random.uniform()
        ]
    ) - np.array([1, 1, 1])

    while squared_length(p) >= 1:
        p = 2 * np.array(
            [
                np.random.uniform(),
                np.random.uniform(),
                np.random.uniform()
            ]
        ) - np.array([1, 1, 1])

    return p
