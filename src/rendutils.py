import numpy as np


def normalize(x):
    x /= np.linalg.norm(x)
    return x


def intersect_plane(O, D, P, N):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # plane (P, N), or +inf if there is no intersection.
    # O and P are 3D points, D and N (normal) are normalized vectors.
    denom = np.dot(D, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(P - O, N) / denom
    if d < 0:
        return np.inf
    return d


def intersect_sphere(O, D, S, R):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # sphere (S, R), or +inf if there is no intersection.
    # O and S are 3D points, D (direction) is a normalized vector, R is a scalar.
    a = np.dot(D, D)
    OS = O - S
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
    disc = b * b - 4 * a * c
    if disc > 0:
        distSqrt = np.sqrt(disc)
        q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return np.inf


def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])


def get_normal(obj, M):
    # Find normal.
    if obj['type'] == 'sphere':
        N = normalize(M - obj['position'])
    elif obj['type'] == 'plane':
        N = obj['normal']
    return N


def get_color(obj, M):
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(M)
    return color


def trace_path(ray: Ray, depth: int) -> Color:
    if (depth >= self.maxdepth) :
        return BLACK  # Bounced enough times.

    ray.find_nearest_object()

    if ray.hit_something is False:
        return BLACK  # Nothing was hit.

    material = ray.thingHit.material  # material = Material()
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

def multitrace(self)