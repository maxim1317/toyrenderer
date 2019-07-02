import numpy as np
from .rendutils import normalize


class Material(object):
    """docstring for Material"""

    def scatter(self, ray, rec, attenuation, scattered_ray):
        assert False, "Must be emplemented in material classes"

    def reflect(self, v, n):
        return v - n * (np.dot(v, n) * 2)

    def refract(self, v, n , ni_over_nt, refracted):
        uv = normalize(v)

        dt = np.dot(uv, n)

        disc = 1 - ni_over_nt * ni_over_nt * (1 - dt * dt)
        if disc > 0:
            refracted = ni_over_nt * (uv - n * dt) - n * np.sqrt(disc)
            return True, refracted
        else:
            return False, refracted

    def shlick(self, cosine, ref_idx):
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0

        return r0 + (1 - r0) * (1 - cosine)**5
