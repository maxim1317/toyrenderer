import numpy as np
from .. import material, rendutils


class Metal(material.Material):

    def __init__(self, albedo, fuzz):
        self.albedo = albedo

        if fuzz < 1:
            self.fuzz = fuzz
        else:
            self.fuzz = 1

    def scatter(self, ray, rec, attenuation, scattered_ray):
        from ..ray import Ray
        from ..rendutils import random_in_unit_sphere

        reflected = self.reflect(rendutils.normalize(ray.direction), rec.normal)
        scattered_ray = Ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())

        attenuation = self.albedo

        return (
            np.dot(scattered_ray.direction, rec.normal) > 0,
            attenuation,
            scattered_ray
        )
