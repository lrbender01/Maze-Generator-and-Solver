#!/usr/bin/env python3

# Libraries
from PIL import Image
import sys, math, time, copy, queue

# TODO: make this more user friendly
# TODO: comment everything
# TODO: optimize
# TODO: take command line argument(s); choose algorithms this way
# TODO: combine generator and solver into one thing; generate and solve mazes simultaneously
# TODO: make generator *so* much faster (C++ that bitch)
# TODO: organize function order to make more sense; everything a function uses should be *above* it
# TODO: organize global variables and figure out global style

# Global Variables
height = 0
width = 0
colors = []
pixels = []

class Node:
    '''
    Node class to help represent mazes.

    Member Variables:
    coords -- coordinate tuple for node
    parent -- coordainte tuple for node parent
    children -- list of coordinate tuples for child nodes
    visited -- boolean tracking if node has been visited
    path_dist -- length of shortest path to reach this node
    est_dist -- estimated remaining distance (admissable heuristic)
    '''
    def __init__(self, x, y):
        self.coords = (x, y)
        self.parent = None
        self.children = []

        self.visited = False

        self.path_dist = math.inf
        self.est_dist = 0

    def __str__(self):
        child_str = ''
        for child in self.children:
            child_str += f'({child[0]},{child[1]}), '
        return f'({self.coords[0]},{self.coords[1]}) ({self.visited}): {child_str[:-2]}'

    def __lt__(self, other):
        # if not self._is_valid_operand(other):
        #    return NotImplemented
        return (self.path_dist + self.est_dist) < (other.path_dist + other.est_dist)

def distance(a = (0, 0), b = (0, 0)):
    '''
    Euclidian distance between two points.

    Parameters:
    a -- tuple for first point (default (0, 0))
    b -- tuple for second point (default (0, 0))
    '''
    return math.sqrt(pow(abs(b[0] - a[0]), 2) + pow(abs(b[1] - a[1]), 2))

def check_node(x, y):
    '''
    Check whether a given point is considered a node.

    Parameters:
    x -- x coordinate
    y -- y coordinate
    '''
    # Mark global variables
    global height, width

    # Check open directions
    north = (colors[y - 1][x] if y > 0 else 0)
    south = (colors[y + 1][x] if y < height - 1 else 0)
    east = (colors[y][x + 1] if x < width - 1 else 0)
    west = (colors[y][x - 1] if x > 0 else 0)

    nsew = north + south + east + west 
    ns = north + south
    ew = east + west

    # Remove "corridor" nodes
    if nsew == 2 and (ns == 2 or ew == 2):
        return False
    
    # All others valid
    return True

def find_neighbor(x, y, dir):
    '''
    Find neighbor to node given its coordinates and cardinal direction.

    Parameters:
    x -- x coordinate of node
    y -- y coordinate of node
    dir -- cardinal direction to search ('N', 'S', 'E', or 'W')
    '''
    # Mark global variables
    global colors

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

def points_between(a = (0, 0), b = (0, 0)):
    '''
    Get list of all points between a and b. X or Y values must match.

    Parameters:
    a -- tuple for first point (default (0, 0))
    b -- tuple for second point (default (0, 0))
    '''
    points = []
    if a[0] == b[0]: # X value the same
        larger = (a[1] if a[1] > b[1] else b[1])
        smaller = (b[1] if larger == a[1] else a[1])

        for i in range(smaller + 1, larger):
            points.append((a[0], i))
    elif a[1] == b[1]: # Y value the same
        larger = (a[0] if a[0] > b[0] else b[0])
        smaller = (b[0] if larger == a[0] else a[0])

        for i in range(smaller + 1, larger):
            points.append((i, a[1]))
    else:
        return []

    return points

def convert_nodes(colors):
    '''
    TODO: do this
    '''
    # Declare and populate node dictionary
    nodes = {}
    nodes[(1, 0)] = Node(1, 0)
    unexplored = [nodes[(1, 0)]]

    # Iterate until there are no more nodes to explore
    while len(unexplored) != 0:
        current_node = unexplored.pop(0)
        valid_dirs = [True, True] # North, South
        x = current_node.coords[0]
        y = current_node.coords[1]

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
            n_x = neighbor.coords[0]
            n_y = neighbor.coords[1]

            if (n_x, n_y) not in nodes[(x, y)].children:
                nodes[(x, y)].children.append((n_x, n_y))

            # Add to unexplored and nodes if not already seen
            if (n_x, n_y) not in nodes:
                nodes[(n_x, n_y)] = neighbor
                unexplored.append(neighbor)

    return nodes

