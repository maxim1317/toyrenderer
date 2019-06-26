# import numpy as np
from .. import material, rendutils


class Lambertian(material.Material):

    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, rec, attenuation, scattered_ray):
        from ..ray import Ray

        target = rec.p + rec.normal + rendutils.random_in_unit_sphere()

        scattered_ray = Ray(rec.p, target - rec.p)

        attenuation = self.albedo

        return (
            True,
            attenuation,
            scattered_ray
        )
