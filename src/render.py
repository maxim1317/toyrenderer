import numpy as np
from .rendutils import *


class Renderer(object):
    """docstring for Renderer"""

    image = None

    def __init__(self, width, height):
        self.w = width
        self.h = height

        self.maxdepth = 5
        self.iterations = 1

    def render(self, config="scenes/cam_n_plane.json"):
        from tqdm import tqdm
        from .camera import Camera
        from .scene import Scene
        from .hitable_list import HitableList

        self.config = self.load_config(path=config)

        self.scene  = Scene(objects=self.config["scene"])

        hitable_list = self.scene.objects

        self.world = HitableList(hitable_list)

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
        # from PIL import ImageOps

        npimage = self.camera.matrix_as_array()

        image = Image.fromarray(npimage, 'RGB')
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        # image = ImageOps.mirror(image)

        image.save('test.png')

        return

    def load_config(self, path):
        from .utils import json_to_dict
        return json_to_dict(path)

    def multitrace(self, pixel, bar):
        color = np.array([0, 0, 0], dtype='float64')

        k = 0

        for i in range(self.iterations):
            k += 1
            ray = self.camera.generate_ray(pixel)
            color += self.get_color(ray, self.world)
            bar.update()
        color /= self.iterations
        color = np.sqrt(color)
        color *= 255.9999
        pixel.color = color.astype('uint8')

        return pixel

    def get_color(self, ray, world):
        from .hitable import HitRecord
        from .ray import Ray

        rec = HitRecord(None, None, None, None)
        hit, rec = world.hit(ray, 0.0001, np.inf, rec)
        if hit:
            target = rec.p + rec.normal + random_in_unit_sphere()

            return 0.5 * self.get_color(Ray(rec.p, target - rec.p), world)
        else:
            return self.get_bg_color(ray)

    def get_bg_color(self, ray):
        # print(ray.direction)
        unit_direction = normalize(ray.direction)
        t = .5 * (unit_direction[1] + 1.)

        color = (1. - t) * np.array([1., 1., 1.]) + t * np.array([.5, .7, 1.])
        # color *= 255.9999

        return color


