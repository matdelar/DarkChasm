import pygame
import SceneManager
from Entities import *
from Input import Input 
from Particle import ParticleEmitter

class Player:
    def __init__(self,screen,pos,database) -> None:
        self.screen = screen
        self.database = database
        self.scale = self.database.get_sprite_scale()
        self.input = Input()
        self.pos = pos
        self.maxSpeed = 5
        self.actualspeed = 0
        self.speedIncrease = 1/60 * self.maxSpeed * 10
        self.speedDecrease = 1/60 * self.maxSpeed * 6
        self.gravityMaxSpeed = 1/60 * self.scale * 100
        self.gravityAceleration = 1/60 * self.scale * 10
        self.gravityActualSpeed = 0
        self.jumpForce = self.gravityMaxSpeed*3
        self.jumpMomentum = 0
        self.coyoteTime = 6
        self.coyoteCounter = 0
        self.collisionTypes = False
        self.color = self.database.getColor()
        self.canMove = True
        
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/player/mask.png"))

        self.size = 16*self.scale, 16*self.scale
        self.horizontalSpeed = 0
        self.isFacingLeft = False

        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        self.frameCount = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos[0]+24, self.pos[1]

        self.lastpos = [0,0]
        self.umbrella = Umbrella(self.screen,self.database)
        self.hook = None
        self.particle = ParticleEmitter(self.screen,(15,15),(200,0,0),self.pos,300,10,10,1,0)

    def collision_test(self,tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile.get_rect()):
                hit_list.append(tile.get_rect())
        return hit_list

    def setCanMove(self,pause=None):
        if pause != None:
            self.canMove = pause
        else:
            self.canMove = not self.canMove

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
        self.color = self.database.getColor()
        self.coyoteCounter -= 1
        
        #movement management
        self.horizontalSpeed = (self.input.get_input('right') - self.input.get_input('left')) 
        if self.input.get_input('jump') and self.coyoteCounter > 0:
            self.jumpMomentum = self.jumpForce
        elif not self.input.get_input('jump') and self.jumpMomentum > 0:
            self.jumpMomentum = self.jumpMomentum/2
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

        self.gravityActualSpeed = self.gravityActualSpeed + self.gravityAceleration if self.gravityActualSpeed + self.gravityAceleration < self.gravityMaxSpeed else self.gravityMaxSpeed
        movement = [self.actualspeed,self.gravityActualSpeed-self.jumpMomentum]

        if self.input.get_input('action') and self.hook == None:
            playerPosScroll = self.pos[0]-scroll[0]+self.size[0]//2,self.pos[1]-scroll[1]+self.size[1]//2
            mouseAngle = math.atan2(pygame.mouse.get_pos()[1]-playerPosScroll[1],pygame.mouse.get_pos()[0]-playerPosScroll[0])
            self.hook = Hook(self.screen,self.pos,mouseAngle,self.database)
        elif not self.input.get_input('action') and self.hook != None:
            self.hook.state = "retracted"

        if self.hook != None:
            print(self.hook.state,self.hook.distance)
            if self.hook.state == "retracted" and self.hook.distance <= self.hook.returnSpeed*2:
                self.hook = None

        hookAngle = 0
        if self.hook != None:
            self.hook.update(tiles,self.pos)
            self.hook.draw(scroll,self.pos)

            if self.hook.state == "attached":
                hookAngle = self.hook.get_angle()
                movement = [movement[0]+hookAngle[0]*10,movement[1]+hookAngle[1]*10]
        
        
        movement = [movement[0]*self.canMove,movement[1]*self.canMove]
        if movement[1] > 0 and self.input.get_input('jump'):
            movement[1] = movement[1]/4


        #umbrella controller


        self.lastpos[0] += (self.pos[0]-self.lastpos[0])*0.75
        self.lastpos[1] += (self.pos[1]-self.lastpos[1])*0.75


        self.pos, onFloor = self.move(movement,tiles)
        self.umbrella.run(self.pos,scroll,(self.input.get_input('jump') and movement[1] > 0 ),self.isFacingLeft,self.color)

        if onFloor['bottom']:
            self.gravityActualSpeed = 0
            self.coyoteCounter = self.coyoteTime

        if onFloor['top']:
            self.jumpMomentum = 0
        
        if onFloor['left'] or onFloor['right']:
            self.actualspeed = 0

        npos = self.pos[0],self.pos[1]

        self.rect.update((npos,self.size))

    def draw(self,scroll):
        newRect = (self.pos[0]-scroll[0],self.pos[1]-scroll[1]),(self.size)

        self.image = pygame.transform.scale(self.sprites[self.currentSprite],(self.size))
        #self.frameCount +=1
        if self.frameCount == 10:
            self.frameCount = 0
            self.currentSprite +=1 if self.currentSprite < 5 else -5

        self.particle.draw()
        self.drawShadow(self.image,scroll)

    
        colorImage = self.set_mask_color(self.get_sprite(),(self.color[0],self.color[1],self.color[2],255),(255,255,255,255))
        self.screen.blit(pygame.transform.flip(colorImage, self.isFacingLeft, False), newRect)

        #hitbox debug
        ##render 
        #pygame.draw.rect(self.screen,(255,255,255), newRect, SceneManager.Manager.get_sprite_scale())
        #atual pos 
        #pygame.draw.rect(self.screen,(255,255,255), self.rect, SceneManager.Manager.get_sprite_scale())
    
    def drawShadow(self,image,scroll):
        shadow = image.copy()
        self.set_color(shadow,(69,17,124,255))


        or1 = (self.lastpos[0]-scroll[0],self.lastpos[1]-scroll[1]-self.scale),(self.size)
        or2 = (self.lastpos[0]-scroll[0],self.lastpos[1]-scroll[1]-self.scale),(self.size)
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

    def get_rect(self):
        return self.rect
