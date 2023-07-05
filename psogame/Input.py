import pygame

class Input:
    def __init__(self) -> None:
        self.keys = {
            'left' : pygame.K_a,
            'right' : pygame.K_d,
            'jump' :  pygame.K_SPACE,
            'action' :  pygame.K_e,
            'back' : pygame.K_ESCAPE,
            'tilePlace' : 0,
            'tileRemove' : 2
        }
        self.keyActive = {
            'left'  : True,
            'right' : True,
            'jump'  : True,
            'action': True,
            'back'  : True,
            'tilePlace' : True,
            'tileRemove' : True
        }
        self.isActive = True

    def get_input(self,key,isMouse=False):
        if isMouse:
            return pygame.mouse.get_pressed()[self.keys[key]] and self.keyActive[key]
        else:
            return pygame.key.get_pressed()[self.keys[key]]  and self.keyActive[key]
    
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
            'action' :  pygame.K_e,
            'back' : pygame.K_ESCAPE,
            'tilePlace' : 0,
            'tileRemove' : 2
        }
    def setKeyState(self,key,state=None):
        if state:
            self.keyActive[key] = state
        else:
            self.keyActive[key] = not self.keyActive[key]