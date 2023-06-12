from perlin_noise import PerlinNoise
from random import randint
import math

def Generate_map(size):
    noise1 = PerlinNoise(octaves=5)
    maxPlayerAmount = 1
    maxCoinAmount = 20
    xpix, ypix = size
    pic = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val = 8*noise1([i/xpix, j/ypix])

            row.append(int(math.fabs(noise_val)))
        pic.append(row)
    return pic
