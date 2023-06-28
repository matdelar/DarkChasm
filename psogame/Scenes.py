import pygame 
from UI import *
from Entities import *
from Player import *
from Tiles import *
import LevelMaker

class Menu:
    def __init__(self,screen,clock,database) -> None:
        self.screen = screen
        self.clock = clock
        self.title = Title(self.screen,(152,50))
        self.background = Background(self.screen,[1/3,0])
        self.buttonPlay = Button("play", screen, (350,200), (100,30), "Iniciar",    (220,207,76),(150,100,150))
        self.buttonTuto = Button("tuto", screen, (350,240), (100,30), "Tutorial",   (220,207,76),(150,100,150))
        self.buttonEdit = Button("edit", screen, (350,280), (100,30), "Customizar", (220,207,76),(150,100,150))
        self.buttonRank = Button("rank", screen, (350,320), (100,30), "Rank",       (220,207,76),(150,100,150))
        self.buttonQuit = Button("quit", screen, (350,360), (100,30), "Sair",       (220,207,76),(150,100,150))
        self.buttons = [self.buttonPlay, self.buttonTuto,self.buttonEdit, self.buttonQuit,self.buttonRank]
        self.activeButton = 0
        self.newState = "menu"

    def run(self,event,dt):
        self.background.draw(dt)

        self.newState = "menu"
        for button in self.buttons:
            if button.mouse_isOver():
                button.set_active(True)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.newState = button.func
            else:
                button.set_active(False)
            
            button.draw()
        self.title.draw(dt)
    
    def get_State(self):
        return self.newState

class Play:
    def __init__(self,screen,clock,database) -> None:
        self.screen = screen
        self.clock = clock
        self.database = database
        self.scale = self.database.get_sprite_scale()
        self.maps = None
        self.newState = "play"
        self.timer = Timer(self.screen,self.clock,(3,30),0)
        self.player = Player(self.screen, (200,264),self.database)
        self.pauseMenu = PauseMenu(self.screen)
        self.scoreBoard = Text(self.screen,"0",(220,206,76),(10,10),32)
        self.points = 0

        self.map1 = LevelMaker.Generate_map((50,100))
        self.scroll = [0,0]
        self.tiles = []
        self.coins = []
        self.resetMap()
        self.doReset = False

    def run(self,event,dt):
        if self.doReset:
            self.resetMap()
            self.doReset = False

        self.newState = 'play'
        self.scroll[0] += (self.player.rect.topleft[0]-self.scroll[0]-400-8*self.scale)/20 
        self.scroll[1] += (self.player.rect.topleft[1]-self.scroll[1]-300-8*self.scale)/20
        
        self.tileUpdate()
        for t in self.tiles:
            t.draw(self.scroll)
        self.player.update(self.tiles,self.scroll,dt)
        self.player.draw(self.scroll)


        for c in self.coins:
            if pygame.Rect.colliderect(self.player.rect,c.get_rect()):
                self.points += c.get_value()
                self.coins.pop(self.coins.index(c))
            else:
                c.draw(self.scroll)

        self.scoreBoard.draw(self.points)
        if self.player.input.get_input('back'):
            self.newState = 'menu'
            self.doReset = True
    
    def resetMap(self):
        self.points = 0
        self.map1 = LevelMaker.Generate_map((50,100))
        self.scroll = [0,0]
        self.player.setPos((200,-16))
        self.tiles = []
        self.coins = []
        for y in range(len(self.map1)):
            for x in range(len(self.map1[y])):
                if self.map1[y][x] == 1:
                    self.tiles.append(Stone(self.screen,(x,y),self.database,4)) 
                elif self.map1[y][x] == 3:
                    self.coins.append(Coin(self.screen,(x*self.scale*16,y*self.scale*16),self.database))
    
    def tileUpdate(self):
        mousePos = pygame.mouse.get_pos()
        worldPos = (mousePos[0]+self.scroll[0])-(mousePos[0]+self.scroll[0])%(16*self.scale),(mousePos[1]+self.scroll[1])-(mousePos[1]+self.scroll[1])%(16*self.scale)
        hasNoTile = True
        for tile in self.tiles:
            if tile.get_rect().collidepoint(worldPos):
                hasNoTile = False
                if self.player.input.get_input('tileRemove',True):  
                    self.tiles.pop(self.tiles.index(tile))
        
        if hasNoTile and self.player.input.get_input('tilePlace',True): 
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
        self.sliderR = Slider(self.screen,(200,109),(200,100),(255,9),(18,18),(10,10,10),(255,0,0),255)
        self.sliderG = Slider(self.screen,(200,139),(200,130),(255,9),(18,18),(10,10,10),(255,0,0),255)
        self.sliderB = Slider(self.screen,(200,169),(200,160),(255,9),(18,18),(10,10,10),(255,0,0),255)
        self.buttonBack = Button("menu",self.screen,(10,10),(120,40),"Back",(255,255,255),(20,5,20))
        self.buttonSave = Button("menu",self.screen,(340,300),(120,40),"Salvar",(255,255,255),(20,5,20))
        self.player = Player(self.screen,(500,100),self.database) 
        self.sliders = [self.sliderR,self.sliderG,self.sliderB]
        self.newState = "edit"
        self.color = [0,0,0]
    
    def run(self,event,dt):
        self.newState = "edit"
        for s in self.sliders:
            s.update()
            s.draw()
            self.color[self.sliders.index(s)] = s.get_Value()
        
        #pygame.draw.rect(self.screen,(v[0],v[1],v[2]),(500,200,100,100))
        self.screen.blit(self.player.set_mask_color(self.player.get_sprite(),(self.color[0],self.color[1],self.color[2],255),(255,255,255,255)), (500,100,16,16))

        if self.buttonBack.mouse_isOver() and pygame.mouse.get_pressed()[0]:
            self.newState = self.buttonBack.get_func()
        self.buttonBack.draw()

        if self.buttonSave.mouse_isOver() and pygame.mouse.get_pressed()[0]:
            self.database.setColor(self.color)
            self.newState = self.buttonSave.get_func()
        self.buttonSave.draw()
        

    def get_State(self):
        return self.newState

