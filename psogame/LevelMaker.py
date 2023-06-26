from random import randint
import math
import Perlin

def Generate_map(size,coinCount=250):
    xpix, ypix = size
    currentCoin = 250
    noise_grid = Perlin.generate_noise(xpix, ypix, 5)

    pic = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val = noise_grid[i][j]
            nval = int(math.fabs(noise_val*10))
            row.append(0<nval<3)

        pic.append(row)
    
    for i in range(coinCount):
        ax = randint(0,xpix-1)
        ay = randint(0,ypix-1)
        pic[ax][ay] = 3
    
    return pic
