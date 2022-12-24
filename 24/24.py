#!/usr/bin/env python3

import collections
import sys

import numpy as np

B_RIGHT = 1
B_UP = 2
B_LEFT = 4
B_DOWN = 8

with open(sys.argv[1]) as f:
    grid = np.array([[c for c in l.strip()] for l in f])

max_y = grid.shape[0] - 2
max_x = grid.shape[1] - 2

BLIZZARD_TYPES = {
    '>': B_RIGHT,
    '^': B_UP,
    '<': B_LEFT,
    'v': B_DOWN,
}

blizzards = {(y-1, x-1): BLIZZARD_TYPES[c] for (y, x), c in np.ndenumerate(grid) if c in BLIZZARD_TYPES}

blizzard_states = [blizzards]

MOVES = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 0),
]

def move_blizzards(blizzards, max_y, max_x):
    new_blizzards = collections.defaultdict(int)
    for (y, x), bs in blizzards.items():
        if bs & B_RIGHT:
            new_location = (y, (x + 1) % max_x)
            new_blizzards[new_location] |= B_RIGHT

        if bs & B_UP:
            new_location = ((y - 1) % max_y, x)
            new_blizzards[new_location] |= B_UP

        if bs & B_LEFT:
            new_location = (y, (x - 1) % max_x)
            new_blizzards[new_location] |= B_LEFT

        if bs & B_DOWN:
            new_location = ((y + 1) % max_y, x)
            new_blizzards[new_location] |= B_DOWN

    return new_blizzards

def dump(blizzards, max_y, max_x):
    for y in range(0, max_y):
        l = ''
        for x in range(0, max_x):
            c = None
            n = 0
            b = blizzards.get((y, x), 0)
            if b & B_RIGHT:
                n += 1
                c = '>'
            if b & B_UP:
                n += 1
                c = '^'
            if b & B_LEFT:
                n += 1
                c = '<'
            if b & B_DOWN:
                n += 1
                c = 'v'

            match n:
                case 0:
                    c2 = '.'
                case 1:
                    c2 = c
                case _:
                    c2 = str(n)

            l += c2
        print(l)
    print()

initial_location = (-1, 0)
initial_state = (initial_location, 0)
todo = [initial_state]
seen = {initial_state}

while todo:
    location, turns = todo.pop(0)

    try:
        blizzards = blizzard_states[turns+1]
    except IndexError:
        blizzards = move_blizzards(blizzard_states[-1], max_y, max_x)
        blizzard_states.append(blizzards)
        print(f'Turn {turns+1}')

    for move in MOVES:
        new_y = location[0] + move[0]
        new_x = location[1] + move[1]

        if new_y == max_y and new_x == max_x - 1:
            print(turns+1)
            print(len(seen))
            raise Exception(location, move, turns)

        if (new_y < 0 or new_y == max_y or new_x < 0 or new_x == max_x) and (new_y, new_x) != initial_location:
            continue

        if (new_y, new_x) not in blizzards:
            new_state = ((new_y, new_x), turns + 1)
            if new_state not in seen:
                todo.append(((new_y, new_x), turns + 1))
                seen.add(new_state)

raise Exception('No solution found')
