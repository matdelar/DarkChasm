import pygame
import SceneManager

class AncientMage():
    def __init__(self,screen,pos):
        self.screen = screen
        self.pos = pos
        self.sprites = []
        for i in range(1, 11):
            filename = f"assets/entities/AncientMage/AncientRobes{i}.png"
            self.sprites.append(pygame.image.load(filename))
            
        self.scale = SceneManager.Manager.get_sprite_scale()
        self.size = 22*self.scale, 38 * self.scale

        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        self.framecount = 0

        self.rect = self.pos,self.size
    
    def draw(self, scroll = [0,0]):
        self.image = pygame.transform.scale(self.sprites[self.currentSprite],self.size)
        self.framecount +=1
        if self.framecount == 6:
            self.framecount = 0
            self.currentSprite +=1 if self.currentSprite < 9 else -9

        self.screen.blit(self.image,self.rect)

        #hitbox debug
        #pygame.draw.rect(self.screen,(255,255,255), self.rect, 3)

class TownMage:
    def __init__(self,screen,pos) -> None:
        self.screen = screen
        self.pos = pos
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/entities/TownMage/TownMage.png"))
        self.scale = SceneManager.Manager.get_sprite_scale()
        self.size = 20*self.scale, 32 * self.scale
        
        self.rect = self.pos,self.size
    
    def draw(self, scroll = [0,0]):
        self.image = pygame.transform.scale(self.sprites,self.size)

        self.screen.blit(self.image,self.rect)

