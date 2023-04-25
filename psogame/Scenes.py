import pygame 
from UI import *
from Entities import *
from Player import *
from Tiles import *
import SceneManager
import Database

class Menu:
    def __init__(self,screen,clock) -> None:
        self.screen = screen
        self.clock = clock
        self.buttonPlay = Button("play",screen,(100,100),(100,20),"Play",(255,255,255),(200,200,200),(10,10,10))
        self.buttonLoad = Button("load",screen,(100,130),(100,20),"Load",(255,255,255),(200,200,200),(10,10,10))
        self.buttonQuit = Button("quit",screen,(100,160),(100,20),"Quit",(255,255,255),(200,200,200),(10,10,10))
        self.buttons = [self.buttonPlay, self.buttonLoad, self.buttonQuit]
        self.activeButton = 0
        self.wRepeatLock = False
        self.sRepeatLock = False
        self.newState = "menu"

    def run(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and not self.wRepeatLock and self.activeButton > 0:
            self.activeButton -=1
            self.wRepeatLock = True
        elif keys[pygame.K_s] and not self.sRepeatLock and self.activeButton < 2:
            self.activeButton +=1
            self.sRepeatLock = True
        elif keys[pygame.K_f]:
            self.newState = self.buttons[self.activeButton].return_func()
        
        if not keys[pygame.K_w]:
            self.wRepeatLock = False
        if not keys[pygame.K_s]:
            self.sRepeatLock = False
        
        for b in self.buttons:
            if self.buttons.index(b) == self.activeButton:
                b.active = True
            else:
                b.active = False
            b.draw()
    
    def get_State(self):
        return self.newState

class Play:

    def __init__(self,screen,clock) -> None:
        self.screen = screen
        self.clock = clock
        self.pixelSize = SceneManager.Manager.get_sprite_scale()
        self.maps = None
        self.newState = "play"
        self.timer = Timer(self.screen,self.clock,(1*self.pixelSize,10*self.pixelSize),0)
        self.p = Player(self.screen, (32,64))
        self.a = TownMage(self.screen,(128,64))
        self.db = Database.Database()
        
        self.xLock = False

        self.map1 = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]

        self.scroll = [0,0]

        self.tiles = []
        for y in range(len(self.map1)):
            for x in range(len(self.map1[y])):
                if self.map1[y][x] == 1:
                    self.tiles.append(Stone(self.screen,(x,y),4)) 
                    
        nmap = self.map1

        nmap = [[0] * (len(nmap[0]) + 2)] + [[0] + row + [0] for row in nmap] + [[0] * (len(nmap[0]) + 2)]

        for tile in self.tiles:
            tile.set_type(nmap)


    def run(self):
        self.scroll[0] += (self.p.rect.topleft[0]-self.scroll[0]-400-7*self.pixelSize)/20 
        self.scroll[1] += (self.p.rect.topleft[1]-self.scroll[1]-300-16*self.pixelSize)/20
        for tile in self.tiles:
            tile.draw(self.scroll)
        
        self.p.update(self.tiles,self.scroll)
        self.p.draw(self.scroll)

        if pygame.key.get_pressed()[pygame.K_x] and not self.xLock:
            self.xLock = True
            self.db.insertRank("a",str(self.timer.time))


        self.timer.update()
        self.timer.draw()

    def get_State(self):
        return self.newState
