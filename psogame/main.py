import pygame
from SceneManager import *
import asyncio
import time

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Dark Chasm")
pygame.display.set_icon(pygame.image.load("assets/ui/menu/icon.png"))


clock = pygame.time.Clock()

scene = Manager(screen,clock)


async def main():
    last_time = time.time()

    while True:
        dt = time.time()-last_time
        dt *= 60
        last_time = time.time()

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        screen.fill((30,30,40))
        
        scene.run(event,dt)

        clock.tick(60)
        #print(int(clock.get_fps()))
        #print(int(clock.get_fps()),dt)
        pygame.display.update()
        await asyncio.sleep(0) 

    pygame.quit()

asyncio.run(main())