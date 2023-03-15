import pygame
from SceneManager import *
import asyncio

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Dark Chasm")

scene = Manager(screen)

clock = pygame.time.Clock()

async def main():

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        screen.fill((30,30,40))
        
        scene.run()

        clock.tick(60)
        #print(int(clk.get_fps()))
        pygame.display.update()
        await asyncio.sleep(0) 

    pygame.quit()

asyncio.run(main())