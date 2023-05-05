import pygame
import SceneManager
import math

class Umbrella:
    def __init__(self,screen) -> None:
        self.screen = screen
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/entities/Player/Items/Umbrella1.png"))
        self.sprites.append(pygame.image.load("assets/entities/Player/Items/Umbrella2.png"))
        self.sprites.append(pygame.image.load("assets/entities/Player/Items/Umbrella3.png"))
        self.frameCount = 0
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        self.scale = SceneManager.Manager.get_sprite_scale()
        
        self.pos = [0,0]
        self.size = [16*self.scale,16*self.scale]
        self.currentOffset = [0,0]
        self.offsetClosed = [8*self.scale,4*self.scale]
        self.offsetOpen = [0,16*self.scale]
        self.angle = 0
        self.angleSpeed = 30
        self.idleFrame = 0

    def run(self,playerPos,scroll,isOpen,isFacingLeft):
        self.idleFrame += 3

        if isOpen:
            self.currentOffset[0] += self.offsetOpen[0]-self.currentOffset[0] * 0.75
            self.currentOffset[1] += self.offsetOpen[1]-self.currentOffset[1] * 0.75
        else:
            self.currentOffset[0] += self.offsetClosed[0]-self.currentOffset[0] * 0.75
            self.currentOffset[1] += self.offsetClosed[1]-self.currentOffset[1] * 0.75
        

        if isOpen and self.currentSprite < 2:
            self.frameCount += 1
            if self.frameCount == 6:
                self.currentSprite += 1 if self.currentSprite < 2 else True
                self.frameCount = 0
        elif not isOpen and self.currentSprite > 0:
            self.frameCount += 1
            if self.frameCount == 6:
                self.currentSprite -= 1 if self.currentSprite > 0  else True
                self.frameCount = 0

        if isOpen:
            self.angle += (180 - self.angle) * 0.4
        else:
            self.angle += (0 - self.angle) * 0.4

        self.pos = playerPos[0]-scroll[0]-self.currentOffset[0]+isFacingLeft*16*self.scale*(not isOpen)-math.cos(math.radians(self.idleFrame))*self.scale,playerPos[1]-scroll[1]-self.currentOffset[1]-math.sin(math.radians(self.idleFrame))*self.scale

        self.image = pygame.transform.rotate(self.sprites[self.currentSprite],self.angle)
        self.image = pygame.transform.scale(self.image,(self.size))

        newRect = pygame.Rect((self.pos[0],self.pos[1]),(self.size[0],self.size[1]))

        self.drawShadow(self.image)
        self.screen.blit(self.image, newRect)

    def draw(self):
        pass

    def drawShadow(self,image):
        shadow = image.copy()
        self.set_color(shadow,(69,17,124,255))


        or1 = (self.pos[0],self.pos[1]-self.scale),(self.size)
        or2 = (self.pos[0],self.pos[1]+self.scale),(self.size)
        or3 = (self.pos[0]-self.scale,self.pos[1]),(self.size)
        or4 = (self.pos[0]+self.scale,self.pos[1]),(self.size)

        offshadowGroup = [or1,or2,or3,or4]

        for nrect in offshadowGroup:
            self.screen.blit(shadow, nrect)


    def set_color(self,surface, color):
        w, h = surface.get_size()
        r, g, b, a = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))
    
    def set_mask_color(self,surface, primaryColor,secondaryColor):
        nsurface = surface.copy()
        w, h = nsurface.get_size()
        r, g, b, a = primaryColor
        r2, g2, b2, a = secondaryColor
        for x in range(w):
            for y in range(h):
                a = nsurface.get_at((x, y))[3]
                if nsurface.get_at((x,y))[0] == 0 and nsurface.get_at((x,y))[1] == 0 and nsurface.get_at((x,y))[2] == 0:
                    nsurface.set_at((x, y), pygame.Color(r, g, b, a))
                elif nsurface.get_at((x,y))[0] == 255 and nsurface.get_at((x,y))[1] == 255 and nsurface.get_at((x,y))[2] == 255:
                    nsurface.set_at((x, y), pygame.Color(r2, g2, b2, a))
        return nsurface
    def get_sprite(self):
        return pygame.transform.scale(self.sprites[self.currentSprite],(self.size))
