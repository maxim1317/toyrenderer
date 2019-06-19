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

    def render(self, final_image, num_samples):
        image = np.apply_along_axis(self., 2, a)
        for pixel in final_image:
            for i in num_samples:
                r = camera.generate_ray(pixel)
                pixel.color += self.trace_path(r, 0)

        pixel.color /= num_samples  # Average samples.


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
