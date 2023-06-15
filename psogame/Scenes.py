import pygame 
from UI import *
from Entities import *
from Player import *
from Tiles import *
import SceneManager
import Database
import LevelMaker

class Menu:
    def __init__(self,screen,clock,database) -> None:
        self.screen = screen
        self.clock = clock
        self.title = Title(self.screen,(200,50))
        self.background = Background(self.screen,[1/3,0])
        self.buttonPlay = Button("play", screen, (350,170), (100,20), "Play", (255,255,255),(200,200,200))
        self.buttonLoad = Button("load", screen, (350,200), (100,20), "Load", (255,255,255),(200,200,200))
        self.buttonEdit = Button("edit", screen, (350,230), (100,20), "Edit", (255,255,255),(200,200,200))
        self.buttonLogn = Button("login",screen, (350,260), (100,20), "Login",(255,255,255),(200,200,200))
        self.buttonQuit = Button("quit", screen, (350,290), (100,20), "Quit", (255,255,255),(200,200,200))
        self.buttons = [self.buttonPlay, self.buttonLoad,self.buttonEdit, self.buttonQuit,self.buttonLogn]
        self.activeButton = 0
        self.newState = "menu"

    def run(self,event):
        self.background.draw()

        self.newState = "menu"
        for button in self.buttons:
            if button.mouse_isOver():
                button.set_active(True)
                if pygame.mouse.get_pressed()[0]:
                    self.newState = button.func
            else:
                button.set_active(False)
            
            button.draw()
        self.title.draw()
    
    def get_State(self):
        return self.newState

class Play:
    def __init__(self,screen,clock,database) -> None:
        self.screen = screen
        self.clock = clock
        self.database = database
        self.pixelSize = self.database.get_sprite_scale()
        self.maps = None
        self.newState = "play"
        self.timer = Timer(self.screen,self.clock,(1*self.pixelSize,10*self.pixelSize),0)
        self.player = Player(self.screen, (200,264),self.database)
        self.pauseMenu = PauseMenu(self.screen)
        self.scoreBoard = Text(self.screen,"0",(255,0,0),(1*self.pixelSize,18*self.pixelSize),16)
        self.points = 0
        self.scale = self.database.get_sprite_scale()
        
        self.coins = []

        self.escLock = False

        self.map1 = LevelMaker.Generate_map((50,100))

        self.scroll = [0,0]

        self.tiles = []
        for y in range(len(self.map1)):
            for x in range(len(self.map1[y])):
                if self.map1[y][x] == 1:
                    self.tiles.append(Stone(self.screen,(x,y),self.database,4)) 
                elif self.map1[y][x] == 3:
                    self.coins.append(Coin(self.screen,(x*self.scale*16,y*self.scale*16),self.database))


    def run(self,event):
        self.scroll[0] += (self.player.rect.topleft[0]-self.scroll[0]-400-7*self.pixelSize)/20 
        self.scroll[1] += (self.player.rect.topleft[1]-self.scroll[1]-300-16*self.pixelSize)/20
        
        for tile in self.tiles:
            tile.draw(self.scroll)
        
        
        self.player.update(self.tiles,self.scroll)
        self.player.draw(self.scroll)


        if pygame.key.get_pressed()[pygame.K_ESCAPE] and not self.escLock:
            self.escLock = True
            self.pauseMenu.setActive()
            self.timer.toggleTimer()
            self.player.input.toggleInput()
        elif not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.escLock = False

        self.pauseMenu.run(event,self.timer.getTime())

        if self.pauseMenu.getSendClick() and self.pauseMenu.active and not self.mLock:
            self.mLock = True
            self.database.insertRank(self.pauseMenu.txtInput.text,self.timer.getTime())
        
        elif not self.pauseMenu.getSendClick():
            self.mLock = False

        self.timer.update()
        self.timer.draw()
        self.scoreBoard.draw(self.points)

        for c in self.coins:
            if pygame.Rect.colliderect(self.player.rect,c.get_rect()):
                self.points += c.get_value()
                self.coins.pop(self.coins.index(c))
            else:
                c.draw(self.scroll)

        self.tileUpdate()
    
    def tileUpdate(self):
        mousePos = pygame.mouse.get_pos()
        worldPos = (mousePos[0]+self.scroll[0])-(mousePos[0]+self.scroll[0])%(16*self.scale),(mousePos[1]+self.scroll[1])-(mousePos[1]+self.scroll[1])%(16*self.scale)
        hasNoTile = True
        for tile in self.tiles:
            if tile.get_rect().collidepoint(worldPos):
                hasNoTile = False
                if pygame.mouse.get_pressed()[2]:  
                    self.tiles.pop(self.tiles.index(tile))
        
        if hasNoTile and pygame.mouse.get_pressed()[0]: 
            self.tiles.append(Stone(self.screen,worldPos,self.database,4,worldPos))
                    

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
    def __init__(self,screen,database) -> None:
        self.screen = screen
        self.database = database
        self.sliderR = Slider(self.screen,(200,100),(200,100),(255,9),(18,18),(10,10,10),(255,0,0),255)
        self.sliderG = Slider(self.screen,(200,130),(200,130),(255,9),(18,18),(10,10,10),(255,0,0),255)
        self.sliderB = Slider(self.screen,(200,160),(200,160),(255,9),(18,18),(10,10,10),(255,0,0),255)
        self.buttonBack = Button("menu",self.screen,(10,10),(120,40),"Back",(255,255,255),(20,5,20))
        self.buttonSave = Button("menu",self.screen,(340,300),(120,40),"Salvar",(255,255,255),(20,5,20))
        self.player = Player(self.screen,(500,100),self.database) 
        self.sliders = [self.sliderR,self.sliderG,self.sliderB]
        self.newState = "edit"
        self.color = [0,0,0]
    
    def run(self,event):
        for s in self.sliders:
            s.update()
            s.draw()
            self.color[self.sliders.index(s)] = s.get_Value()
        
        #pygame.draw.rect(self.screen,(v[0],v[1],v[2]),(500,200,100,100))
        self.screen.blit(self.player.set_mask_color(self.player.get_sprite(),(self.color[0],self.color[1],self.color[2],255),(255,255,255,255)), (500,100,16,16))

        x,y = pygame.mouse.get_pos()
        if self.buttonBack.mouse_isOver() and pygame.mouse.get_pressed()[0]:
            self.newState = self.buttonBack.get_func()
            self.newState = "menu"
        self.buttonBack.draw()

        if self.buttonSave.mouse_isOver() and pygame.mouse.get_pressed()[0]:
            self.database.setColor(self.color)
            self.newState = "menu"
        self.buttonSave.draw()
        

    def get_State(self):
        return self.newState

class Login:
    def __init__(self,screen,database) -> None:
        self.screen = screen
        self.loginInfo = None
        self.nickText = TextInput(self.screen,(300,200),(200,15),(50,30,50),(70,20,70),(255,255,255))
        self.emailText = TextInput(self.screen,(300,220),(200,15),(50,30,50),(70,20,70),(255,255,255))
        self.passwordText = TextInput(self.screen,(300,240),(200,15),(50,30,50),(70,20,70),(255,255,255))
        self.newState = "login"
    
    def run(self,event):
        self.nickText.update(event)
        self.passwordText.update(event)
        self.emailText.update(event)

        self.nickText.draw()
        self.passwordText.draw()
        self.emailText.draw()
    
    def get_State(self):
        return self.newState