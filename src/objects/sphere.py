import numpy as np
from .. import hitable


class Sphere(hitable.Hitable):
    """docstring for Sphere"""

    type = "sphere"

    def __init__(self, params):
        self.center = params["center"]
        self.radius = params["radius"]
        self.color  = params["color"]

    def hit(self, ray, t_min, t_max, rec):
        # from .. import rendutils

        OC = ray.origin - self.center

        a = np.dot(ray.direction, ray.direction)
        b = np.dot(OC, ray.direction)
        c = np.dot(OC, OC) - self.radius * self.radius

        disc = b * b - a * c

        if disc > 0:
            temp = (-b - np.sqrt(disc)) / (a)
            if temp < t_max and temp > t_min:
                rec.t = temp
                rec.p = ray.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                rec.color = self.color

                return (True, rec)

            temp = (-b + np.sqrt(disc)) / (a)
            if temp < t_max and temp > t_min:
                rec.t = temp
                rec.p = ray.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                rec.color = self.color

                return (True, rec)

        return (False, rec)


def sphere_test():
    Sphere()


if __name__ == '__main__':
    sphere_test()
