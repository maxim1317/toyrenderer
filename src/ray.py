import numpy as np
from rendutils import *


class Ray(object):
    """docstring for Ray"""

    def __init__(self, origin, direction):
        self.origin    = np.array(origin)
        self.direction = np.array(direction)

        self.t = None
        self.object_hit = None

    def get_nearest_object(self):
        if self.nearest_object is not None:
            return self.nearest_object

        min_dist = None
        for obj in self.objects_hit:
            dist = np.linalg.norm(obj["hit_position"] - self.origin)
            if (min_dist is None) or (dist < min_dist):
                min_dist = dist
                self.nearest_object = obj
                self.hit_position   = obj["hit_position"]
                self.hit_normal     = obj["hit_normal"]

        return self.nearest_object

    def is_hit(self, objects):
        checkers = {
            "sphere": self.hit_sphere
        }
        for obj in objects:
            checker = checkers[obj["type"]]
            t = checker(obj)

            if self.t is None or 0 < t < self.t:
                self.t = t
                self.object_hit = obj

            return t
            # if t and t:
            #     self.objects_hit.append(obj.copy())

        return False

    def hit_sphere(self, sphere):
        # print("origin", self.origin)
        # print("sphere", sphere)
        OC = self.origin - sphere["center"]

        a = np.dot(self.direction, self.direction)
        b = 2 * np.dot(OC, self.direction)
        c = np.dot(OC, OC) - sphere["radius"] * sphere["radius"]

        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return False
        else:
            t = -(-b - np.sqrt(discriminant)) / (2.0 * a)
            return t

    def point_at_parameter(self, t):
        return self.origin + t * self.direction
