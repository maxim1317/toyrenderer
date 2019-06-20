import numpy as np


class Camera(object):
    """docstring for Camera"""

    def __init__(self, w, h):
        self.matrix    = None
        self.position  = None
        self.direction = None

        self.w = w
        self.h = h
        self.matrix_real_size = (3.6, 2.4)  # Full frame he-he...

        pass

    def form_matrix(self):
        from pixel import Pixel

        self.matrix = np.ndarray(shape=(self.w, self.h), dtype=np.object)
        print(self.matrix.shape)
        for ix, iy in np.ndindex(self.matrix.shape):
            self.matrix[ix, iy] = Pixel(ix, iy)

    def get_pixel_position(self, ix, iy):
        """
        @brief      Returns pixel position in space

        @return     The pixel position.
        """
        assert False, "Camera.get_pixel_position() is not implemented yet"

    def generate_ray(self):
        from ray import Ray

        Ray()

        assert False, "Camera.generate_ray() is not implemented yet"


def camera_test():
    camera = Camera(2, 2)
    camera.form_matrix()
    print(camera.matrix)


if __name__ == '__main__':
    camera_test()
