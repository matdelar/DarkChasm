import pygame

class Input:
    def __init__(self) -> None:
        self.keys = {
            'left' : pygame.K_a,
            'right' : pygame.K_d,
            'jump' :  pygame.K_SPACE,
            'action' :  pygame.K_e,
            'back' : pygame.K_ESCAPE
        }
        self.isActive = True

    def get_input(self,key):
        keyPressed = pygame.key.get_pressed()
        if not self.isActive:
            return False
        return keyPressed[self.keys[key]] 
    
    def set_input(self,key,value):
        self.keys[key] = value
    
    def toggleInput(self,newState = None):
        if newState != None:
            self.isActive = newState
        else:
            self.isActive = not self.isActive

    def reset_key(self):
        self.keys = {
            'left' : pygame.K_a,
            'right' : pygame.K_d,
            'jump' :  pygame.K_SPACE,
            'action' :  pygame.K_SPACE,
            'back' : pygame.K_ESCAPE
        }
