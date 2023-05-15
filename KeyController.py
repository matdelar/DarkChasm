import pygame

class Input:
    def __init__(self) -> None:
        self.keys = {
            'left' : pygame.K_a,
            'right' : pygame.K_d,
            'jump' :  pygame.K_SPACE,
            'action' :  pygame.K_SPACE,
            'back' : pygame.K_ESCAPE
        }

    def get_input(self,key):
        keyPressed = pygame.key.get_pressed()
        return keyPressed[self.keys[key]]
    
    def set_input(self,key,value):
        self.keys[key] = value

    def reset_key(self):
        self.keys = {
            'left' : pygame.K_a,
            'right' : pygame.K_d,
            'jump' :  pygame.K_SPACE,
            'action' :  pygame.K_SPACE,
            'back' : pygame.K_ESCAPE
        }