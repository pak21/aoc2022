#!/usr/bin/env python3

import sys

import numpy as np

DIRECTIONS = {
    'R': (1, 0),
    'U': (0, -1),
    'L': (-1, 0),
    'D': (0, 1)
}

worm = [(0, 0)] * int(sys.argv[2])
seen = set()

with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        direction, num = l.split()

        for i in range(int(num)):
            worm[0] = (worm[0][0] + DIRECTIONS[direction][0], worm[0][1] + DIRECTIONS[direction][1])
            for j in range(len(worm) - 1):
                dx = worm[j][0] - worm[j+1][0]
                dy = worm[j][1] - worm[j+1][1]
                mx, my = (np.sign(dx), np.sign(dy)) if abs(dx) == 2 or abs(dy) == 2 else (0, 0)
                worm[j+1] = (worm[j+1][0] + mx, worm[j+1][1] + my)

            seen.add(worm[-1])

print(len(seen))
