import numpy as np
from rendutils import *


class Renderer(object):
    """docstring for Renderer"""

    image = None

    def __init__(self, width, height, scene):
        self.w = width
        self.h = height

        self.depth_max = 5

        self.scene = scene

    def render(self):
        self.image = np.zeros((self.w, self.h, 3))

        # self.image = np.vectorize(self.cast_ray)(self.image)
        self.image = self.cast_ray(self.image)

        self.image *= (255.0 / self.image.max())
        self.image = self.image.astype(np.uint8)
        # print(self.image)
        self.save(self.image)

        return self.image

    def cast_ray(self, image):
        from tqdm import tqdm

        col = np.zeros(3)
        r = float(self.w) / self.h
        # Screen coordinates: x0, y0, x1, y1.
        S = (-1., -1. / r + .25, 1., 1. / r + .25)
        # Loop through all pixels.

        prog = tqdm(total=100, unit_scale=True)

        # print(r)
        for i, x in enumerate(np.linspace(S[0], S[2], self.w)):
            # if i % 10 == 0:
                # print(int(i / float(self.w) * 100), "%")

            for j, y in enumerate(np.linspace(S[1], S[3], self.h)):
                col[:] = 0
                self.scene.Q[:2] = (x, y)
                D = normalize(self.scene.Q - self.scene.O)
                depth = 0
                rayO, rayD = self.scene.O, D
                reflection = 1.
                # Loop through initial and secondary rays.
                while depth < self.depth_max:
                    traced = trace_ray(rayO, rayD, self.scene)
                    if not traced:
                        break
                    obj, M, N, col_ray = traced
                    # Reflection: create a new ray.
                    rayO, rayD = M + N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
                    depth += 1
                    col += reflection * col_ray
                    reflection *= obj.get('reflection', 1.)
                    image[self.h - j - 1, i, :] = np.clip(col, 0, 1)
                    # print(self.h - j - 1, i)
                prog.update(100 / (self.w * self.h))

        prog.close()

        return image

    def save(self, npimage):
        from PIL import Image

        image = Image.fromarray(npimage, 'RGB')
        image.save('test.png')

        return


def test_renderer():
    from scene import Scene

    rend = Renderer(640, 640, Scene(saved="default"))
    rend.render()


if __name__ == '__main__':
    test_renderer()
