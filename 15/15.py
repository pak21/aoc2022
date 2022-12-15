#!/usr/bin/env python3

import sys

beacons_on_target_row = set()

target_row = int(sys.argv[2])

data = []
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        f = l.split()
        sx = int(f[2][2:-1])
        sy = int(f[3][2:-1])
        nx = int(f[8][2:-1])
        ny = int(f[9][2:])
        dist = abs(nx-sx) + abs(ny-sy)
        data.append(((sx, sy), dist))

        if ny == target_row:
            beacons_on_target_row.add(nx)

part1 = None
part2 = None

for row in range(0, 4000000):
    empty_ranges = []
    for (sx, sy), dist in data:
        row_delta = dist - abs(row-sy)
        if row_delta < 0:
            continue
        empty_ranges.append((sx-row_delta, sx+row_delta))

    empty_ranges = sorted(empty_ranges)
    min_x, max_x = empty_ranges[0]
    for new_min_x, new_max_x in empty_ranges[1:]:
        if new_min_x > max_x + 1:
            part2 = (max_x + 1) * 4000000 + row
            break

        min_x = min(min_x, new_min_x)
        max_x = max(max_x, new_max_x)

    if row == target_row:
        part1 = max_x - min_x + 1 - len([x for x in beacons_on_target_row if x >= min_x and x <= max_x])
        
    if part1 and part2:
        break

print(part1, part2)
