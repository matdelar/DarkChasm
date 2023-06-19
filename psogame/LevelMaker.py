from random import randint
import math
import Perlin

def Generate_map(size):
    xpix, ypix = size

    noise_grid = Perlin.generate_noise(xpix, ypix, 5)

    pic = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val = noise_grid[i][j]

            row.append(int(math.fabs(noise_val*10)))
        pic.append(row)
    return pic
