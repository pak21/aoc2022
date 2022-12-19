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
rows_removed = 0
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

state_hashes = {}
heights = []
rock_count = 0

done = False
while not done:
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

    if y > highest:
        highest = y

    completed = -1
    for y0 in reversed(range(rock.shape[0])):
        for x0 in range(rock.shape[1]):
            if rock[y0, x0]:
                chamber.add((x+x0, y-y0))

        complete = True
        for x0 in range(0, 6):
            if (x0, y-y0) not in chamber:
                complete = False
                break
        if complete:
            if y - y0 > completed:
                completed = y - y0

    if completed != -1:
        chamber = {(x, y - completed - 1) for x, y in chamber if y > completed}
        rows_removed += completed + 1
        highest = max([y for _, y in chamber])

    height = rows_removed + highest + 1
    heights.append(height)

    state_hash = hash((tuple(chamber), jet_id))
    if state_hash in state_hashes:
        old_rock_count = state_hashes[state_hash]
        period = rock_count - old_rock_count
        height_change = height - heights[old_rock_count]
        done = True

    state_hashes[state_hash] = rock_count

    current_rock_id = (current_rock_id + 1) % len(rocks)
    rock_count += 1

target_count = old_rock_count // period * period + 1000000000000 % period
increments = (1000000000000 - target_count) // period
print(heights[target_count-1] + height_change * increments)
