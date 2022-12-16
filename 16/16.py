#!/usr/bin/env python3

import collections
import sys

MAX_TURNS = 30 + 1

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

def merge_valves(old_valves, new_valve):
    return old_valves | (2**new_valve)

def open_valve(state, valve):
    old_location, old_open, old_flow_rate, old_turns, old_pressure = state
    return (old_location, merge_valves(old_open, valve), old_flow_rate + cave[valve][0], old_turns + 1, old_pressure + old_flow_rate)

def move(state, location):
    old_location, old_open, old_flow_rate, old_turns, old_pressure = state
    return (location, old_open, old_flow_rate, old_turns + 1, old_pressure + old_flow_rate)

def moves(state):
    old_location, old_open, old_flow_rate, turns, pressure = state

    if turns == MAX_TURNS:
        return

    for new_location in cave[old_location][1]:
        yield move(state, new_location)

    if not (old_open & (2**old_location)) and cave[old_location][0] > 0:
        yield open_valve(state, old_location)

initial_state = (indexes['AA'], 0, 0, 1, 0)
todo = [initial_state]
seen = [{} for _ in cave]
seen[initial_state[0]][initial_state[1]] = initial_state[4]

best_so_far = 0

def should(state, seen, foo):
    result = True
    to_remove = []

    for valves, pressure in seen[state[0]].items():

        extra_valves_new = state[1] & ~valves
        if extra_valves_new == 0 and pressure >= state[4] + foo:
            result = False
            break

        extra_valves_old = valves & ~state[1]
        if extra_valves_old == 0 and state[4] > pressure:
            to_remove.append(valves)

    if result:
        for k in to_remove:
            del seen[state[0]][k]

    return result

def dump_seen(s):
    for k, v in s.items():
        print(k)
        for k2, v2 in v.items():
            print(f'{k2:x}, {v2}')
        print()

while todo:
    state = todo.pop(0)

    if not should(state, seen, 1):
        continue

    for ns in moves(state):
        if should(ns, seen, 0):
            todo.append(ns)
            seen[ns[0]][ns[1]] = ns[4]
            if ns[4] > best_so_far:
                best_so_far = ns[4]

print(best_so_far)
