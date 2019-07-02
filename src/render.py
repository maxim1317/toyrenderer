import numpy as np
from .rendutils import *


class Renderer(object):
    """docstring for Renderer"""

    image = None

    def __init__(self, width, height):
        self.cores = 4

        self.superrez = 1

        self.w = width * self.superrez
        self.h = height * self.superrez

        self.maxdepth = 50
        self.iterations = 100

    def render(self, config="scenes/cam_n_plane.json"):
        from .camera import Camera
        from .scene import Scene
        from .hitable_list import HitableList

        self.config = self.load_config(path=config)

        self.scene  = Scene(objects=self.config["scene"])

        hitable_list = self.scene.objects

        self.world = HitableList(hitable_list)

        if self.iterations == 1:
            antialiasing = False
        else:
            antialiasing = True

        self.camera = Camera(
            self.w,
            self.h,
            params=self.config["camera"],
            antialiasing=antialiasing
        )
        self.camera.form_matrix()

        # for pixel in np.ndindex(camera.matrix.shape)
        # camera.matrix = np.apply_along_axis(self.multitrace, 2, camera.matrix)
        self.parallelize()
        # print(self.camera.matrix)
        self.save()

    def save(self):
        from PIL import Image
        # from PIL import ImageOps

        npimage = self.camera.matrix_as_array()

        image = Image.fromarray(npimage, 'RGB')
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        # image = ImageOps.mirror(image)
        image.thumbnail((self.w // self.superrez, self.h // self.superrez), Image.ANTIALIAS)

        image.save('test.png')

        return

    def load_config(self, path):
        from .utils import json_to_dict
        return json_to_dict(path)

    def get_color(self, ray, world, depth):
        from .hitable import HitRecord
        from .ray import Ray

        rec = HitRecord(None, None, None, None)
        hit, rec = world.hit(ray, 0.0001, np.inf, rec)
        if hit:
            scattered_ray = Ray(np.zeros(3), np.zeros(3))
            attenuation   = np.zeros(3)

            scatter, attenuation, scattered_ray = rec.material.scatter(
                ray=ray,
                rec=rec,
                attenuation=attenuation,
                scattered_ray=scattered_ray
            )
            if depth < self.maxdepth and scatter:
                return attenuation * self.get_color(scattered_ray, world, depth + 1)
            else:
                return np.zeros(3)
        else:
            return self.get_bg_color(ray)

    def get_bg_color(self, ray):
        # print(ray.direction)
        unit_direction = normalize(ray.direction)
        t = .5 * (unit_direction[1] + 1.)

        color = (1. - t) * np.array([1., 1., 1.]) + t * np.array([.5, .7, 1.])
        # color *= 255.9999

        return color

    def multitrace(self, pixel, bar):
        color = np.array([0, 0, 0], dtype='float64')

        for i in range(self.iterations):
            ray = self.camera.generate_ray(pixel)
            color += self.get_color(ray, self.world, 0)

        bar.update()

        color /= self.iterations
        color = np.sqrt(color)
        color *= 255.9999

        pixel.color = color.astype('uint8')

        return pixel

    def npmap(self, q, bar, return_dict):
        # from multiprocessing import queues
        # from tqdm import tqdm

        while True:
            got = q.get()

            if got is None:
                return return_dict

            bid   = got["i"]
            batch = got["batch"]

            # bar = tqdm(total=(self.camera.matrix.size // self.batchesnum), unit_scale=True)
            # bar.set_description(desc='Batch #' + str(bid) + '/' + str(self.batchesnum))

            batch = np.vectorize(self.multitrace)(batch, bar)
            self.bar.update()

            return_dict[bid] = batch

    def parallelize(self):
        from multiprocessing import Manager, Queue, Process
        from tqdm import tqdm

        manager = Manager()
        return_dict = manager.dict()

        q = Queue()

        batches = blockshaped(self.camera.matrix, self.w // (self.w // 5), self.h // (self.h // 5))

        self.batchesnum = len(batches)
        for i in range(len(batches)):
            q.put(
                {
                    "i"    : i,
                    "batch": batches[i]
                }
            )
        q.put(None)
        q.put(None)
        q.put(None)
        q.put(None)

        self.bar = tqdm(total=self.batchesnum)
        processes = [
            Process(
                target=self.npmap,
                args=(
                    q,
                    self.bar,
                    return_dict
                )
            ) for i in range(self.cores)
        ]
        self.bar.close()

        for p in processes:
            p.start()
        for p in processes:
            p.join()

        for i in return_dict.keys():
            batches[i] = return_dict[i]

        self.camera.matrix = unblockshaped(batches, self.w, self.h)

        return
