#!/usr/bin/env python3

import sys

import numpy as np

DIRECTIONS = {
    'R': np.array([1, 0]),
    'U': np.array([0, -1]),
    'L': np.array([-1, 0]),
    'D': np.array([0, 1])
}

worm = [np.array([0, 0])] * int(sys.argv[2])
seen = set()

with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        direction, num = l.split()

        for _ in range(int(num)):
            worm[0] = worm[0] + DIRECTIONS[direction]
            for i in range(len(worm) - 1):
                diff = worm[i] - worm[i+1]
                if np.max(np.abs(diff)) == 2:
                    worm[i+1] = worm[i+1] + np.sign(diff)

            seen.add(tuple(worm[-1]))

print(len(seen))
