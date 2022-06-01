import time
import pygame
import sys
from object_3d import Object3D


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
        self.object = Object3D(self)

    def draw(self):
        self.screen.fill(pygame.Color("darkslategray"))

    def run(self):
        self.dt = time.time() - self.last_time
        self.last_time = time.time()
        while True:
            self.draw()
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
