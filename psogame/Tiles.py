import pygame
import SceneManager
class Stone:
    def __init__(self,screen, pos, type = 0) -> None:
        self.screen = screen
        self.type = type
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone1.png"))
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone2.png"))
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone3.png"))
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone4.png"))
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone5.png"))
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone6.png"))
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone7.png"))
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone8.png"))
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone9.png"))
        self.image = self.sprites[self.type]
        self.scale = SceneManager.Manager.get_sprite_scale()
        self.size = 16*self.scale, 16*self.scale
        self.pos = pos[0]*16*self.scale, pos[1]*16*self.scale
        self.tilepos = pos[0]+1, pos[1]+1
        self.rect = self.pos,self.size
        self.rect = pygame.rect.Rect(self.rect)
        self.image = pygame.transform.scale(self.sprites[self.type],self.size)
    
    def draw(self,scroll):
        #aplica scroll da camera e renderiza a imagem
        npos = self.pos[0]-scroll[0],self.pos[1]-scroll[1]

        self.screen.blit(self.image, npos)
        
        #hitbox debug
        #pygame.draw.rect(self.screen,(255,255,255), self.rect, 3)

    def get_rect(self):
        return self.rect
    
    def set_type(self,grid):
        sides = [False,False,False,False,False,False,False,False]

        if grid[self.tilepos[1]-1][self.tilepos[0]-1] == 1: # x-1,y-1 top left
            sides[0] = True
        else:
            sides[0] = False

        if grid[self.tilepos[1]-1][self.tilepos[0]] == 1: # x,y-1 top
            sides[1] = True
        else:
            sides[1] = False

        if grid[self.tilepos[1]-1][self.tilepos[0]+1] == 1: # x+1,y-1 top Right
            sides[2] = True
        else:
            sides[2] = False

        if grid[self.tilepos[1]][self.tilepos[0]+1] == 1: # x+1,y Right
            sides[3] = True
        else:
            sides[3] = False

        if grid[self.tilepos[1]+1][self.tilepos[0]+1] == 1: # x+1,y+1 bottom Right
            sides[4] = True
        else:
            sides[4] = False

        if grid[self.tilepos[1]+1][self.tilepos[0]] == 1: # x,y+1 bottom
            sides[5] = True
        else:
            sides[5] = False

        if grid[self.tilepos[1]+1][self.tilepos[0]-1] == 1: # x-1,y+1 bottom left
            sides[6] = True
        else:
            sides[6] = False

        if grid[self.tilepos[1]][self.tilepos[0]-1] == 1: # x-1,y left
            sides[7] = True
        else:
            sides[7] = False
        
        
        if not sides[1] and sides[3] and sides[4] and sides[5] and not sides[7]:
            self.type = 0
        if not sides[1] and sides[3] and sides[4] and sides[5] and sides[6] and sides[7]:
            self.type = 1
        if not sides[1] and not sides[3] and sides[5] and sides[6] and sides[7]:
            self.type = 2

        if sides[1] and sides[2] and sides[3] and sides[4] and sides[5] and not sides[7]:
            self.type = 3
        if sides[0] and sides[1] and not sides[3] and sides[6] and sides[7]:
            self.type = 5


        if sides[1] and sides[3] and not sides[5] and not sides[7]:
            self.type = 6
        if sides[0] and sides[1] and sides[2] and sides[3] and not sides[5] and sides[7]:
            self.type = 7 
        if sides[1] and not sides[3] and not sides[5] and sides[7]:
            self.type = 8
        
            
        self.image = pygame.transform.scale(self.sprites[self.type],self.size)