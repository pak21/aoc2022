#!/usr/bin/env python3

import collections
import sys

def prop_ns(y, x, elves):
    return (y, x) if (y, x-1) not in elves and (y, x) not in elves and (y, x+1) not in elves else None

def prop_ew(y, x, elves):
    return (y, x) if (y-1, x) not in elves and (y, x) not in elves and (y+1, x) not in elves else None

LOOKS = [(y, x) for y in range(-1, 2) for x in range(-1, 2) if (y, x) != (0, 0)]

PROPS = [
    lambda y, x, e: prop_ns(y-1, x, e),
    lambda y, x, e: prop_ns(y+1, x, e),
    lambda y, x, e: prop_ew(y, x-1, e),
    lambda y, x, e: prop_ew(y, x+1, e)
]

def do_round(elves, n):
    somebody_moved = False
    proposed = collections.defaultdict(list)

    for y, x in elves:
        if any([(y+dy, x+dx) in elves for dy, dx in LOOKS]):
            for i in range(4):
                move = PROPS[(n+i) % 4](y, x, elves)
                if move:
                    proposed[move].append((y, x))
                    break
                
    for (ty, tx), movers in proposed.items():
        if len(movers) == 1:
            elves.remove(movers[0])
            elves.add((ty, tx))
            somebody_moved = True

    return somebody_moved

def score(elves):
    min_y = min([y for y, _ in elves])
    max_y = max([y for y, _ in elves])
    min_x = min([x for _, x in elves])
    max_x = max([x for _, x in elves])

    return (max_y - min_y + 1) * (max_x - min_x + 1) - len(elves)

with open(sys.argv[1]) as f:
    elves = {(y, x) for y, l in enumerate(f) for x, c in enumerate(l) if c == '#'}

r = 0
while do_round(elves, r):
    r += 1
    if r == 10:
        print(score(elves))

print(r+1)
