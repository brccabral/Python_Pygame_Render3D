import time
import pygame
import sys
from object_3d import Axes, Cube, Object3D
from camera import Camera
from projection import Projection


class GameWindow:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1600, 900
        self.center_width = self.width // 2
        self.center_height = self.height // 2
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        self.dt = 0
        self.fps = 120

        self.axes = None
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [-5, 5, -50])
        self.projection = Projection(self)
        self.object = self.get_object_from_file("assets/tank_T-34-85/t_34_obj.obj")
        self.object.draw_vertices = False  # increases fps
        # self.create_axes_and_cube()

    def create_axes_and_cube(self):
        self.object = Cube(self)
        self.object.translate([0.2, 0.4, 0.2])

        # draw axes XYZ in cube projection
        self.axes = Axes(self)
        self.axes.translate([0.7, 0.9, 0.7])

        # draw world XYZ axes
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False
        self.world_axes.scale(2.5)
        self.world_axes.translate([0.0001, 0.0001, 0.0001])

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith("v "):
                    # v  0.0330 13.0139 9.3289
                    # file has xyz and we add w = [x y z] + [w]
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith("f"):
                    # f 30/36/24 42/60/36 43/61/37 31/37/25
                    faces_ = line.split()[1:]  # remove f
                    faces.append([int(face_.split("/")[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pygame.Color("darkslategray"))
        self.object.draw()
        if self.axes:
            self.axes.draw()
            self.world_axes.draw()

    def run(self):
        self.dt = time.time() - self.last_time
        self.last_time = time.time()
        while True:
            self.draw()
            self.camera.control(self.dt)
            for event in pygame.event.get([pygame.QUIT]):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.set_caption(f"Render 3D {self.clock.get_fps():.2f}")
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = GameWindow()
    game.run()
