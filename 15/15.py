#!/usr/bin/env python3

import collections
import sys

import numpy as np

data = []
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        f = l.split()
        sx = int(f[2][2:-1])
        sy = int(f[3][2:-1])
        nx = int(f[8][2:-1])
        ny = int(f[9][2:])
        data.append(((sx, sy), (nx, ny)))

empty = set()
for (sx, sy), (nx, ny) in data:
    dist = abs(nx-sx) + abs(ny-sy)
    for y in range(sy-dist, sy+dist+1):
        dx = dist-abs(y-sy)
        x0 = sx-dx
        x1 = sx+dx
        for x in range(x0, x1+1):
            empty.add((x, y))

for _, (nx, ny) in data:
    if (nx, ny) in empty:
        empty.remove((nx, ny))

print(len([a for a in empty if a[1] == 10]))
