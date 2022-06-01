import math
import numpy as np


def translate(pos):
    tx, ty, tx = pos

    return np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [tx, ty, tx, 1],
        ]
    )


def rotate_x(alpha):
    return np.array(
        [
            [1, 0, 0, 0],
            [0, math.cos(alpha), math.sin(alpha), 0],
            [0, -math.sin(alpha), math.cos(alpha), 0],
            [0, 0, 0, 1],
        ]
    )


def rotate_y(alpha):
    return np.array(
        [
            [math.cos(alpha), 0, -math.sin(alpha), 0],
            [0, 1, 0, 0],
            [math.sin(alpha), 0, math.cos(alpha), 0],
            [0, 0, 0, 1],
        ]
    )


def rotate_z(alpha):
    return np.array(
        [
            [math.cos(alpha), math.sin(alpha), 0, 0],
            [-math.sin(alpha), math.cos(alpha), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


def scale(n):
    return np.array(
        [
            [n, 0, 0, 0],
            [0, n, 0, 0],
            [0, 0, n, 0],
            [0, 0, 0, 1],
        ]
    )
