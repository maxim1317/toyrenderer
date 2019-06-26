from .scenutils import add_obj


class Scene(object):
    """docstring for Scene"""

    def __init__(self, objects):

        self.objects = [add_obj[obj["type"]](obj["center"], obj["radius"], obj["material"]) for obj in objects]
