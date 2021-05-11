#!/usr/bin/env python3

import os, sys
from PIL import Image

def main():
    image = Image.open(str(input('File: ')))
    image = image.convert('RGB')
    width = image.size[0]
    height = image.size[1]
    pixels = image.load()

    colors = []
    for y in range(0, height):
        colors.append([])
        for x in range(0, width):
            pix_val = image.getpixel((x, y))[0]
            if pix_val == 255:
                colors[y].append(1)
            else:
                colors[y].append(0)

    nodes = []
    for y in range(0, height):
        for x in range(0, width):
            if y == 0:
                if colors[y][x] == 1:
                    nodes.append((x,y))
            elif y == height - 1:
                if colors[y][x] == 1:
                    nodes.append((x, y))
            else:
                if colors[y][x] == 1:
                    north = colors[y - 1][x]
                    south = colors[y + 1][x]
                    east = colors[y][x + 1]
                    west = colors[y][x - 1]
                    if north + south + east + west == 2:
                        if north + south == 2:
                            continue
                        elif east + west == 2:
                            continue
                        else:
                            nodes.append((x, y))
                    else:
                        nodes.append((x, y))

    for n in nodes:
        colors[n[1]][n[0]] = 2
        pixels[n[0], n[1]] = (255, 0, 0, 255)

    image.save('mazenode.png')

# Always call main()
if __name__ == '__main__':
    main()