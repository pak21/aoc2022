#!/usr/bin/env python3

import collections
import sys

import numpy as np

def draw(grid):
    xs = [x for x, _ in grid]
    ys = [y for _, y in grid]
    minx = min(xs)
    maxx = max(xs)
    miny = 0
    maxy = max(ys)

    for y in range(miny, maxy+1):
        l = ''
        for x in range(minx, maxx+1):
            l += grid.get((x, y), '.')
        print(l)

with open(sys.argv[1]) as f:
    rock = []
    for l in [x.rstrip() for x in f]:
        coords = [[int(b) for b in a.split(',')] for a in l.split(' -> ')]
        rock.append(coords)

    grid = {}
    for a in rock:
        for (x0, y0), (x1, y1) in zip(a, a[1:]):
            if x0 == x1:
                for y in range(min(y0, y1), max(y0, y1)+1):
                    grid[(x0, y)] = '#'
            elif y0 == y1:
                for x in range(min(x0, x1), max(x0, x1)+1):
                    grid[(x, y0)] = '#'

    maxy = max([y for _, y in grid])

    sand = 0
    while True:
        x, y = 500, 0
        while True:
            if (x, y+1) in grid:
                if (x-1, y+1) in grid:
                    if (x+1, y+1) in grid:
                        grid[(x, y)] = 'o'
                        print(f'Sand {sand} comes to rest at ({x}, {y})')
                        sand = sand + 1
                        break
                    else:
                        x = x + 1
                        y = y + 1
                else:
                    x = x - 1
                    y = y + 1
            else:
                y = y + 1
            if y > maxy:
                print(f'Sand {sand} escapes')
                foo = bar
