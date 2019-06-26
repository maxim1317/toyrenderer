import numpy as np


def add_sphere(center, radius, material_params):
    from .objects.sphere import Sphere

    material = add_mat[material_params["type"]](material_params)

    params = {
        "center"  : np.array(center),
        "radius"  : np.array(radius),
        "material": material,
    }

    return Sphere(params)


def add_lambertian(params):
    from .materials.lambertian import Lambertian

    return Lambertian(np.array(params["albedo"]))


def add_metal(params):
    from .materials.metal import Metal

    return Metal(np.array(params["albedo"]), params["fuzz"])


add_obj = {
    "sphere": add_sphere
}
add_mat = {
    "lambertian": add_lambertian,
    "metal": add_metal
}