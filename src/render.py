import numpy as np
from rendutils import *


class Renderer(object):
    """docstring for Renderer"""

    image = None

    def __init__(self, width, height, scene):
        self.w = width
        self.h = height

        self.maxdepth = 5

        self.scene = scene

    def render(self):
        from camera import Camera

        camera = Camera(self.w, self.h)
        camera.form_matrix()

        image = np.apply_along_axis(self.multitrace, 2, image)
        # for pixel in final_image:
        #     for i in num_samples:
        #         r = camera.generate_ray(pixel)
        #         pixel.color += self.trace_path(r, 0)

        # pixel.color /= num_samples  # Average samples.

    def save(self, npimage):
        from PIL import Image

        image = Image.fromarray(npimage, 'RGB')
        image.save('test.png')

        return

    def trace_path(self, ray, depth: int):
        from consts import BLACK

        if (depth >= self.maxdepth) :
            return BLACK  # Bounced enough times.

        ray.find_nearest_object()

        if ray.hit_something is False:
            return BLACK  # Nothing was hit.

        material = ray.thing_hit.material  # material = Material()
        emittance = material.emittance  # emittance = Color()

        # Pick a random direction from here and keep going.
        newRay = Ray()
        newRay.origin = ray.point_where_obj_was_hit

        # This is NOT a cosine-weighted distribution!
        newRay.direction = RandomUnitVectorInHemisphereOf(ray.normal_where_obj_was_hit)

        # Probability of the newRay
        p = 1. / (2 * np.pi)

        # Compute the BRDF for this ray (assuming Lambertian reflection)
        cos_theta = np.dot(newRay.direction, ray.normal_where_obj_was_hit)
        BRDF = material.reflectance / np.pi  # BRDF = Color()

        # Recursively trace reflected light sources.
        incoming = trace_path(newRay, depth + 1)

        # Apply the Rendering Equation here.
        return emittance + (BRDF * incoming * cos_theta / p)

    def multitrace(self, pixel):
        for i in range(self.iterations):
            ray = camera.generate_ray(pixel)
            pixel += trace_path(ray, 0)


def test_renderer():
    from scene import Scene

    rend = Renderer(2, 2, Scene(saved="default"))
    rend.render()


if __name__ == '__main__':
    test_renderer()
