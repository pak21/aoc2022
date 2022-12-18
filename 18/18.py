#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    cubes = {tuple([int(c) for c in l.rstrip().split(',')]) for l in f}

exposed = 0
for x, y, z in cubes:
    exposed += 6
    if (x-1, y, z) in cubes:
        exposed -= 1
    if (x+1, y, z) in cubes:
        exposed -= 1
    if (x, y-1, z) in cubes:
        exposed -= 1
    if (x, y+1, z) in cubes:
        exposed -= 1
    if (x, y, z-1) in cubes:
        exposed -= 1
    if (x, y, z+1) in cubes:
        exposed -= 1

print(exposed)
