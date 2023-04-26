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
        self.buttonPlay = Button("play",screen,(100,100),(100,20),"Play",(255,255,255),(200,200,200))
        self.buttonLoad = Button("load",screen,(100,130),(100,20),"Load",(255,255,255),(200,200,200))
        self.buttonEdit = Button("edit",screen,(100,160),(100,20),"Edit",(255,255,255),(200,200,200))
        self.buttonQuit = Button("quit",screen,(100,190),(100,20),"Quit",(255,255,255),(200,200,200))
        self.buttons = [self.buttonPlay, self.buttonLoad,self.buttonEdit, self.buttonQuit]
        self.activeButton = 0
        self.wRepeatLock = False
        self.sRepeatLock = False
        self.newState = "menu"

    def run(self):
        self.newState = "menu"
        for button in self.buttons:
            if button.mouse_isOver():
                button.set_active(True)
                if pygame.mouse.get_pressed()[0]:
                    self.newState = button.func
            else:
                button.set_active(False)
            
            button.draw()
    
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

        self.map1 = self.load_matrix("assets/levels/level1.txt")

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
            self.db.insertRank("a",self.timer.getTime())


        self.timer.update()
        self.timer.draw()

    def get_State(self):
        return self.newState
    
    def load_matrix(self,filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines]

        matrix = [[int(pixel) for pixel in line.split()] for line in lines]

        matrix = [[1 if pixel > 0 else 0 for pixel in row] for row in matrix]

        return matrix

class Edit:
    def __init__(self,screen) -> None:
        self.screen = screen
        self.sliderR = Slider(self.screen,(200,200),(200,200),(255,9),(18,18),(10,10,10),(255,0,0),255)
        self.sliderG = Slider(self.screen,(200,230),(200,230),(255,9),(18,18),(10,10,10),(255,0,0),255)
        self.sliderB = Slider(self.screen,(200,260),(200,260),(255,9),(18,18),(10,10,10),(255,0,0),255)
        self.buttonBack = Button("menu",self.screen,(10,10),(100,50),"Back",(255,255,255),(20,5,20))
        self.p = Player(self.screen,(500,200))
        self.sliders = [self.sliderR,self.sliderG,self.sliderB]
        self.newState = "edit"
    
    def run(self):
        v = [0,0,0]
        for s in self.sliders:
            s.update()
            s.draw()
            v[self.sliders.index(s)] = s.get_Value()
        
        #pygame.draw.rect(self.screen,(v[0],v[1],v[2]),(500,200,100,100))
        self.screen.blit(self.p.set_mask_color(self.p.get_sprite(),(v[0],v[1],v[2],255),(255,v[1],0,255)), (500,200,16,16))

        x,y = pygame.mouse.get_pos()
        if pygame.rect.Rect.collidepoint(self.buttonBack.rect,x,y):
            self.buttonBack.active = True
            if pygame.mouse.get_pressed()[0]:
                self.newState = self.buttonBack.get_func()
        else:
            self.buttonBack.active = False
        self.buttonBack.draw()
        

    def get_State(self):
        return self.newState