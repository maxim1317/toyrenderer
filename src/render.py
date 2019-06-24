import numpy as np
from rendutils import *


class Renderer(object):
    """docstring for Renderer"""

    image = None

    def __init__(self, width, height):
        self.w = width
        self.h = height

        self.maxdepth = 5
        self.iterations = 1

    def render(self, config="../scenes/cam_n_plane.json"):
        from camera import Camera
        from scene import Scene
        from tqdm import tqdm

        self.config = self.load_config(path=config)

        self.scene  = Scene(objects=self.config["scene"])

        self.camera = Camera(self.w, self.h, params=self.config["camera"])
        self.camera.form_matrix()

        # for pixel in np.ndindex(camera.matrix.shape)
        # camera.matrix = np.apply_along_axis(self.multitrace, 2, camera.matrix)

        bar = tqdm(total=(self.camera.matrix.size * self.iterations), unit_scale=True)
        self.camera.matrix = np.vectorize(self.multitrace)(self.camera.matrix, bar)
        bar.close()
        # print(self.camera.matrix)
        self.save()

    def save(self):
        from PIL import Image

        npimage = self.camera.matrix_as_array()

        npimage = np.ascontiguousarray(npimage.transpose(1, 0, 2))

        # npimage *= 255
        npimage = npimage.astype(np.uint8)
        # print(npimage)

        image = Image.fromarray(npimage, 'RGB')
        image.save('test.png')

        return

    def load_config(self, path):
        from utils import json_to_dict
        return json_to_dict(path)

    def multitrace(self, pixel, bar):
        for i in range(self.iterations):
            ray = self.camera.generate_ray(pixel)
            pixel.color = self.get_color(ray)
            bar.update()
        return pixel

    def get_color(self, ray):
        t = ray.is_hit(self.scene.objects)

        if t > 0:
            # N = normalize(ray.point_at_parameter(t) - np.array([0, 0, -1]))

            # color = (.5 * (N + 1)) * 255
            # print(color)

            color = ray.object_hit["color"]

            return color
        else:
            return self.get_bg_color(ray)

    def get_bg_color(self, ray):
        # print(ray.direction)
        unit_direction = normalize(ray.direction)
        t = .5 * (unit_direction[1] + 1.)

        color = (1. - t) * np.array([1., 1., 1.]) + t * np.array([.5, .7, 1.])
        color *= 255.

        return color


def test_renderer():

    rend = Renderer(400, 200)
    rend.render()


if __name__ == '__main__':
    test_renderer()
