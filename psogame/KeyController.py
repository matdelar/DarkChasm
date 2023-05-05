import pygame

class Controller:
    def __init__(self) -> None:
        self.leftKey = pygame.K_a
        self.rightKey = pygame.K_d
        self.jumpKey = pygame.K_SPACE

    def get_axisX(self):
        return self.rightKey-self.leftKey