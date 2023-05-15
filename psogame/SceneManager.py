import pygame
from Scenes import *

class Manager:
    def __init__(self, screen,clock) -> None:
        self.screen = screen
        self.state = "menu"
        self.lastState = self.state
        self.sceneTrasition = Transition(self.screen,True,1,30)
        self.trasitionState = None
        self.scenes = [Menu(screen,clock),
                       Play(screen,clock),
                       Edit(screen),
                       Login(screen)]

        self.scenes = {
                        "menu"  : Menu(screen,clock),
                        "play"  : Play(screen,clock),
                        "edit"  : Edit(screen),
                        "login" : Login(screen)
                       
                       }

    def run(self,event):
        if self.state == "quit" or self.state ==None:
            pygame.quit()
        else:
            self.scenes[self.state].run(event)
            self.state = self.scenes[self.state].get_State()

    def get_sprite_scale():
        return 3