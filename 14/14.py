#!/usr/bin/env python3

import sys

grid = set()
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        coords = [[int(b) for b in a.split(',')] for a in l.split(' -> ')]
        for (x0, y0), (x1, y1) in zip(coords, coords[1:]):
            if x0 == x1:
                for y in range(min(y0, y1), max(y0, y1)+1):
                    grid.add((x0, y))
            elif y0 == y1:
                for x in range(min(x0, x1), max(x0, x1)+1):
                    grid.add((x, y0))

floor = max([y for _, y in grid]) + 2

sand = 0
done = False
first_escape = False
while not done:
    x, y = 500, 0
    while True:
        if y == floor - 1:
            if not first_escape:
                print(sand)
                first_escape = True
            grid.add((x, y))
            sand = sand + 1
            break
        if (x, y+1) not in grid:
            y = y + 1
        elif (x-1, y+1) not in grid:
            x, y = x-1, y+1
        elif (x+1, y+1) not in grid:
            x, y = x+1, y+1
        else:
            grid.add((x, y))
            sand = sand + 1

            if x == 500 and y == 0:
                print(sand)
                done = True

            break
