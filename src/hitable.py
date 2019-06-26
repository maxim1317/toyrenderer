from recordclass import recordclass
# from .material import Material


HitRecord = recordclass('HitRecord', ['t', 'p', 'normal', 'material'])


class Hitable(object):
    """docstring for Hitable"""

    type = "Hitable"

    def hit(self, ray, t_min, t_max, rec):
        assert False, "Must be emplemented in object classes"

