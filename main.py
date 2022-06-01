import time
import pygame
import sys
from object_3d import Axes, Object3D
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
        self.fps = 60

        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])

        # draw axes XYZ in cube projection
        self.axes = Axes(self)
        self.axes.translate([0.7, 0.9, 0.7])

        # draw world XYZ axes
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False
        self.world_axes.scale(2.5)
        self.world_axes.translate([0.0001, 0.0001, 0.0001])

    def draw(self):
        self.screen.fill(pygame.Color("darkslategray"))
        self.object.draw()
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
