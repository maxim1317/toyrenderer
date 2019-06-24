class Ray(object):
    """docstring for Ray"""

    def __init__(self):
        self.origin = None
        self.direction = None

        self.hit_something = None
        self.thing_hit = None
        self.normal_where_obj_was_hit = None

    def find_nearest_object(self):
        assert False, "Ray.find_nearest_object() is not implemented yet"
