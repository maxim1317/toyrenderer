import numpy as np


def normalize(x):
    try:
        x /= np.linalg.norm(x)
    except Exception:
        print(x)
        raise
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


def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """

    h, w = arr.shape

    assert h % nrows == 0, "{} rows is not evenly divisble by {}".format(h, nrows)
    assert w % ncols == 0, "{} cols is not evenly divisble by {}".format(w, ncols)

    return (arr.reshape(h // nrows, nrows, -1, ncols).swapaxes(1, 2).reshape(-1, nrows, ncols))


def unblockshaped(arr, h, w):
    """
    Return an array of shape (h, w) where
    h * w = arr.size

    If arr is of shape (n, nrows, ncols), n sublocks of shape (nrows, ncols),
    then the returned array preserves the "physical" layout of the sublocks.
    """
    n, nrows, ncols = arr.shape
    return (arr.reshape(h // nrows, -1, nrows, ncols).swapaxes(1, 2).reshape(h, w))
