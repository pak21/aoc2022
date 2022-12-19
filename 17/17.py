#!/usr/bin/env python3

import collections
import sys

import numpy as np

ROCKS = [
    [
        [1, 1, 1, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ],
    [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    [
        [1],
        [1],
        [1],
        [1],
    ],
    [
        [1, 1],
        [1, 1],
    ]
]

with open(sys.argv[1]) as f:
    jets = [1 if c == '>' else -1 for c in f.read().rstrip()]

rocks = [np.array(r) for r in ROCKS]

chamber = set()
highest = -1
current_rock_id = 0
jet_id = 0

WIDTH = 7

def intersect(chamber, rock, x, y):
    for y0 in range(rock.shape[0]):
        for x0 in range(rock.shape[1]):
            x1 = x + x0
            y1 = y - y0
            if rock[y0, x0] and (x1, y1) in chamber:
                return True

    return False

def dump(chamber, highest):
    for y in range(highest, -1, -1):
        l = ''
        for x in range(0, 7):
            l += '#' if (x, y) in chamber else '.'
        print(l)

for i in range(2022):
    rock = rocks[current_rock_id]
    x, y = 2, (highest + 3 + rock.shape[0])

    while True:
        jet = jets[jet_id]

        # Jet movement
        jet_move = True
        if jet == 1:
            if x + rock.shape[1] >= WIDTH:
                jet_move = False
        else:
            if x == 0:
                jet_move = False

        if jet_move:
            if intersect(chamber, rock, x + jet, y):
                jet_move = False

        if jet_move:
            x += jet

        jet_id = (jet_id + 1) % len(jets)

        # Falling
        can_fall = True
        if y - rock.shape[0] + 1 == 0:
            # Hit bottom
            can_fall = False

        if can_fall:
            if intersect(chamber, rock, x, y - 1):
                can_fall = False

        if can_fall:
            y -= 1
        else:
            break

    for y0 in range(rock.shape[0]):
        for x0 in range(rock.shape[1]):
            if rock[y0, x0]:
                chamber.add((x+x0, y-y0))
            if y > highest:
                highest = y

    current_rock_id = (current_rock_id + 1) % len(rocks)

print(highest+1)
