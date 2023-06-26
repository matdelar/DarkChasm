import pygame
import math

class Umbrella:
    def __init__(self,screen,database) -> None:
        self.screen = screen
        self.database = database
        self.scale = self.database.get_sprite_scale()
        self.color = self.database.getColor()
        self.size = [16*self.scale,16*self.scale]
        self.sprites = []
        self.sprites.append(self.set_mask_color(pygame.transform.scale(pygame.image.load("assets/items/umbrella/umbrella1.png").convert_alpha(),self.size),self.color,(255,255,255,255)))
        self.sprites.append(self.set_mask_color(pygame.transform.scale(pygame.image.load("assets/items/umbrella/umbrella2.png").convert_alpha(),self.size),self.color,(255,255,255,255)))
        self.sprites.append(self.set_mask_color(pygame.transform.scale(pygame.image.load("assets/items/umbrella/umbrella3.png").convert_alpha(),self.size),self.color,(255,255,255,255)))

        self.spriteShadow = []
        self.spriteShadow.append(pygame.transform.scale(pygame.image.load("assets/items/umbrella/umbrella1Shadow1.png").convert_alpha(),[18*self.scale,18*self.scale]))
        self.spriteShadow.append(pygame.transform.scale(pygame.image.load("assets/items/umbrella/umbrella1Shadow2.png").convert_alpha(),[18*self.scale,18*self.scale]))
        self.spriteShadow.append(pygame.transform.scale(pygame.image.load("assets/items/umbrella/umbrella1Shadow3.png").convert_alpha(),[18*self.scale,18*self.scale]))

        
        self.frameCount = 0
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        
        self.pos = [0,0]
        self.currentOffset = [0,0]
        self.offsetClosed = [8*self.scale,4*self.scale]
        self.offsetOpen = [0,16*self.scale]
        self.angle = 0
        self.angleSpeed = 30
        self.idleFrame = 0

    def run(self,playerPos,scroll,isOpen,isFacingLeft,dt):
        if self.color != self.database.getColor():
            self.updateColor()

        self.idleFrame = (self.idleFrame+(dt*3)) % 360
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
            self.angle += (180 - self.angle) * 0.4 * dt
        else:
            self.angle += (0 - self.angle) * 0.4 * dt

        self.pos = playerPos[0]-scroll[0]-self.currentOffset[0]+isFacingLeft*16*self.scale*(not isOpen)-math.cos(math.radians(self.idleFrame))*self.scale,playerPos[1]-scroll[1]-self.currentOffset[1]-math.sin(math.radians(self.idleFrame))*self.scale

        image = pygame.transform.rotate(self.sprites[self.currentSprite],self.angle)
        imageShadow = pygame.transform.rotate(self.spriteShadow[self.currentSprite],self.angle)


        newRect = self.pos[0]-self.scale,self.pos[1]-self.scale


        self.screen.blit(imageShadow,newRect)
        self.screen.blit(image, self.pos)

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
    
    def updateColor(self):
        self.color = self.database.getColor()
        self.size = [16*self.scale,16*self.scale]
        self.sprites = []
        self.sprites.append(self.set_mask_color(pygame.transform.scale(pygame.image.load("assets/items/umbrella/umbrella1.png").convert_alpha(),self.size),(0,0,0,255),self.color))
        self.sprites.append(self.set_mask_color(pygame.transform.scale(pygame.image.load("assets/items/umbrella/umbrella2.png").convert_alpha(),self.size),(0,0,0,255),self.color))
        self.sprites.append(self.set_mask_color(pygame.transform.scale(pygame.image.load("assets/items/umbrella/umbrella3.png").convert_alpha(),self.size),(0,0,0,255),self.color))


class Coin:
    def __init__(self, screen, pos,database,value=50):
        self.screen = screen
        self.database = database
        self.pos = pos
        self.value = value
        self.scale = self.database.get_sprite_scale()
        self.sprite = pygame.image.load("assets/tiles/Tile_Gold.png").convert()
        self.size = [16,16]
        self.scaled = pygame.transform.scale(self.sprite,(self.size[0]*self.scale,self.size[1]*self.scale))
        self.rect = pos[0],pos[1],self.size[0],self.size[1]


    def get_value(self):
        return self.value

    def get_rect(self):
        return self.rect

    def draw(self,scroll):
        newRect = self.pos[0]-scroll[0],self.pos[1]-scroll[1]
        self.screen.blit(self.scaled,newRect)

