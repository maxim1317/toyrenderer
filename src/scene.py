import numpy as np


class Scene(object):
    """docstring for Scene"""

    def __init__(self, objects):

        add_fn = {
            "sphere": self.add_sphere
        }

        self.objects = [add_fn[obj["type"]](obj["center"], obj["radius"], obj["color"]) for obj in objects]

    def add_sphere(self, center, radius, color):
        from .objects.sphere import Sphere

        params = {
            "center": np.array(center),
            "radius": np.array(radius),
            "color": np.array(color),
        }

        return Sphere(params)
