import numpy as np
from .rendutils import *


class Ray(object):
    """docstring for Ray"""

    def __init__(self, origin, direction):
        self.origin    = np.array(origin)
        self.direction = np.array(direction)

        self.t          = None
        self.normal     = None
        self.object_hit = None

    def get_nearest_object(self):
        if self.nearest_object is not None:
            return self.nearest_object

        min_dist = None
        for obj in self.objects_hit:
            dist = np.linalg.norm(obj.hit_position - self.origin)
            if (min_dist is None) or (dist < min_dist):
                min_dist = dist
                self.nearest_object = obj
                self.hit_position   = obj.hit_position
                self.hit_normal     = obj.hit_normal

        return self.nearest_object

    def is_hit(self, objects):
        for obj in objects:
            t = obj.hit(self)

            if self.t is None or 0 < t < self.t:
                self.t = t
                self.object_hit = obj
                self.normal = normalize(self.point_at_parameter(t) - np.array([0, 0, -1]))

            return t
            # if t and t:
            #     self.objects_hit.append(obj.copy())

        return False

    def point_at_parameter(self, t):
        return self.origin + t * self.direction
