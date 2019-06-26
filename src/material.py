import numpy as np


class Material(object):
    """docstring for Material"""

    def scatter(self, ray, rec, attenuation, scattered_ray):
        assert False, "Must be emplemented in material classes"

    def reflect(self, v, n):
        return v - n * (np.dot(v, n) * 2)
