import pygame
import SceneManager
from Hook import *

class Player:
    def __init__(self,screen,pos) -> None:
        self.scale = SceneManager.Manager.get_sprite_scale()
        self.screen = screen
        self.pos = pos
        self.maxSpeed = 4
        self.actualspeed = 0
        self.speedIncrease = 1/60 * self.maxSpeed * 8
        self.speedDecrease = 1/60 * self.maxSpeed * 4
        self.gravityMaxSpeed = 1/60 * self.scale * (16*13)
        self.gravityAceleration = 1/60 * self.scale * 8
        self.gravityActualSpeed = 0
        self.jumpForce = self.gravityMaxSpeed * 4/3
        self.canJump = False
        self.jumpMomentum = 0
        self.collisionTypes = False
        
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/entities/Player/Idle/Player1.png"))
        self.sprites.append(pygame.image.load("assets/entities/Player/Idle/Player2.png"))
        self.sprites.append(pygame.image.load("assets/entities/Player/Idle/Player3.png"))
        self.sprites.append(pygame.image.load("assets/entities/Player/Idle/Player4.png"))
        self.sprites.append(pygame.image.load("assets/entities/Player/Idle/Player5.png"))
        self.sprites.append(pygame.image.load("assets/entities/Player/Idle/Player6.png"))
        self.sprites.append(pygame.image.load("assets/entities/Player/Idle/mask.png"))

        self.size = 16*self.scale, 16*self.scale
        self.horizontalSpeed = 0
        self.isFacingLeft = False

        self.currentSprite = 6
        self.image = self.sprites[self.currentSprite]
        self.frameCount = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos[0]+24, self.pos[1]
    
        self.hook = None
        self.hookVelocity = [0,0]
        self.actualHookSpeed = 0
        self.hookSpeedIncrease = 1/60 * self.maxSpeed * 8
        self.hookMaxVelocity = 1/60 * self.maxSpeed * (16*12)
        self.hookMomentum = [0,0]

        self.lastpos = [0,0]
        self.hookoffset = 7*self.scale, 14*self.scale

    def collision_test(self,tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile.get_rect()):
                hit_list.append(tile.get_rect())
        return hit_list

    def move(self,movement,tiles):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.rect.x += movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if movement[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True
        self.rect.y += movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
        return self.rect, collision_types

    def update(self,tiles,scroll):
        keys = pygame.key.get_pressed()
        mouseClick = pygame.mouse.get_pressed()[0]

        #hook controller
        if mouseClick and not isinstance(self.hook,Hook):

            playerPosScroll = self.pos[0]-scroll[0]+self.size[0]//2,self.pos[1]-scroll[1]+self.size[1]//2
            centerPos = self.pos[0]+self.size[0]//2,self.pos[1]+self.size[1]//2
            mousepos = pygame.mouse.get_pos()
            hookAngle = math.atan2(mousepos[1]-playerPosScroll[1],mousepos[0]-playerPosScroll[0])
            self.hook = Hook(self.screen,centerPos,hookAngle)
            self.hook.update(tiles,self.pos)
            self.hook.draw(scroll, self.pos)

        elif mouseClick and isinstance(self.hook,Hook) and self.hook.state != "dead":
            self.hookVelocity = self.hook.update(tiles,self.pos)
            self.hook.draw(scroll, self.pos)
        
            self.actualHookSpeed = self.actualHookSpeed + self.hookSpeedIncrease if self.actualHookSpeed + self.hookSpeedIncrease < self.hookMaxVelocity else self.hookMaxVelocity 
        elif not mouseClick and isinstance(self.hook,Hook) and self.hook.state !="dead":
            self.hook.set_state("retracted")
            self.hook.update(tiles,self.pos)
            self.hook.draw(scroll, self.pos)
        
        elif isinstance(self.hook,Hook) and self.hook.state == "attached":
            if self.hookMomentum[0] == self.hookMomentum[1] == 0:
                self.hookMomentum = self.hook.update(tiles,self.pos)
                self.hookMomentum[0],self.hookMomentum[1] = self.hookMomentum[0]*self.actualHookSpeed,self.hookMomentum[1] *self.actualHookSpeed
            else:
                self.hook.update(tiles,self.pos)
            self.gravityActualSpeed = 0

        elif isinstance(self.hook,Hook) and self.hook.state == "dead":
            self.actualHookSpeed = 0
            self.hook = None
        
        #movement management
        self.horizontalSpeed = (keys[pygame.K_d] - keys[pygame.K_a]) 
        if keys[pygame.K_SPACE] and self.canJump:
            self.jumpMomentum = self.jumpForce
        else:
            self.jumpMomentum = self.jumpMomentum-self.gravityAceleration if self.jumpMomentum-self.gravityAceleration > 0 else 0  

        if self.horizontalSpeed < 0:
            self.isFacingLeft = True
        elif self.horizontalSpeed > 0:
            self.isFacingLeft = False

        if self.horizontalSpeed != 0:
            if self.isFacingLeft:
                self.actualspeed = self.actualspeed - self.speedIncrease if self.actualspeed - self.speedIncrease > -self.maxSpeed else -self.maxSpeed
            else:
                self.actualspeed = self.actualspeed + self.speedIncrease if self.actualspeed + self.speedIncrease < self.maxSpeed else self.maxSpeed
        elif self.horizontalSpeed == 0:
            if self.isFacingLeft:
                self.actualspeed = self.actualspeed + self.speedDecrease if self.actualspeed + self.speedDecrease < 0 else 0
            else:
                self.actualspeed = self.actualspeed - self.speedDecrease if self.actualspeed - self.speedDecrease > 0 else 0

        self.gravityActualSpeed = self.gravityActualSpeed + self.gravityAceleration if self.gravityActualSpeed + self.gravityAceleration < self.gravityMaxSpeed else self.maxSpeed
    

        if self.hookVelocity != None and isinstance(self.hook,Hook):
            movement = [self.actualspeed+self.hookVelocity[0]*self.actualHookSpeed,self.gravityActualSpeed+self.hookVelocity[1]*self.actualHookSpeed]
        else:
            movement = [self.actualspeed+self.hookMomentum[0],self.gravityActualSpeed+self.hookMomentum[1]-self.jumpMomentum]

        print(self.hookMomentum)


        self.lastpos[0] += (self.pos[0]-self.lastpos[0])*0.75
        self.lastpos[1] += (self.pos[1]-self.lastpos[1])*0.75


        self.pos, onFloor = self.move(movement,tiles)

        if onFloor['bottom']:
            self.gravityActualSpeed = 0
            self.canJump = True
        else:
            self.canJump = False

        if onFloor['top']:
            self.jumpMomentum = 0

        npos = self.pos[0],self.pos[1]

        self.rect.update((npos,self.size))

    def draw(self,scroll):
        newRect = (self.pos[0]-scroll[0],self.pos[1]-scroll[1]),(self.size)

        self.image = pygame.transform.scale(self.sprites[self.currentSprite],(self.size))
        #self.frameCount +=1
        if self.frameCount == 10:
            self.frameCount = 0
            self.currentSprite +=1 if self.currentSprite < 5 else -5

        self.drawShadow(self.image,scroll)

    
        self.screen.blit(pygame.transform.flip(self.image, self.isFacingLeft, False), newRect)

        #hitbox debug
        #render 
        #pygame.draw.rect(self.screen,(255,255,255), nrect, SceneManager.Manager.get_sprite_scale())
        #atual pos 
        #pygame.draw.rect(self.screen,(255,255,255), self.rect, SceneManager.Manager.get_sprite_scale())
    
    def drawShadow(self,image,scroll):
        shadow = image.copy()
        self.set_color(shadow,(69,17,124,255))


        or1 = (self.lastpos[0]-scroll[0],self.lastpos[1]-scroll[1]-self.scale),(self.size)
        or2 = (self.lastpos[0]-scroll[0],self.lastpos[1]-scroll[1]+self.scale),(self.size)
        or3 = (self.lastpos[0]-scroll[0]-self.scale,self.lastpos[1]-scroll[1]),(self.size)
        or4 = (self.lastpos[0]-scroll[0]+self.scale,self.lastpos[1]-scroll[1]),(self.size)

        offshadowGroup = [or1,or2,or3,or4]

        for nrect in offshadowGroup:
            self.screen.blit(pygame.transform.flip(shadow, self.isFacingLeft, False), nrect)


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