import pygame
from Scenes import *

class Manager:
    def __init__(self, screen,clock) -> None:
        self.screen = screen
        self.state = "menu"
        self.lastState = self.state
        self.sceneTrasition = Transition(self.screen,True,1,30)
        self.trasitionState = None
        self.scenes = [Menu(screen,clock),Play(screen,clock),Edit(screen)]

    def run(self):

        if self.state == None:
            print("Error: sceneState: null")
        elif self.state == "menu":
            self.scenes[0].run()
            self.state = self.scenes[0].get_State()
        elif self.state == "play":
            self.scenes[1].run()
            self.state = self.scenes[1].get_State()
        elif self.state == "edit":
            self.scenes[2].run()
            self.state = self.scenes[2].get_State()
        elif self.state == "quit":
            pygame.quit()

    def get_sprite_scale():
        return 2