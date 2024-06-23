import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()

class Capture:
    def __init__(self):
        self.size = (640, 480)
        self.display = pygame.display.set_mode(self.size)
        
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()
        
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        self.display.blit(self.snapshot, (0, 0))
        pygame.display.flip()

    def main(self):
        going = True
        while going:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.cam.stop()
                    going = False

            self.get_and_flip()

if __name__ == "__main__":
    capture = Capture()
    capture.main()
