#!/usr/bin/env python3

import collections
import sys

import numpy as np

with open(sys.argv[1]) as f:
    grid = np.array([[c == '#' for c in l.strip()] for l in f])

elves = {k for k, v in np.ndenumerate(grid) if v}

def prop_n(y, x, elves, proposed):
    if (y-1, x-1) not in elves and (y-1, x) not in elves and (y-1, x+1) not in elves:
        proposed[(y-1, x)].append((y, x))
        return True
    return False
    
def prop_s(y, x, elves, proposed):
    if (y+1, x-1) not in elves and (y+1, x) not in elves and (y+1, x+1) not in elves:
        proposed[(y+1, x)].append((y, x))
        return True
    return False

def prop_w(y, x, elves, proposed):
    if (y-1, x-1) not in elves and (y, x-1) not in elves and (y+1, x-1) not in elves:
        proposed[(y, x-1)].append((y, x))
        return True
    return False

def prop_e(y, x, elves, proposed):
    if (y-1, x+1) not in elves and (y, x+1) not in elves and (y+1, x+1) not in elves:
        proposed[(y, x+1)].append((y, x))
        return True
    return False

PROPS = [prop_n, prop_s, prop_w, prop_e]

def do_round(elves, n):
    somebody_moved = False
    proposed = collections.defaultdict(list)

    for y, x in elves:

        found = False
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue

                if (y+dy, x+dx) in elves:
                    found = True
                    break

        if found:
            if not PROPS[(n+0) % 4](y, x, elves, proposed):
                if not PROPS[(n+1) % 4](y, x, elves, proposed):
                    if not PROPS[(n+2) % 4](y, x, elves, proposed):
                        PROPS[(n+3) % 4](y, x, elves, proposed)
                
    for (ty, tx), movers in proposed.items():
        if len(movers) == 1:
            elves.remove(movers[0])
            elves.add((ty, tx))
            somebody_moved = True

    return somebody_moved

def score(elves):
    s = 0
    min_y = min([y for y, _ in elves])
    max_y = max([y for y, _ in elves])
    min_x = min([x for _, x in elves])
    max_x = max([x for _, x in elves])

    s = (max_y - min_y + 1) * (max_x - min_x + 1) - len(elves)
    return s

r = 0
while do_round(elves, r):
    r += 1
    if r == 10:
        print(score(elves))

print(r+1)
