import numpy as np
from matrix_functions import translate, rotate_x, rotate_y, rotate_z, scale


class Object3D:
    def __init__(self, render):
        self.render = render
        # position of cube vertexes
        self.vertexes = np.array(
            [
                (0, 0, 0, 1),
                (0, 1, 0, 1),
                (1, 1, 0, 1),
                (1, 0, 0, 1),
                (0, 0, 1, 1),
                (0, 1, 1, 1),
                (1, 1, 1, 1),
                (1, 0, 1, 1),
            ]
        )
        # list of tuples that contains vertices indexes
        self.faces = np.array(
            [
                (0, 1, 2, 3),
                (4, 5, 6, 7),
                (0, 4, 5, 1),
                (2, 3, 7, 6),
                (1, 2, 6, 5),
                (0, 3, 7, 4),
            ]
        )

    # @ operator = a.__matmul__(b)
    #  or dot(a, b)
    #  a @= b
    #  a = dot(a, b)

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)

    def scale(self, n):
        self.vertexes = self.vertexes @ scale(n)

    def rotate_x(self, alpha):
        self.vertexes = self.vertexes @ rotate_x(alpha)

    def rotate_y(self, alpha):
        self.vertexes = self.vertexes @ rotate_y(alpha)

    def rotate_z(self, alpha):
        self.vertexes = self.vertexes @ rotate_z(alpha)
