import pygame
from math import *

class Button:
    def __init__(self,func,screen,pos,size,text,textColor,color) -> None:
        self.screen = screen
        self.pos = pos
        self.size = size
        self.text = text
        self.textColor = textColor
        self.color = color
        self.active = False
        self.func = func
        self.rect = pygame.Rect(pos,size)
        pygame.font.init()
        self.font = pygame.font.Font("assets/invasion2000.ttf",int(self.size[1]*0.9))
        self.txt_surface = self.font.render(self.text, True, self.textColor)
        self.textPos = self.pos[0]+self.size[0]/2-self.txt_surface.get_width()/2,self.pos[1]
        
        self.rect.w = self.txt_surface.get_width()
        self.rect.topleft = self.textPos
    
    def selected_draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect,0)

    def draw(self):
        self.selected_draw() if self.active else True
        text1 = self.font.render(self.text, False, self.textColor)
        self.screen.blit(text1, self.textPos)
    
    def get_func(self):
        return self.func
    
    def mouse_isOver(self):
        m = pygame.mouse.get_pos()
        return self.rect.collidepoint(m[0], m[1])

    def getClick(self):
        return self.mouse_isOver() and pygame.mouse.get_pressed()[0]
            
    
    def set_active(self, nstate = None):
        if nstate == None:
            self.active = not self.active
        else:
            self.active = nstate
            
class Timer:
    def __init__(self,screen,clock,pos,time = 0) -> None:
        self.screen = screen
        self.clock = clock
        self.time = time
        self.pos = pos
        self.isActive = True
        pygame.font.init()
        self.font = pygame.font.Font("assets/invasion2000.ttf",18)
    
    def update(self):
        self.time += self.clock.get_time()/1000 * self.isActive

    def draw(self):
        pygame.draw.rect(self.screen,(50,10,50),((self.pos[0],self.pos[1]),(100,30)))
        text1 = self.font.render(str(round(self.time,3)), False, (240,10,20))
        self.screen.blit(text1, self.pos)
    
    def toggleTimer(self,newState = None):
        if newState != None:
            self.isActive = newState
        else:
            self.isActive = not self.isActive

    def getTime(self):
        return str(round(self.time,3))

class Slider:
    def __init__(self,screen,pos,handlePos,size,handleSize,sliderColor,handleColor,maxvalue = 255) -> None:
        self.screen = screen
        self.pos = pos
        self.size = size
        self.range = maxvalue
        self.sliderColor = sliderColor
        self.handleColor = handleColor
        self.handlePos = handlePos
        self.handleSize = handleSize
        self.isMouseOver = False
        self.isMouseClick = False
        self.lock = False
        self.value = 0
        self.handleRect = pygame.Rect(self.handlePos[0],self.handlePos[1],handleSize[0],self.handleSize[1])
    
    def update(self):
        x,y = pygame.mouse.get_pos()
        nrect = pygame.Rect(self.handlePos[0],self.handlePos[1],self.handleSize[0],self.handleSize[1])
        self.isMouseOver = pygame.rect.Rect.collidepoint(nrect,x,y)
        self.isMouseClick = pygame.mouse.get_pressed()[0]
        if (self.lock or self.isMouseOver) and self.isMouseClick:
            newX = x
            if newX < self.pos[0]:
                newX = self.pos[0]
            if newX > self.size[0]+self.pos[0]:
                newX = self.size[0]+self.pos[0]

            self.handlePos = newX,self.handlePos[1]
            self.lock = True
        elif not self.isMouseClick:
            self.lock = False

        if self.isMouseOver:
            self.handleColor = (0,255,0)
        else:
            self.handleColor = (255,0,0)

        self.handleRect.update(self.handlePos[0],self.handlePos[1],self.handleSize[0],self.handleSize[1])

        self.value = self.handlePos[0]-self.pos[0]

    def draw(self):
        pygame.draw.rect(self.screen,self.sliderColor,(self.pos,self.size))
        pygame.draw.rect(self.screen,self.handleColor,self.handleRect)
        pygame.draw.rect(self.screen,(0,255,0),(self.handlePos,self.handleSize),3)

    def get_Value(self):
        return self.value
    
class TextInput:
    def __init__(self,screen,pos,size,color,colorActive,fontColor,maxTextLength=0) -> None:
        self.screen = screen
        self.pos = pos
        self.size = size
        self.text = ""
        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.color = color
        self.colorActive = colorActive
        self.fontColor = fontColor
        pygame.font.init()
        self.font = pygame.font.Font("assets/invasion2000.ttf",self.size[1])
        self.txt_surface = self.font.render(self.text, True, self.fontColor)
        self.length = maxTextLength
        self.active = False
    
    def update(self,event):
        mouseClick = pygame.mouse.get_pressed()[0]
        mousePos = pygame.mouse.get_pos()

        if mouseClick:
            self.active = self.rect.collidepoint(mousePos[0],mousePos[1]) 
        
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.fontColor)
        
        width = max(self.size[0], self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        if self.active:
            pygame.draw.rect(self.screen, self.colorActive, self.rect, width=0)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect, width=0)
        
        self.screen.blit(self.txt_surface,self.rect)

