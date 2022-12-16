#!/usr/bin/env python3

import collections
import sys

cave_dict = {}
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        fields = l.split()
        flow_rate = int(fields[4][5:-1])
        tunnels = [x.replace(',', '') for x in fields[9:]]
        cave_dict[fields[1]] = (flow_rate, tunnels)

indexes = {k: i for i, k in enumerate(cave_dict)}
cave = [
    (
        flow_rate,
        [indexes[t] for t in tunnels]
    )
    for k, (flow_rate, tunnels)
    in cave_dict.items()
]

def open_valve(state, valve):
    location, valves, flow_rate, turns, pressure = state
    return (location, valves | 2**valve, flow_rate + cave[valve][0], turns + 1, pressure + flow_rate)

def move(state, location):
    _, valves, flow_rate, turns, pressure = state
    return (location, valves, flow_rate, turns + 1, pressure + flow_rate)

def moves_part1(state):
    old_location, old_open, old_flow_rate, turns, pressure = state

    for new_location in cave[old_location][1]:
        yield move(state, new_location)

    if not (old_open & (2**old_location)) and cave[old_location][0] > 0:
        yield open_valve(state, old_location)

def move_and_move(state, location1, location2):
    _, valves, flow_rate, turns, pressure = state
    new_locations = (location1, location2) if location1 < location2 else (location2, location1)
    return (new_locations, valves, flow_rate, turns + 1, pressure + flow_rate)

def move_and_open(state, location1, valve):
    (_, location2), valves, flow_rate, turns, pressure = state
    new_locations = (location1, location2) if location1 < location2 else (location2, location1)
    return (new_locations, valves | 2**valve, flow_rate + cave[valve][0], turns + 1, pressure + flow_rate)

def open_and_move(state, valve, location2):
    (location1, _), valves, flow_rate, turns, pressure = state
    new_locations = (location1, location2) if location1 < location2 else (location2, location1)
    return (new_locations, valves | 2**valve, flow_rate + cave[valve][0], turns + 1, pressure + flow_rate)

def open_and_open(state, valve1, valve2):
    locations, valves, flow_rate, turns, pressure = state
    return (locations, valves | 2**valve1 | 2**valve2, flow_rate + cave[valve1][0] + cave[valve2][0], turns + 1, pressure + flow_rate)

def moves_part2(state):
    (old_location1, old_location2), valves, flow_rate, turns, pressure = state

    for new_location1 in cave[old_location1][1]:
        for new_location2 in cave[old_location2][1]:
            yield move_and_move(state, new_location1, new_location2)

        if not (valves & (2**old_location2)) and cave[old_location2][0] > 0:
            yield move_and_open(state, new_location1, old_location2)

    if not (valves & (2**old_location1)) and cave[old_location1][0] > 0:
        for new_location2 in cave[old_location2][1]:
            yield open_and_move(state, old_location1, new_location2)

        if old_location1 != old_location2 and not (valves & (2**old_location2)) and cave[old_location2][0] > 0:
            yield open_and_open(state, old_location1, old_location2)

starting_location = indexes['AA']
if int(sys.argv[2]):
    initial_state = ((starting_location, starting_location), 0, 0, 0, 0)
    moves = moves_part2
    max_turns = 26
else:
    initial_state = (starting_location, 0, 0, 0, 0)
    moves = moves_part1
    max_turns = 30

todo = [initial_state]
seen = collections.defaultdict(dict)
seen[initial_state[0]][initial_state[1]] = initial_state[4]

best_so_far = 0

def prune(state, seen):
    for valves, pressure in seen.items():
        if (state[1] & ~valves) == 0 and pressure > state[4]:
            return True

    return False

def should(state, seen):
    result = True
    to_remove = []

    for valves, pressure in seen.items():

        extra_valves_new = state[1] & ~valves
        if extra_valves_new == 0 and pressure >= state[4]:
            result = False
            break

        extra_valves_old = valves & ~state[1]
        if extra_valves_old == 0 and state[4] > pressure:
            to_remove.append(valves)

    for k in to_remove:
        del seen[k]

    if result:
        seen[state[1]] = state[4]

    return result

while todo:
    state = todo.pop(0)

    if prune(state, seen[state[0]]):
        continue

    for ns in moves(state):
        if should(ns, seen[ns[0]]):
            if ns[3] < max_turns:
                todo.append(ns)
            if ns[4] > best_so_far:
                best_so_far = ns[4]

print(best_so_far)
