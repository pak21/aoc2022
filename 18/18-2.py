#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    cubes = {tuple([int(c) for c in l.rstrip().split(',')]) for l in f}

min_x = min([x for x, y, z in cubes]) - 1
max_x = max([x for x, y, z in cubes]) + 1

min_y = min([y for x, y, z in cubes]) - 1
max_y = max([y for x, y, z in cubes]) + 1

min_z = min([z for x, y, z in cubes]) - 1
max_z = max([z for x, y, z in cubes]) + 1

start = (0, 0, 0)
todo = [start]
seen = {start}

exposed = 0

while todo:
    x, y, z = todo.pop()

    for x0, y0, z0 in [
        (x-1, y, z),
        (x+1, y, z),
        (x, y-1, z),
        (x, y+1, z),
        (x, y, z-1),
        (x, y, z+1),
    ]:
        if (x0, y0, z0) in seen:
            continue

        if x0 < min_x or x0 > max_x or y0 < min_y or y0 > max_y or z0 < min_z or z0 > max_z:
            continue

        if (x0, y0, z0) in cubes:
            exposed += 1
            continue

        todo.append((x0, y0, z0))
        seen.add((x0, y0, z0))

print(exposed)
