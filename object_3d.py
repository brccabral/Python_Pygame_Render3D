from __future__ import annotations
import numpy as np
import pygame
from matrix_functions import translate, rotate_x, rotate_y, rotate_z, scale
from numba import njit

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GameWindow


# this increases fps
@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render: GameWindow, vertices, faces):
        self.render = render
        # position of cube vertices
        self.vertices = np.array([np.array(v) for v in vertices])
        # list of tuples that contains vertices indexes
        # can't add faces with different dimensions
        # normalize dimensions to 16 padding with NaN
        # before drawing we need to remove the NaN
        self.faces = np.array([np.array(f + [np.nan] * (16 - len(f))) for f in faces])

        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.color_faces = [(pygame.Color("orange"), face) for face in self.faces]
        self.movement_flag = True
        self.draw_vertices = True
        self.label = ""

    def draw(self):
        self.screen_projection()
        self.movement()

    def movement(self):
        if self.movement_flag:
            self.rotate_y(pygame.time.get_ticks() % 0.005)

    def screen_projection(self):
        # transfer to camera space
        vertices = self.vertices @ self.render.camera.camera_matrix()
        # transfer to clip space
        vertices = vertices @ self.render.projection.projection_matrix
        # normalize
        vertices /= vertices[:, -1].reshape(-1, 1)
        # clip
        vertices[(vertices > 2) | (vertices < -2)] = 0
        # project to screen
        vertices = vertices @ self.render.projection.to_screen_matrix
        # get screen X and Y
        vertices = vertices[:, :2]

        # clipped vertices will be on screen center, do not draw them
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            # remove NaN before selecting the vertices
            polygon = vertices[face[np.logical_not(np.isnan(face))].astype(np.integer)]
            if not any_func(
                polygon, self.render.center_width, self.render.center_height
            ):
                pygame.draw.polygon(self.render.screen, color, polygon, 1)
                if self.label:
                    text = self.font.render(
                        self.label[index], True, pygame.Color("white")
                    )
                    self.render.screen.blit(text, polygon[-1])

        if self.draw_vertices:
            for vertex in vertices:
                if not any_func(
                    vertex, self.render.center_width, self.render.center_height
                ):
                    pygame.draw.circle(
                        self.render.screen, pygame.Color("white"), vertex, 2
                    )

    # @ operator = a.__matmul__(b)
    #  or dot(a, b)
    #  a @= b
    #  a = dot(a, b)

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, n):
        self.vertices = self.vertices @ scale(n)

    def rotate_x(self, alpha):
        self.vertices = self.vertices @ rotate_x(alpha)

    def rotate_y(self, alpha):
        self.vertices = self.vertices @ rotate_y(alpha)

    def rotate_z(self, alpha):
        self.vertices = self.vertices @ rotate_z(alpha)


# draw only axes edges
class Axes(Object3D):
    def __init__(self, render: GameWindow):
        verts = [
            (0, 0, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 0, 1, 1),
        ]
        faces = [
            (0, 1),
            (0, 2),
            (0, 3),
        ]
        super().__init__(render, verts, faces)

        self.colors = [pygame.Color("red"), pygame.Color("green"), pygame.Color("blue")]
        self.color_faces = [
            (color, face) for color, face in zip(self.colors, self.faces)
        ]
        self.draw_vertices = False
        self.label = "XYZ"


class Cube(Object3D):
    def __init__(self, render: GameWindow):
        verts = [
            (0, 0, 0, 1),
            (0, 1, 0, 1),
            (1, 1, 0, 1),
            (1, 0, 0, 1),
            (0, 0, 1, 1),
            (0, 1, 1, 1),
            (1, 1, 1, 1),
            (1, 0, 1, 1),
        ]
        faces = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 4, 5, 1),
            (2, 3, 7, 6),
            (1, 2, 6, 5),
            (0, 3, 7, 4),
        ]
        super().__init__(render, verts, faces)
