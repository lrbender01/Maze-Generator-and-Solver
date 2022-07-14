#!/usr/bin/env python3

from PIL import Image
import random, time, os

DEBUG_FLAG = False

# Kruskal's Algorithm: http://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm
    # https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
    # https://mtimmerm.github.io/webStuff/maze.html
    # https://stackoverflow.com/questions/38502/whats-a-good-algorithm-to-generate-a-maze
    # https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap

# Set bar to be half of terminal size
bar_length = round(os.get_terminal_size()[0]/2)

# Draw progress for maze generation
def draw_progress(percent):
    curr_length = int(round(bar_length * percent))
    bar = '\r[{0}] {1}%'.format('#' * curr_length + '-' * (bar_length - curr_length), round(percent * 100, 2))
    print(bar, end = '', flush = True)  

# Generate actual maze
def generate_maze(width, height, cycles):
    # Lists
    nodes = []
    sub_graphs = []
    edges = []

    # Populate nodes
    for y in range(height):
        for x in range(width):
            node_num = x + (y * width)
            nodes.append(node_num)
            sub_graphs.append({node_num})
    
    # Populate edges
    for n in nodes:
        if n % width == 0: # left
            edges.append([n, n + 1])
        elif n % width == width - 1: # right
            edges.append([n - 1, n])
        else: # middle
            edges.append([n, n + 1])
            edges.append([n - 1, n])
        
        if n / width < 1: # top
            edges.append([n, n + width])
        elif n / width >= height - 1: # bottom
            edges.append([n - width, n])
        else: # middle
            edges.append([n, n + width])
            edges.append([n - width, n])

    # Remove duplicates
    edges = list(set(map(tuple, edges)))

    # Debugging Output
    if DEBUG_FLAG:
        print(f'{len(nodes)} Nodes')
        print(f'{len(edges)} Edges')

    # Continuously remove edges
    num_cycles = 0
    while True:
        e = random.choice(edges)

        # Find element sets are
        for g in sub_graphs:
            if e[0] in g:
                set_a = g
            if e[1] in g:
                set_b = g

        # Only coalesce if sets are different
        if set_a != set_b:
            sub_graphs.append(set_a.union(set_b))
            sub_graphs.remove(set_a)
            sub_graphs.remove(set_b)
            edges.remove(e)
        else:
            continue

        # Debugging Output
        if DEBUG_FLAG:
            print(f'Sub Graphs: {sub_graphs}, Edge Removed: {e}, Graphs Left: {len(sub_graphs)}')

        draw_progress(1 - (len(sub_graphs) / (width * height)))        

        # Break when all nodes are accessible
        if len(sub_graphs) == 1:
            print('')
            break
    
    while num_cycles != cycles:
        edges.remove(random.choice(edges))
        num_cycles = num_cycles + 1

    if DEBUG_FLAG:
        print(f'Remaining Edges: {edges}')

    return edges

def generate_image(width, height, edges, scale, file):
    img_width = 2 * width + 1
    img_height = 2 * height + 1
    image = Image.new('RGBA', (img_width, img_height), color = 'white')
    pixels = image.load()

    # Draw walls and nodes
    for y in range(img_height):
        for x in range(img_width):
            if (x == 1 and y == 0) or (x == img_width - 2 and y == img_height - 1): # Entrance/Exit
                pixels[x, y] = (255, 255, 255, 255)
            elif x == 0 or y == 0 or x == img_width - 1 or y == img_height - 1: # Wall
                pixels[x, y] = (0, 0, 0, 255)
            elif x % 2 == 1 and y % 2 == 1: # Node
                pixels[x, y] = (255, 255, 255, 255)
            elif x % 2 == 0 and y % 2 == 0: # Between edges
                pixels[x, y] = (0, 0, 0, 255)

    # Draw remaining edges
    for e in edges:
        node_0 = e[0]
        delta = e[1] - node_0
        x = 2 * (node_0 % width) + 1
        y = 2 * (node_0 // width) + 1

        if delta == 1:
            pixels[x + 1, y] = (0, 0, 0, 255)
        else:
            pixels[x, y + 1] = (0, 0, 0, 255)

    # Save the image
    image.save(f'{file}')

    if scale != 1:
        big_image = Image.new('RGBA', (img_width * scale, img_height * scale), color = 'white')
        big_pixels = big_image.load()
        for y in range(big_image.height):
            for x in range(big_image.width):
                big_pixels[x, y] = pixels[int(x / scale), int(y / scale)]
        big_image.save(f'{file[:-4]}_{scale}x.png')
        
def main():
    width = int(input('Width: '))
    height = int(input('Height: '))

    file = str(input('Save as: '))

    scale = 1
    if str(input('Enlarge image (y/n): ')) == 'y':
        scale = int(input('\tScale: '))

    cycles = 0
    if str(input('Allow cycles (y/n): ')) == 'y':
        cycles = int(input('\tCycles: '))

    start_time = time.time()
    maze = generate_maze(width, height, cycles)
    generate_image(width, height, maze, scale, file)
    print(f'Finished maze and image in {str(round(time.time() - start_time, 3))} seconds')

# Always call main()
if __name__ == '__main__':
    main()