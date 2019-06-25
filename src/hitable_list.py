# import numpy as np
from .hitable import Hitable, HitRecord


class HitableList(Hitable):
    """docstring for HitableList"""

    def __init__(self, hitable_list):
        self.hitable_list = hitable_list

    def hit(self, ray, t_min, t_max, rec):

        temp_rec = HitRecord(None, None, None, None)

        hit_any = False
        closest = t_max

        for hitable in self.hitable_list:
            hit, temp_rec = hitable.hit(ray, t_min, closest, temp_rec)
            if hit:
                hit_any = True
                closest = temp_rec.t
                rec = temp_rec

        return hit_any, rec
