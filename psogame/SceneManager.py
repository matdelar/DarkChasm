import pygame
from Scenes import *
import Database

class Manager:
    def __init__(self, screen,clock) -> None:
        self.screen = screen
        self.state = "menu"
        self.lastState = self.state
        self.database = Database.Database()
        self.scenes = {
                        "menu"  : Menu(screen,clock,self.database),
                        "play"  : Play(screen,clock,self.database),
                        "tuto"  : Tutorial(screen,clock,self.database),
                        "edit"  : Edit(screen,self.database),
                        "rank"  : Ranks(screen,self.database),
                       
                       }

    def run(self,event,dt):
        if self.state == "quit" or self.state ==None:
            pygame.quit()
        else:
            self.scenes[self.state].run(event,dt)
            self.state = self.scenes[self.state].get_State()