class Ranks:
    def __init__(self,screen,database) -> None:
        self.screen = screen
        self.database = database
        self.rankData = self.database.getRanksAll()
        self.newState = "rank"
        self.offsetY = 100
        self.btnBack = Button("menu",screen,(48,16),(100,50),"Voltar",(220,206,76),(50,50,50))
        self.text = []
        if self.database.isOnline:
                for row in self.rankData:
                    try:
                        t1 = Text(self.screen,str(row[0]),(255,255,255),(300,100+self.offsetY+15*self.rankData.index(row)),20)
                        t2 = Text(self.screen,str(row[1]),(255,255,255),(400,100+self.offsetY+15*self.rankData.index(row)),20)
                        t2.setPos((400-t2.rect.w,100+self.offsetY+15*self.rankData.index(row)))
                        t3 = Text(self.screen,str(row[1]),(255,255,255),(400,100+self.offsetY+15*self.rankData.index(row)),20)
                        t3.setPos((500-t3.rect.w,100+self.offsetY+15*self.rankData.index(row)))
                        self.text.append(t1)
                        self.text.append(t2)
                        self.text.append(t3)
                    except:
                        pass
       
    def run(self,event,dt):
        self.newState = "rank"
        if len(self.text) != self.database.rankAmount:
            self.update()
        if self.btnBack.mouse_isOver() and pygame.mouse.get_pressed()[0]:
            self.newState = self.btnBack.get_func()
        self.btnBack.draw()
        for t in self.text:
            t.draw()

    def get_State(self):
        return self.newState

    def update(self):
        self.rankData = self.database.getRanksAll()
        self.text = []
        self.btnBack.set_active(self.btnBack.mouse_isOver())
        for row in self.rankData:
            t1 = Text(self.screen,str(row[0]),(220,206,76),(200,100+self.offsetY+15*self.rankData.index(row)),20)
            t2 = Text(self.screen,str(row[1]),(220,206,76),(400,100+self.offsetY+15*self.rankData.index(row)),20)
            t3 = Text(self.screen,str(row[2]),(220,206,76),(500,100+self.offsetY+15*self.rankData.index(row)),20)
            t2.setPos((400-t2.rect.w,100+self.offsetY+15*self.rankData.index(row)))
            t3.setPos((500-t3.rect.w,100+self.offsetY+15*self.rankData.index(row)))
            self.text.append(t1)
            self.text.append(t2)
            self.text.append(t3)

