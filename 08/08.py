#!/usr/bin/env python3

import sys

import numpy as np

with open(sys.argv[1]) as f:
    grid = np.array([[int(c) for c in l.strip()] for l in f])

    visible = 0
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            tree = grid[y,x]

            v = True
            for x0 in range(x):
                if grid[y,x0] >= tree:
                    v = False
                    break
            if v:
                visible += 1
                continue

            v = True
            for x0 in range(x+1, grid.shape[1]):
                if grid[y,x0] >= tree:
                    v = False
                    break
            if v:
                visible += 1
                continue

            v = True
            for y0 in range(y):
                if grid[y0,x] >= tree:
                    v = False
                    break
            if v:
                visible += 1
                continue

            v = True
            for y0 in range(y+1, grid.shape[0]):
                if grid[y0,x] >= tree:
                    v = False
                    break
            if v:
                visible += 1
                continue
           
    print(visible)
