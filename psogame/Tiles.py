import pygame
import SceneManager
class Stone(pygame.sprite.Sprite):
    def __init__(self,screen, pos,database, type = 0, worldPos=None):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.database = database
        self.type = type
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone1.png").convert())
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone2.png").convert())
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone3.png").convert())
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone4.png").convert())
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone5.png").convert())
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone6.png").convert())
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone7.png").convert())
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone8.png").convert())
        self.sprites.append(pygame.image.load("assets/tiles/Tile_Stone9.png").convert())
        self.image = self.sprites[self.type]
        self.scale = self.database.get_sprite_scale()
        self.size = 16*self.scale, 16*self.scale
        self.pos = pos[0]*16*self.scale, pos[1]*16*self.scale
        if worldPos!= None:
            self.pos = worldPos
        self.rect = self.pos,self.size

        self.tilepos = pos[0]+1, pos[1]+1
        self.rectStatic = pygame.rect.Rect(self.rect)
        self.rect = pygame.rect.Rect(self.rect)
        self.image = pygame.transform.scale(self.sprites[self.type],self.size)

    def draw(self,scroll):
        npos = self.pos[0]-scroll[0],self.pos[1]-scroll[1]
        self.screen.blit(self.image,npos)
        #aplica scroll da camera e renderiza a imagem
        
        #hitbox debug
        #pygame.draw.rect(self.screen,(255,255,255), self.rect, 3)

    def get_rect(self):
        return self.rectStatic
    
    def set_type(self,grid):
        sides = [False,False,False,False,False,False,False,False]

        sides[0] = grid[self.tilepos[1]-1][self.tilepos[0]-1]# x-1,y-1 top left
        sides[1] = grid[self.tilepos[1]-1][self.tilepos[0]]   # x,y-1 top
        sides[2] = grid[self.tilepos[1]-1][self.tilepos[0]+1]# x+1,y-1 top Right
        sides[3] = grid[self.tilepos[1]][self.tilepos[0]+1]  # x+1,y Right
        sides[4] = grid[self.tilepos[1]+1][self.tilepos[0]+1]# x+1,y+1 bottom Right
        sides[5] = grid[self.tilepos[1]+1][self.tilepos[0]]  # x,y+1 bottom
        sides[6] = grid[self.tilepos[1]+1][self.tilepos[0]-1]# x-1,y+1 bottom left
        sides[7] = grid[self.tilepos[1]][self.tilepos[0]-1]  # x-1,y left
   
        
        
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