#!/usr/bin/env python3

import collections
import sys

import numpy as np

target_row = int(sys.argv[2])

data = []
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        f = l.split()
        sx = int(f[2][2:-1])
        sy = int(f[3][2:-1])
        nx = int(f[8][2:-1])
        ny = int(f[9][2:])
        data.append(((sx, sy), (nx, ny)))

empty_ranges = []
for (sx, sy), (nx, ny) in data:
    dist = abs(nx-sx) + abs(ny-sy)
    target_row_delta = dist - abs(target_row-sy)
    if target_row_delta < 0:
        continue
    min_x = sx-target_row_delta
    max_x = sx+target_row_delta
    if min_x > max_x:
        min_x, max_x = max_x, min_x
    print(sx, sy, nx, ny, dist, target_row_delta, min_x, max_x)
    empty_ranges.append((min_x, max_x))

print(empty_ranges)

empty = set()
for min_x, max_x in empty_ranges:
    for x in range(min_x, max_x+1):
        empty.add(x)

for _, (nx, ny) in data:
    if ny == target_row and nx in empty:
        empty.remove(nx)

print(len(empty))
