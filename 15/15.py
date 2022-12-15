#!/usr/bin/env python3

import functools
import sys

def reduce_ranges(a, b):
    old_min_x, old_max_x, maybe_gap = a
    new_min_x, new_max_x = b

    if new_min_x > old_max_x + 1:
        if maybe_gap:
            raise Exception('Found multiple gaps')
        maybe_gap = old_max_x + 1

    return min(old_min_x, new_min_x), max(old_max_x, new_max_x), maybe_gap

target_row = int(sys.argv[2])

sensors = []
beacons_on_target_row = set()
with open(sys.argv[1]) as f:
    for line in [x.rstrip() for x in f]:
        fields = line.split()
        sx = int(fields[2][2:-1])
        sy = int(fields[3][2:-1])
        nx = int(fields[8][2:-1])
        ny = int(fields[9][2:])
        dist = abs(nx-sx) + abs(ny-sy)
        sensors.append((sx, sy, dist))

        if ny == target_row:
            beacons_on_target_row.add(nx)

part1 = None
part2 = None

for row in range(0, 4000000):
    empty_ranges = [
        (sx-row_delta, sx+row_delta)
        for sx, row_delta
        in [
            (sx, dist - abs(row-sy))
            for sx, sy, dist
            in sensors
        ]
        if row_delta >= 0
    ]

    sorted_ranges = sorted(empty_ranges)
    min_x, max_x, gap = functools.reduce(reduce_ranges, sorted_ranges[1:], (*sorted_ranges[0], None))

    if gap:
        part2 = gap * 4000000 + row

    if row == target_row:
        part1 = max_x - min_x + 1 - len(beacons_on_target_row)
        
    if part1 and part2:
        break

print(part1, part2)
