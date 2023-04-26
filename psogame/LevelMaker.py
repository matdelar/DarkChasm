from PIL import Image

# Open the image and convert it to black and white
image = Image.open('PNGS\level1.png').convert('L')

# Get the height and width of the image
width, height = image.size

# Create an empty matrix with the same dimensions as the image
matrix = [[0 for y in range(height)] for x in range(width)]

# Loop through each pixel in the image and add its value to the matrix
for x in range(width):
    for y in range(height):
        matrix[x][y] = image.getpixel((x, y))

# Transpose the matrix to fix its orientation
matrix = list(map(list, zip(*matrix)))

# Invert the 1s and 0s in the matrix
for row in matrix:
    for i in range(len(row)):
        row[i] = 1 - row[i] if 1 - row[i] == 1 else 0

# Save the inverted matrix as a text file
with open('inverted_matrix.txt', 'w') as file:
    for row in matrix:
        file.write(' '.join(str(pixel) for pixel in row) + '\n')
