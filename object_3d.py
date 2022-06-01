from __future__ import annotations
import numpy as np
import pygame
from matrix_functions import translate, rotate_x, rotate_y, rotate_z, scale

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GameWindow


class Object3D:
    def __init__(self, render: GameWindow):
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

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        # transfer to camera space
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        # transfer to clip space
        vertexes = vertexes @ self.render.projection.projection_matrix
        # normalize
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        # clip
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        # project to screen
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        # get screen X and Y
        vertexes = vertexes[:, :2]

        # clipped vertexes will be on screen center, do not draw them
        for face in self.faces:
            polygon = vertexes[face]
            if not np.any(
                (polygon == self.render.center_width)
                | (polygon == self.render.center_height)
            ):
                pygame.draw.polygon(
                    self.render.screen, pygame.Color("orange"), polygon, 3
                )

        for vertex in vertexes:
            if not np.any(
                (vertex == self.render.center_width)
                | (vertex == self.render.center_height)
            ):
                pygame.draw.circle(self.render.screen, pygame.Color("white"), vertex, 6)

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
