import pygame
import SceneManager

class Button:
    def __init__(self,func,screen,pos,size,text,textColor,color) -> None:
        self.screen = screen
        self.pos = pos
        self.size = size
        self.text = text
        self.tcolor = textColor
        self.color = color
        self.active = False
        self.func = func
        self.rect = pygame.Rect(pos,size)
        pygame.font.init()
        self.font = pygame.font.Font("assets/invasion2000.ttf",self.size[1])
    
    def selected_draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect)

    def draw(self):
        self.selected_draw() if self.active else True
        text1 = self.font.render(self.text, False, self.tcolor)
        self.screen.blit(text1, self.pos)
    
    def get_func(self):
        return self.func
    
    def mouse_isOver(self):
        m = pygame.mouse.get_pos()
        return self.rect.collidepoint(m[0], m[1])
    
    def set_active(self, nstate = None):
        if nstate == None:
            self.active = not self.active
        else:
            self.active = nstate
            
class Transition:
    def __init__(self,screen,auto = True,timeins = 2,spacing=24) -> None:
        self.screen = screen
        self.scale = SceneManager.Manager.get_sprite_scale()
        self.auto = auto
        self.totalFrames = timeins*60
        self.frameCount = 0
        self.circleSizeIncrease = spacing/self.totalFrames
        self.circleSizeActual = self.circleSizeIncrease
        self.spacing = spacing
        self.xAmount = int(self.screen.get_width()//spacing)+3
        self.yAmount = int(self.screen.get_height()//spacing)+3
    
    def run(self):
        self.frameCount += 1
        if self.frameCount < self.totalFrames:
            self.circleSizeActual += self.circleSizeIncrease
            self.draw()
            return "on"
        elif self.auto:
            self.circleSizeActual -= self.circleSizeIncrease if self.circleSizeActual - self.circleSizeIncrease > 0 else 0
            self.draw()
            return "off"
        elif pygame.key.get_pressed()[pygame.K_x]:
            self.auto = 1
            self.draw()
            return "waiting"
        
    def draw(self):
        for x in range(self.xAmount):
            for y in range(self.yAmount):
                pygame.draw.circle(self.screen,(0,0,0), [x*self.spacing,y*self.spacing], self.circleSizeActual)
    
class Timer:
    def __init__(self,screen,clock,pos,time = 0) -> None:
        self.screen = screen
        self.clock = clock
        self.time = time
        self.pos = pos
        pygame.font.init()
        #self.size = size[0],size[1]
        self.font = pygame.font.Font("assets/invasion2000.ttf",18)
    
    def update(self):
        self.time += self.clock.get_time()/1000

    def draw(self):
        pygame.draw.rect(self.screen,(50,10,50),((self.pos[0],self.pos[1]),(100,30)))
        text1 = self.font.render(str(round(self.time,3)), False, (240,10,20))
        self.screen.blit(text1, self.pos)
    
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
    def __init__(self,screen,pos,size,color,fontColor,maxTextLength=0) -> None:
        self.screen = screen
        self.pos = pos
        self.size = size
        self.text = ""
        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.color = color
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
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.fontColor)
        
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        if self.active:
            pygame.draw.rect(self.screen, self.color, self.rect, width=0)
        else:
            pygame.draw.rect(self.screen, self.fontColor, self.rect, width=0)
        
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))


