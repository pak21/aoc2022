#!/usr/bin/env python3

import collections
import sys

B_RIGHT = 1
B_UP = 2
B_LEFT = 4
B_DOWN = 8

BLIZZARD_TYPES = {
    '>': B_RIGHT,
    '^': B_UP,
    '<': B_LEFT,
    'v': B_DOWN,
}

with open(sys.argv[1]) as f:
    blizzards = {
        (y-1, x-1): BLIZZARD_TYPES[c]
        for y, l in enumerate(f)
        for x, c in enumerate(l)
        if c in BLIZZARD_TYPES
    }

max_y = max([y for y, _ in blizzards]) + 1
max_x = max([x for _, x in blizzards]) + 1

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

MOVES = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 0),
]

def run(initial_location, initial_turns, blizzards, target_location):
    initial_state = (initial_location, initial_turns)
    todo = [initial_state]
    seen = {initial_state}

    max_turns = initial_turns

    while todo:
        location, turns = todo.pop(0)

        new_turns = turns + 1
        if new_turns > max_turns:
            blizzards = move_blizzards(blizzards, max_y, max_x)
            max_turns = new_turns

        for move in MOVES:
            new_y, new_x = location[0] + move[0], location[1] + move[1]

            if (new_y, new_x) == target_location:
                print(f'Reached {target_location} after {new_turns} turns (saw {len(seen)} states)')
                return new_turns, blizzards

            if (new_y < 0 or new_y == max_y or new_x < 0 or new_x == max_x) and (new_y, new_x) != initial_location:
                continue

            if (new_y, new_x) not in blizzards:
                new_state = ((new_y, new_x), new_turns)
                if new_state not in seen:
                    todo.append(new_state)
                    seen.add(new_state)

    raise Exception('No solution found')

start_loc = (-1, 0)
end_loc = (max_y, max_x - 1)

part1, blizzards = run(start_loc, 0, blizzards, end_loc)
part2a, blizzards = run(end_loc, part1, blizzards, start_loc)
part2, _ = run(start_loc, part2a, blizzards, end_loc)

print(part1, part2)
