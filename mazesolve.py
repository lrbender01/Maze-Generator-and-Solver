#!/usr/bin/env python3

from PIL import Image
import sys

# TODO: make this more user friendly
# TODO: comment everything
# TODO: optimize
# TODO: take command line arguments
# TODO: combine generator and solver
# TODO: make generator *so* much faster (C++ that bitch)

height = 0
width = 0
colors = []
pixels = []

# Node Class
class Node:
    def __init__(self, x, y):
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.neighbors = [] # list for neighbor coordinate tuples

    def __str__(self):
        neighbors_str = ''
        for neighbor in self.neighbors:
            neighbors_str += f'({neighbor[0]},{neighbor[1]}), '
        return f'({self.x},{self.y}): {neighbors_str[:-2]}'

# Check if a given location is a node
def check_node(x, y):
    north = (colors[y - 1][x] if y > 0 else 0)
    south = (colors[y + 1][x] if y < height - 1 else 0)
    east = (colors[y][x + 1] if x < width - 1 else 0)
    west = (colors[y][x - 1] if x > 0 else 0)

    # Corridors are not nodes
    if north + south + east + west == 2:
        if north + south == 2 or east + west == 2:
            return False
    
    # Not a corridor, must be a node
    return True

# Find neighbor to a node given coordinates and direction
def find_neighbor(x, y, dir):
    if dir == 'N': # North
        while True:
            next = colors[y - 1][x]
            if next == 1 and check_node(x, y - 1):
                return Node(x, y - 1)
            y -= 1
    elif dir == 'S': # South
        while True:
            next = colors[y + 1][x]
            if next == 1 and check_node(x, y + 1):
                return Node(x, y + 1)
            y += 1
    elif dir == 'E': # East
        while True:
            next = colors[y][x + 1]
            if next == 1 and check_node(x + 1, y):
                return Node(x + 1, y)
            x += 1
    elif dir == 'W': # West
        while True:
            next = colors[y][x - 1]
            if next == 1 and check_node(x - 1, y):
                return Node(x - 1, y)
            x -= 1

def main():
    if len(sys.argv) != 2:
        print('Usage: mazegen.py <FILE>')
        exit(-1)
    
    # Read in the file
    image = Image.open(sys.argv[1])
    image = image.convert('RGB')

    global width, height, colors, pixels
    width = image.size[0]
    height = image.size[1]
    pixels = image.load()

    # Calculate maze properties
    node_height = int((height - 1)/2)
    node_width = int((width - 1)/2)
    max_nodes = node_height * node_width + 2

    # Maze property readout
    print(f'Image Dimensions: {width} x {height}')
    print(f'Node Dimensions: {node_width} x {node_height}')
    print(f'{max_nodes} maximum nodes')

    # Convert image into colors bitmap
    for y in range(0, height):
        colors.append([])
        for x in range(0, width):
            pix_val = image.getpixel((x, y))[0]
            if pix_val == 255:
                colors[y].append(1) # Maze corridor
            else:
                colors[y].append(0) # Wall

    # Declare and populate node dictionary
    nodes = {}
    nodes[(1, 0)] = Node(1, 0)
    unexplored = [nodes[(1, 0)]]

    # Iterate until there are no more nodes to explore
    while len(unexplored) != 0:
        current_node = unexplored.pop(0)
        valid_dirs = [True, True] # North, South
        x = current_node.x
        y = current_node.y

        if y == 0: # Start
            valid_dirs[0] = False # North inaccessible
        elif y == height - 1: # End
            valid_dirs[1] = False # South inaccessible

        # Populate directions
        north = (colors[y - 1][x] if valid_dirs[0] else 0)
        south = (colors[y + 1][x] if valid_dirs[1] else 0)
        east = colors[y][x + 1]
        west = colors[y][x - 1]

        # Find neighbors
        neighbors = []
        if north == 1:
            neighbors.append(find_neighbor(x, y, 'N'))
        if south == 1:
            neighbors.append(find_neighbor(x, y, 'S'))
        if east == 1:
            neighbors.append(find_neighbor(x, y, 'E'))
        if west == 1:
            neighbors.append(find_neighbor(x, y, 'W'))

        for neighbor in neighbors:
            # Append neighbor node
            if (neighbor.x, neighbor.y) not in nodes[(x, y)].neighbors:
                nodes[(x, y)].neighbors.append((neighbor.x, neighbor.y))

            # Add to unexplored and nodes if not already seen
            if (neighbor.x, neighbor.y) not in nodes:
                nodes[(neighbor.x, neighbor.y)] = neighbor
                unexplored.append(neighbor)

    # Debugging
    #for node in nodes:
        #print(nodes[node])
    print(f'{len(nodes)} critical nodes ({(1 - (len(nodes) / max_nodes)):.4f}% reduction)')
    # print(f'{(1 - (len(nodes) / max_nodes)):.2f}% reduction')

    # Now we have a dict of nodes/neighbors, start at (1, 0), end at (width - 2, height - 1)

    # TODO: implement different algorithms in functions, each must return a list of nodes to visit to go from the start to the end
    # track time outside of functions, encapsulate algorithms to individual functions for comparison

# TODO: salvage this into an optional mode or something
    '''   
    nodes = []
    for y in range(0, height):
        for x in range(0, width):
            if y == 0: # Start
                if colors[y][x] == 1:
                    nodes.append((x,y))
                    print('start')
                    print(nodes[-1])
            elif y == height - 1: # End
                if colors[y][x] == 1:
                    nodes.append((x, y))
                    print('end')
                    print(nodes[-1])
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
                        else: # Only include corner and deadend nodes
                            nodes.append((x, y))
                    else:
                        nodes.append((x, y))

    for n in nodes:
        colors[n[1]][n[0]] = 2
        pixels[n[0], n[1]] = (255, 0, 0, 255)

    image.save('mazenode.png')
    '''

# Always call main()
if __name__ == '__main__':
    main()