class Hook:
    def __init__(self, screen, pos, angle,database) -> None:
        self.screen = screen
        self.database = database
        self.pos = pos
        self.angle = angle
        self.returnSpeed = 16
        self.fowardSpeed = 8
        self.state = "moving"
        self.scale = self.database.get_sprite_scale()
        self.color = self.database.getColor()
        self.size = [8*self.scale,8*self.scale]
        self.ropeSize = [4*self.scale,4*self.scale]
        self.ropeSpacing = 1*self.scale
        self.hookSprite = pygame.image.load("assets/items/hook/hook_graple.png")
        self.ropeSprite = pygame.image.load("assets/items/hook/hook_rope.png")
        self.rect = pygame.rect.Rect((self.pos[0],self.pos[1]),(self.size[0],self.size[0]))
        self.distance = 0
        self.hookAngle = 0

    def update(self,tiles,plrpos,dt):
        self.distance = math.sqrt((plrpos[0]-self.pos[0]+7*self.scale)**2+(plrpos[1]-self.pos[1]+16*self.scale)**2)
        self.hookAngle = math.atan2(plrpos[1]-self.pos[1]+16*self.scale,plrpos[0]-self.pos[0]+7*self.scale)
        if self.state == "moving":
            self.pos = self.pos[0]+self.fowardSpeed*math.cos(self.angle)*self.scale, self.pos[1]+self.fowardSpeed*math.sin(self.angle)*self.scale
            for tile in tiles:
                if self.rect.colliderect(tile.get_rect()):
                    self.state = "attached"

        elif self.state == "retracted":
            self.pos =  self.pos[0]+(self.returnSpeed*math.cos(self.hookAngle)*self.scale)*dt, self.pos[1]+self.returnSpeed*math.sin(self.hookAngle)*self.scale*dt
            if self.distance <= self.returnSpeed*2: # distance should be less than backspd to avoid bugs
                self.state = "dead"
        
        elif self.state == "attached":
            pass

        self.rect.update(self.pos[0],self.pos[1],self.size[0],self.size[1])
        
    def get_angle(self):
        return -math.cos(math.pi*2-self.hookAngle),math.sin(math.pi*2-self.hookAngle)

    def set_state(self,state):
        self.state = state
            
    def draw(self,scroll,plrpos):
        newRect = (((self.pos[0]-scroll[0]-self.size[0]//2,self.pos[1]-scroll[1]-self.size[1]//2),(self.size[0],self.size[1]))) 
        self.hookSprite = pygame.transform.scale(self.hookSprite,(self.size))
        self.screen.blit(self.hookSprite, newRect)
        
        pygame.draw.line(self.screen,self.color,
                         (self.pos[0]-scroll[0],self.pos[1]-scroll[1]),
                         (plrpos[0]-scroll[0]+7*self.scale,plrpos[1]-scroll[1]+16*self.scale), int(self.scale))

        dis = math.sqrt(((plrpos[0]-self.pos[0])**2+(plrpos[1]-self.pos[1])**2))
        amount =  dis //(self.ropeSize[0]+self.ropeSpacing*2)
        
        for dot in range(int(amount)):
            self.ropeSprite = pygame.transform.scale(self.ropeSprite,(self.ropeSize))
            newRopeRect =   (self.pos[0]+(dot*math.cos(self.hookAngle)*self.ropeSize[0]+dot*math.cos(self.hookAngle)*self.ropeSpacing*2)-scroll[0]-self.ropeSize[0]//2,
                                self.pos[1]+(dot*math.sin(self.hookAngle)*self.ropeSize[1]+dot*math.sin(self.hookAngle)*self.ropeSpacing*2)-scroll[1]-self.ropeSize[1]//2),\
                                    (self.ropeSize[0],self.ropeSize[1])

            self.screen.blit(self.ropeSprite,newRopeRect)

class Pickaxe:
    pass

class Tile:
    pass
