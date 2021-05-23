# Maze Generator and Solver

### mazegen.py
This script can be used to generate a maze of any size (in nodes) based on user input. It relies on a modified version of Kruskal's algorithm to randomly add edges to a graph of maze nodes until all nodes are connected. It also supports creating larger images for easier viewing as well as any number of cycles to confuse solvers. I know that it is not nearly as efficient as it could be because Python does not allow direct pointer manipulation for graph-like data structures.

### mazesolve.py
This script is a work in progress and can parse an image file like the ones produced by mazegen.py into a list of significant nodes for processing and solving. I intend on adding different solution algorithms for comparison on both cyclic and acyclic mazes from mazegen.py.

### Dependencies

Both mazegen.py and mazesolve.py rely on PIL (Python Imaging Library) to create and modify .png files. Neither will work without having PIL installed. Anyone who does not have it installed should reference [this](https://pillow.readthedocs.io/en/stable/index.html) site.

Written by Luke Bender (lrbender01@gmail.com) in April 2021.