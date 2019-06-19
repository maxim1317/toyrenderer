import numpy as np


class Scene(object):
    """docstring for Scene"""

    def __init__(self, saved="default"):
        self.saved = saved

        self.color_plane0 = 1. * np.ones(3)
        self.color_plane1 = 0. * np.ones(3)

        self.O = np.array([0., 0.35, -1.])  # Camera.
        self.Q = np.array([0., 0., 0.])  # Camera pointing to.
        self.L = np.array([5., 5., -10.])
        self.color_light = np.ones(3)

        self.scene = [
            self.add_sphere([  .75,  .1, 1.  ], .6, [0., 0.   , 1.   ]),
            self.add_sphere([- .75,  .1, 2.25], .6, [ .5, .223,  .5  ]),
            self.add_sphere([-2.75,  .1, 3.5 ], .6, [1.,  .572,  .184]),
            self.add_plane( [0., -.5, 0.], [0., 1., 0.]),
        ]

    def add_sphere(self, position, radius, color):
        return dict(
            type='sphere',
            position=np.array(position),
            radius=np.array(radius),
            color=np.array(color),
            reflection=.5
        )

    def add_plane(self, position, normal):
        return dict(
            type='plane',
            position=np.array(position),
            normal=np.array(normal),
            color=lambda M: (
                self.color_plane0 if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2) else self.color_plane1
            ),
            diffuse_c=.75, specular_c=.5, reflection=.25
        )
