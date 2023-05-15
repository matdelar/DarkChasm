import pygame

class Input:
    def __init__(self) -> None:
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.jump = pygame.K_SPACE
        self.hover = pygame.K_SPACE

    def get_axisX(self):
        return self.right-self.left
    