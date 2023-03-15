import pygame
import SceneManager

class Button:
    def __init__(self,func,screen,pos,size,text,tcolor,slcolor,srcolor) -> None:
        self.screen = screen
        self.pos = pos
        self.size = size
        self.text = text
        self.tcolor = tcolor
        self.slcolor = slcolor
        self.srcolor = srcolor
        self.active = False
        self.func = func
        self.rect = pygame.Rect(pos,size)
        pygame.font.init()
        self.font = pygame.font.Font("assets/invasion2000.ttf",self.size[1])

    def gradientRect(self):
        fadeRect = pygame.Surface( ( 2, 2 ) )                                   
        fadeRect.set_at((0,0),self.slcolor)
        fadeRect.set_at((0,1),self.slcolor)
        fadeRect.set_at((1,0),self.srcolor)
        fadeRect.set_at((1,1),self.srcolor)
        fadeRect = pygame.transform.smoothscale( fadeRect, ( self.rect.width, self.rect.height ) )  # stretch!
        self.screen.blit( fadeRect, self.rect )   
    
    def draw(self):
        self.gradientRect() if self.active else True
        text1 = self.font.render(self.text, False, self.tcolor)
        self.screen.blit(text1, self.pos)
    
    def return_func(self):
        return self.func
    
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
    
        
        