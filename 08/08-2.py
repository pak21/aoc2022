#!/usr/bin/env python3

import sys

import numpy as np

with open(sys.argv[1]) as f:
    grid = np.array([[int(c) for c in l.strip()] for l in f])

    max_score = -1
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            tree = grid[y,x]

            a = 0
            for x0 in reversed(range(x)):
                a += 1
                if grid[y, x0] >= tree:
                    break

            b = 0
            for x0 in range(x+1, grid.shape[1]):
                b += 1
                if grid[y, x0] >= tree:
                    break

            c = 0
            for y0 in reversed(range(y)):
                c += 1
                if grid[y0, x] >= tree:
                    break

            d = 0
            for y0 in range(y+1, grid.shape[0]):
                d += 1
                if grid[y0, x] >= tree:
                    break

            score = a * b * c * d
            if score > max_score:
               max_score = score 

    print(max_score)