class Tutorial:
    def __init__(self,screen,clock,database) -> None:
        self.screen = screen
        self.clock = clock
        self.database = database
        self.pixelSize = self.database.get_sprite_scale()
        self.maps = None
        self.newState = "tuto"
        self.timer = Timer(self.screen,self.clock,(3,30),0)
        self.player = Player(self.screen, (200,364),self.database)
        self.pauseMenu = PauseMenu(self.screen)
        self.scoreBoard = Text(self.screen,"0",(255,0,0),(3,54),16)
        self.points = 0
        self.scale = self.database.get_sprite_scale()
        self.tutTexts = []
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(100,   500),10,self.database,"A e D: andar"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(500,   500),10,self.database,"pegue todos os blocos de ouro"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(1300,  500),10,self.database,"ESPACO: pular"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(1600,  400),10,self.database,"Segurar ESPACO: planar com o guarda-chuva"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(3650,  600),10,self.database,"E: usar o gancho"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(3650,  700),10,self.database,"o gancho vai na direcao do mouse"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(3850,  300),10,self.database,"Botao direito do mouse: remover bloco"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(3850,  400),10,self.database,"Botao esquerdo do mouse: colocar bloco"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(4500,  600),10,self.database,"Fim do tutorial!"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(4400, 1000),10,self.database,"Esc para salvar seu tempo e"))
        self.tutTexts.append(WorldText(self.screen,(220,207,76),(4400, 1030),10,self.database,"voltar ao menu"))

        self.escLock = False

        self.map1 = self.load_matrix("levels/tutorial.txt")
        self.scroll = [0,0]

        self.player.input.setKeyState('jump',False)
        self.player.input.setKeyState('action',False)
        self.player.input.setKeyState('tilePlace',False)
        self.player.input.setKeyState('tileRemove',False)


        self.coins = []
        self.tiles = []
        for y in range(len(self.map1)):
            for x in range(len(self.map1[y])):
                if self.map1[y][x] == 1:
                    self.tiles.append(Stone(self.screen,(x,y),self.database,4)) 
                elif self.map1[y][x] == 3:
                    self.coins.append(Coin(self.screen,(x*self.scale*16,y*self.scale*16),self.database))
        

    def run(self,event,dt):
        self.newState = 'tuto'
        self.scroll[0] += (self.player.rect.topleft[0]-self.scroll[0]-400-7*self.pixelSize)/20 
        self.scroll[1] += (self.player.rect.topleft[1]-self.scroll[1]-300-16*self.pixelSize)/20
        if self.player.pos[0]>1300:
            self.player.input.setKeyState('jump',True)
        if self.player.pos[0]>3650:
            self.player.input.setKeyState('action',True)
        if self.player.pos[0]>3850:
            self.player.input.setKeyState('tilePlace',True)
            self.player.input.setKeyState('tileRemove',True)
        
        for t in self.tiles:
            t.draw(self.scroll)
        self.player.update(self.tiles,self.scroll,dt)
        self.player.draw(self.scroll)

        #print(len(self.coins))

        if pygame.key.get_pressed()[pygame.K_ESCAPE] and not self.escLock:
            self.pauseMenu.setActive()
            self.escLock = True
            
        elif not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.escLock = False

        self.pauseMenu.run(event,self.timer.getTime())
        self.timer.toggleTimer(not self.pauseMenu.active)
        self.player.setCanMove(not self.pauseMenu.active)

        if self.pauseMenu.getSendClick() and self.pauseMenu.active and not self.mLock:
            self.mLock = True
            self.database.insertRank(self.pauseMenu.txtInput.text,self.timer.getTime(),self.points)
        
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
        for t in self.tutTexts:
            t.draw(self.scroll)

        if self.pauseMenu.active:
            self.pauseMenu.draw()
        
        if self.pauseMenu.btnBack.getClick() and self.pauseMenu.active:
            self.newState = self.pauseMenu.btnBack.get_func()
            self.restart()

    
    def tileUpdate(self):
        mousePos = pygame.mouse.get_pos()
        worldPos = (mousePos[0]+self.scroll[0])-(mousePos[0]+self.scroll[0])%(16*self.scale),(mousePos[1]+self.scroll[1])-(mousePos[1]+self.scroll[1])%(16*self.scale)
        hasNoTile = True
        for tile in self.tiles:
            if tile.get_rect().collidepoint(worldPos):
                hasNoTile = False
                if self.player.input.get_input('tileRemove',True):  
                    self.tiles.pop(self.tiles.index(tile))
        
        if hasNoTile and self.player.input.get_input('tilePlace',True): 
            self.tiles.append(Stone(self.screen,worldPos,self.database,4,worldPos))
                    

    def get_State(self):
        return self.newState
    
    def load_matrix(self,filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines]

        matrix = [[int(pixel) for pixel in line.split()] for line in lines]

        return matrix
    
    def restart(self):
        self.pauseMenu.active = False
        self.timer.time = 0
        self.player.setPos((200,364))
        self.player.input.setKeyState('jump',False)
        self.player.input.setKeyState('action',False)
        self.player.input.setKeyState('tilePlace',False)
        self.player.input.setKeyState('tileRemove',False)

        self.scroll = [0,0]
        self.coins = []
        self.tiles = []
        for y in range(len(self.map1)):
            for x in range(len(self.map1[y])):
                if self.map1[y][x] == 1:
                    self.tiles.append(Stone(self.screen,(x,y),self.database,4)) 
                elif self.map1[y][x] == 3:
                    self.coins.append(Coin(self.screen,(x*self.scale*16,y*self.scale*16),self.database))