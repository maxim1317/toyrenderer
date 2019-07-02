import numpy as np
from .. import material


class Dielectric(material.Material):

    def __init__(self, ref_idx):
        self.ref_idx = ref_idx

    def scatter(self, ray, rec, attenuation, scattered_ray):
        from ..ray import Ray

        np.seterr(all='raise')

        reflected   = self.reflect(ray.direction, rec.normal)
        refracted   = np.zeros(3)
        attenuation = np.ones(3)

        if np.dot(ray.direction, rec.normal) > 0:
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * np.dot(ray.direction, rec.normal) / np.linalg.norm(ray.direction)
        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ref_idx
            cosine = -np.dot(ray.direction, rec.normal) / np.linalg.norm(ray.direction)

        do_refract, refracted = self.refract(ray.direction, outward_normal, ni_over_nt, refracted)
        if do_refract:
            reflect_prob = self.shlick(cosine, self.ref_idx)
        else:
            scattered_ray = Ray(rec.p, reflected)
            reflect_prob = 1.0

        if np.random.random() < reflect_prob:
            scattered_ray = Ray(rec.p, reflected)
        else:
            scattered_ray = Ray(rec.p, refracted)

        return (
            True,
            attenuation,
            scattered_ray
        )
