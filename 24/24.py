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

def run(initial_location, initial_turns, target_location):
    initial_state = (initial_location, initial_turns)
    todo = [initial_state]
    seen = {initial_state}

    while todo:
        location, turns = todo.pop(0)

        try:
            blizzards = blizzard_states[turns+1]
        except IndexError:
            blizzards = move_blizzards(blizzard_states[-1], max_y, max_x)
            blizzard_states.append(blizzards)

        for move in MOVES:
            new_y = location[0] + move[0]
            new_x = location[1] + move[1]

            if (new_y, new_x) == target_location:
                print(f'Reached {target_location} after {turns+1} turns and {len(seen)} states')
                return turns+1

            if (new_y < 0 or new_y == max_y or new_x < 0 or new_x == max_x) and (new_y, new_x) != initial_location:
                continue

            if (new_y, new_x) not in blizzards:
                new_state = ((new_y, new_x), turns + 1)
                if new_state not in seen:
                    todo.append(((new_y, new_x), turns + 1))
                    seen.add(new_state)

    raise Exception('No solution found')

start_loc = (-1, 0)
end_loc = (max_y, max_x - 1)

part1 = run(start_loc, 0, end_loc)
part2a = run(end_loc, part1, start_loc)
part2 = run(start_loc, part2a, end_loc)
