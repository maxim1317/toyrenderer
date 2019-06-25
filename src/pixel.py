class Pixel(object):
    def __init__(self, ix, iy):
        from .consts import BLACK

        self.ix = ix
        self.iy = iy

        self.color = BLACK
