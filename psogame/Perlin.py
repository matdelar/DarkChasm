import math
import random
import time

def generate_noise(width, height, scale):
    grid = [[0.0] * height for _ in range(width)]
    
    for y in range(height):
        for x in range(width):
            nx = float(x) / width - 0.5
            ny = float(y) / height - 0.5
            
            value = perlin_noise_2d(nx * scale, ny * scale)
            grid[x][y] = value
    
    return grid


def perlin_noise_2d(x, y):
    x0, x1 = int(math.floor(x)), int(math.ceil(x))
    y0, y1 = int(math.floor(y)), int(math.ceil(y))
    
    sx = x - x0
    sy = y - y0
    
    n0 = dot_grid_gradient(x0, y0, x, y)
    n1 = dot_grid_gradient(x1, y0, x, y)
    ix0 = lerp(n0, n1, sx)
    
    n0 = dot_grid_gradient(x0, y1, x, y)
    n1 = dot_grid_gradient(x1, y1, x, y)
    ix1 = lerp(n0, n1, sx)
    
    value = lerp(ix0, ix1, sy)
    return value


def dot_grid_gradient(ix, iy, x, y):
    dx = x - float(ix)
    dy = y - float(iy)
    
    gradient = gradients[iy % len(gradients)][ix % len(gradients[0])]
    return dx * gradient[0] + dy * gradient[1]


def lerp(a, b, t):
    return (1.0 - t) * a + t * b


# Generate random gradients
random.seed(time.time_ns())
gradients = [[(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(256)] for _ in range(256)]

