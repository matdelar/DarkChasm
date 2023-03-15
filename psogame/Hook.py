import pygame
import math
import SceneManager

class Hook:
    def __init__(self, screen, pos, angle) -> None:
        self.screen = screen
        self.pos = pos
        self.angle = angle
        self.returnSpeed = 16
        self.fowardSpeed = 8
        self.state = "moving"
        self.scale = SceneManager.Manager.get_sprite_scale()
        self.size = [8*self.scale,8*self.scale]
        self.ropeSize = [4*self.scale,4*self.scale]
        self.ropeSpacing = 1*self.scale
        self.hookSprite = pygame.image.load("assets/misc/hook/hook_graple.png")
        self.ropeSprite = pygame.image.load("assets/misc/hook/hook_rope.png")
        self.rect = pygame.rect.Rect((self.pos[0],self.pos[1]),(self.size[0],self.size[0]))
        self.distance = 0
        self.hookAngle = 0

    def update(self,tiles,plrpos):
        self.distance = math.sqrt((plrpos[0]-self.pos[0]+7*self.scale)**2+(plrpos[1]-self.pos[1]+16*self.scale)**2)
        self.hookAngle = math.atan2(plrpos[1]-self.pos[1]+16*self.scale,plrpos[0]-self.pos[0]+7*self.scale)
        if self.state == "moving":
            self.pos = self.pos[0]+self.fowardSpeed*math.cos(self.angle)*self.scale, self.pos[1]+self.fowardSpeed*math.sin(self.angle)*self.scale
            for tile in tiles:
                if self.rect.colliderect(tile.get_rect()):
                    self.state = "attached"

        elif self.state == "retracted":
            self.pos =  self.pos[0]+(self.returnSpeed*math.cos(self.hookAngle)*self.scale), self.pos[1]+self.returnSpeed*math.sin(self.hookAngle)*self.scale
            if self.distance <= 24: # distance should be less than backspd to avoid bugs
                self.state = "dead"
        
        elif self.state == "attached":
            return -math.cos(math.pi*2-self.hookAngle),math.sin(math.pi*2-self.hookAngle)

        self.rect.update(self.pos[0],self.pos[1],self.size[0],self.size[1])
        

    def set_state(self,state):
        self.state = state
            
    def draw(self,scroll,plrpos):
        newRect = (((self.pos[0]-scroll[0]-self.size[0]//2,self.pos[1]-scroll[1]-self.size[1]//2),(self.size[0],self.size[1]))) 
        self.hookSprite = pygame.transform.scale(self.hookSprite,(self.size))
        self.screen.blit(self.hookSprite, newRect)
        
        pygame.draw.line(self.screen,(93,53,15),
                         (self.pos[0]-scroll[0],self.pos[1]-scroll[1]),
                         (plrpos[0]-scroll[0]+7*self.scale,plrpos[1]-scroll[1]+16*self.scale), self.scale)

        dis = math.sqrt(((plrpos[0]-self.pos[0])**2+(plrpos[1]-self.pos[1])**2))
        amount =  dis //(self.ropeSize[0]+self.ropeSpacing*2)
        
        for dot in range(int(amount)):
            self.ropeSprite = pygame.transform.scale(self.ropeSprite,(self.ropeSize))
            newRopeRect =   (self.pos[0]+(dot*math.cos(self.hookAngle)*self.ropeSize[0]+dot*math.cos(self.hookAngle)*self.ropeSpacing*2)-scroll[0]-self.ropeSize[0]//2,
                                self.pos[1]+(dot*math.sin(self.hookAngle)*self.ropeSize[1]+dot*math.sin(self.hookAngle)*self.ropeSpacing*2)-scroll[1]-self.ropeSize[1]//2),\
                                    (self.ropeSize[0],self.ropeSize[1])

            self.screen.blit(self.ropeSprite,newRopeRect)
    