class Text:
    def __init__(self,screen,text,color,pos,fontSize) -> None:
        self.screen = screen
        self.text = text 
        self.color = color 
        self.pos = pos 
        self.fontSize = fontSize 
        
        pygame.font.init()
        self.font = pygame.font.Font("assets/invasion2000.ttf",self.fontSize)
        self.txt_surface = self.font.render(str(self.text), True, self.color)
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.txt_surface.get_width(),self.fontSize)
    
    def draw(self,newText=None):
        if newText != None:
            newTxt_surface = self.font.render(str(newText), True, self.color)    
            newRect = pygame.Rect(self.pos[0],self.pos[1],newTxt_surface.get_width(),self.fontSize) 
            self.screen.blit(newTxt_surface,newRect)
        else:
            self.screen.blit(self.txt_surface,self.rect)
    
    def setPos(self,pos):
        self.rect.update(pos,self.rect.size)

class PauseMenu:
    def __init__(self,screen) -> None:
        self.screen = screen
        self.pos = (250,150)
        self.size = (300,300)
        self.color = (30,20,30)
        self.active = False
        pygame.font.init()
        self.font = pygame.font.Font("assets/invasion2000.ttf",30)
        self.txt_surface = self.font.render("0", True, (255,255,255))
        self.txtInput = TextInput(self.screen,(340,200),(120,30),(50,30,50),(70,20,70),(255,255,255))
        self.btnSend = Button("insertRank",self.screen,(350,300),(100,30),("Enviar"),(255,255,255),(202,207,76))
        self.btnBack = Button("menu",self.screen,(350,270),(100,30),("Voltar ao Menu"),(255,255,255),(202,207,76))
        self.sendClick = False
    
    def run(self,event,time):
        if self.active:
            pygame.draw.rect(self.screen,self.color,(self.pos[0],self.pos[1],self.size[0],self.size[1]))
            self.txtInput.update(event)

            self.txt_surface = self.font.render(time, True, (255,255,255))
            self.screen.blit(self.txt_surface,(400-self.txt_surface.get_width()/2,230,100,30))
            if self.btnSend.mouse_isOver():
                self.btnSend.set_active(True)
            else:
                self.btnSend.set_active(False)
            
            if self.btnBack.mouse_isOver():
                self.btnBack.set_active(True)
            else:
                self.btnBack.set_active(False)
    
    def draw(self):
        self.txtInput.draw()
        self.btnSend.draw()
        self.btnBack.draw()

    def setActive(self):
        self.active = not self.active
    
    def getTextActive(self):
        return self.txtInput.active
    
    def getSendClick(self):
       return pygame.mouse.get_pressed()[0] and self.btnSend.mouse_isOver()

class Title:
    def __init__(self,screen,pos) -> None:
        self.screen = screen
        self.sprite = pygame.image.load("assets/ui/menu/title2.png").convert_alpha()
        self.size = self.sprite.get_size()
        self.rect = self.sprite.get_rect()
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.scale = 4
        self.time = 0
        self.image = pygame.transform.scale(self.sprite, (self.size[0]*self.scale, self.size[1]*self.scale))
    
    def draw(self,dt):
        self.time += dt * 1/20
        self.rect.y = self.pos[1]+cos(self.time)*10


        self.screen.blit(self.image,self.rect)

class Background:
    def __init__(self,screen,staticSpeed) -> None:
        self.screen = screen
        self.pos = [0,0]
        self.sprite = pygame.image.load("assets/ui/menu/spike.png").convert_alpha()
        self.size = self.sprite.get_size()
        self.rect = self.sprite.get_rect()
        self.speed = staticSpeed
        self.scale = 4
        self.sprite = pygame.transform.scale(self.sprite, (self.size[0]*self.scale, self.size[1]*self.scale))
        

    def draw(self,dt,dinamicSpeed=[0,0]):
        self.pos[0] += (self.speed[0]+dinamicSpeed[0])*dt
        self.rect.x = self.pos[0]

        infRect = pygame.Rect(self.pos[0]-self.size[0]*self.scale,self.pos[1],self.size[0]*self.scale,self.size[1]*self.scale)
        infRect2 = pygame.Rect(self.pos[0]+self.size[0]*self.scale,self.pos[1],self.size[0]*self.scale,self.size[1]*self.scale)

        if self.pos[0] > self.size[0]*self.scale:
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = self.size[0]*self.scale


        self.screen.blit(self.sprite,self.rect)
        self.screen.blit(self.sprite,infRect)
        self.screen.blit(self.sprite,infRect2)

class WorldText:
    def __init__(self,screen,color,worldPos,fontSize,database,text) -> None:
        self.screen = screen
        self.database = database
        self.text = text
        self.color = color
        self.pos = worldPos
        self.scale = self.database.get_sprite_scale()
        self.sizeY = fontSize*self.scale
        pygame.font.init()
        self.font = pygame.font.Font("assets/invasion2000.ttf",self.sizeY)
        self.txtRender = self.font.render(self.text,True,self.color)
        self.size = self.txtRender.get_rect().width,self.txtRender.get_rect().height
        self.txtRender = self.font.render(self.text,True,self.color)
    
    def draw(self,scroll):
        npos = self.pos[0]-scroll[0],self.pos[1]-scroll[1]
        self.screen.blit(self.txtRender,npos)

