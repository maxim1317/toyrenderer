import numpy as np


class Camera(object):
    """docstring for Camera"""

    def __init__(self, w, h, params, antialiasing):
        self.matrix    = None

        self.center     = np.array(params["center"])
        self.origin     = self.center

        self.LLCorner   = np.array(params["matrix"]["LLCorner"])
        self.horizontal = np.array(params["matrix"]["horizontal"])
        self.vertical   = np.array(params["matrix"]["vertical"])

        self.w = w
        self.h = h

        self.antialiasing = antialiasing
        # self.matrix_real_size = (3.6, 2.4)  # Full frame he-he...

        pass

    def form_matrix(self):
        from .pixel import Pixel

        self.matrix = np.ndarray(shape=(self.w, self.h), dtype=np.object)
        # print(self.matrix.shape)
        for ix, iy in np.ndindex(self.matrix.shape):
            self.matrix[ix, iy] = Pixel(ix, iy)

    def get_offset(self, pixel):
        """
        @brief      Returns pixel position in space

        @return     The pixel position.
        """

        if self.antialiasing:
            return ((pixel.ix + np.random.uniform()) / self.w, (pixel.iy + np.random.uniform()) / self.h)
        else:
            return float(pixel.ix) / self.w, float(pixel.iy) / self.h

    def generate_ray(self, pixel):
        from .ray import Ray

        u, v = self.get_offset(pixel)
        ray = Ray(origin=self.origin, direction=(self.LLCorner + u * self.horizontal + v * self.vertical))

        return ray

    def matrix_as_array(self):
        nparray = np.zeros((self.w, self.h, 3))

        for ix, iy in np.ndindex(self.matrix.shape):
            # print(self.matrix[ix, iy])
            nparray[ix, iy] = self.matrix[ix, iy].color

        nparray = np.ascontiguousarray(nparray.transpose(1, 0, 2))
        nparray = nparray.astype(np.uint8)

        return nparray


def camera_test():
    from .utils import json_to_dict

    camera = Camera(2, 2, json_to_dict('../scenes/cam_n_plane.json')["camera"])
    camera.form_matrix()
    print(camera.matrix_as_array())


if __name__ == '__main__':
    camera_test()