def dijkstra(nodes):
    '''
    TODO: write this
    '''

    # TODO: implement with a priority queue like a*
    # https://docs.python.org/3/library/queue.html

    # Initial Setup
    global height, width
    nodes[(1, 0)].path_dist = 0
    current_node = nodes[(1, 0)]

    # Algorithm Loop
    while current_node != nodes[(width - 2, height - 1)]:
        # Check neighbors
        for c in current_node.children:
            neighbor = nodes[(c[0], c[1])]

            # Check if path to neighbor can be shortened
            calc_dist = current_node.path_dist + distance(current_node.coords, neighbor.coords)
            if calc_dist < neighbor.path_dist:
                neighbor.path_dist = calc_dist
                neighbor.parent = current_node.coords

        # Mark node as visited
        nodes[current_node.coords].visited = True

        # Find node with shortest path
        min_dist = math.inf
        for n in nodes.values():
            if not n.visited and n.path_dist < min_dist:
                next_node = n.coords
                min_dist = n.path_dist

        # Update current node
        current_node = nodes[next_node]

    current_node = nodes[(width - 2, height - 1)]
    path = [current_node.coords]
    while True:
        if not current_node.parent:
            path.append(current_node.coords)
            break
        else:
            path.append(current_node.parent)
        current_node = nodes[current_node.parent]

    return path

def a_star(nodes):
    global width, height
    
    # Update estimated distance for all nodes
    for k in nodes.keys():
        nodes[k].est_dist = distance(nodes[k].coords, (width - 2, height - 1))
    
    nodes[(1, 0)].path_dist = 0
    fringe = queue.PriorityQueue()
    fringe.put(nodes[(1, 0)])
    curr_node = fringe.get()
    # print(curr_node)
    # print(type(curr_node))

    while curr_node != nodes[(width - 2, height - 1)]:
        for c in curr_node.children:
            child = nodes[(c[0], c[1])]

            calc_dist = curr_node.path_dist + distance(curr_node.coords, child.coords)
            if calc_dist < child.path_dist:
                child.path_dist = calc_dist
                child.parent = curr_node.coords

            if not child.visited:
                fringe.put(nodes[(c[0], c[1])])

        curr_node.visited = True
        curr_node = fringe.get()

    current_node = nodes[(width - 2, height - 1)]
    path = [current_node.coords]
    while True:
        if not current_node.parent:
            path.append(current_node.coords)
            break
        else:
            path.append(current_node.parent)
        current_node = nodes[current_node.parent]

    return path

def main():
    if len(sys.argv) != 2:
        print('usage: mazegen.py maze_file')
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

    # Convert color bitmap into reduced node dictionary
    nodes = convert_nodes(colors)

    print(f'{len(nodes)} critical nodes ({((1 - (len(nodes) / max_nodes)) * 100):.2f}% reduction)')

    # Run and time algorithms
    # dijkstra_nodes = copy.deepcopy(nodes)
    start_dijk = time.perf_counter_ns()
    # dijkstra_path = dijkstra(dijkstra_nodes)
    end_dijk = time.perf_counter_ns()

    print(f'Dijkstra: {((end_dijk - start_dijk) / 1000000000):.2f}s')

    a_star_nodes = copy.deepcopy(nodes) # adds major overhead - I wonder if we could just go undo the damage?
    start_ast = time.perf_counter_ns()
    a_star_path = a_star(a_star_nodes)
    end_ast = time.perf_counter_ns()

    print(f'A*: {((end_ast - start_ast) / 1000000000):.2f}s')

    # TODO: put other algorithms in here

    path = a_star_path

    prev_node = None
    for curr_node in path:
        pixels[curr_node[0], curr_node[1]] = (255, 0, 0, 255)
        if prev_node:
            for p in points_between(prev_node, curr_node):
                pixels[p[0], p[1]] = (255, 0, 0, 255)
        prev_node = curr_node

    # Save solved maze image
    image.save(f'{(sys.argv[1])[:-4]}_solved.png')

# Entrypoint
if __name__ == '__main__':
    main()