#!/usr/bin/env python3

import collections
import sys

import numpy as np

max_target_row = int(sys.argv[2])

data = []
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        f = l.split()
        sx = int(f[2][2:-1])
        sy = int(f[3][2:-1])
        nx = int(f[8][2:-1])
        ny = int(f[9][2:])
        data.append(((sx, sy), (nx, ny)))

for target_row in range(0, max_target_row+1):
    if target_row % 1000 == 0:
        print(target_row)
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
        empty_ranges.append((min_x, max_x))

    empty_ranges = sorted(empty_ranges)
    min_x, max_x = empty_ranges[0]
    for a, b in empty_ranges[1:]:
        if a > max_x:
            print(target_row, max_x, a, empty_ranges)
            result = (max_x + 1) * 4000000 + target_row
            print(result)
            raise Exception('boom')

        min_x = min(min_x, a)
        max_x = max(max_x, b)
