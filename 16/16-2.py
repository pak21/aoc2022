#!/usr/bin/env python3

import sys

MAX_TURNS = 26 + 1

with open(sys.argv[1]) as f:
    cave = {}
    for l in [x.rstrip() for x in f]:
        fields = l.split()
        flow_rate = int(fields[4][5:-1])
        tunnels = [x.replace(',', '') for x in fields[9:]]
        cave[fields[1]] = (flow_rate, tunnels)

def merge_valves(old_valves, new_valve):
    x = set(old_valves)
    x.add(new_valve)
    return tuple(sorted(x))

def merge_valves2(old_valves, new_valve1, new_valve2):
    x = set(old_valves)
    x.add(new_valve1)
    x.add(new_valve2)
    return tuple(sorted(x))

def move_and_move(state, location1, location2):
    _, old_open, old_flow_rate, old_turns, old_pressure = state
    new_locations = (location1, location2) if location1 < location2 else (location2, location1)
    return (new_locations, old_open, old_flow_rate, old_turns + 1, old_pressure + old_flow_rate)

def move_and_open(state, location1, valve):
    (_, location2), old_open, old_flow_rate, old_turns, old_pressure = state
    new_locations = (location1, location2) if location1 < location2 else (location2, location1)
    return (new_locations, merge_valves(old_open, valve), old_flow_rate + cave[valve][0], old_turns + 1, old_pressure + old_flow_rate)

def open_and_move(state, valve, location2):
    (location1, _), old_open, old_flow_rate, old_turns, old_pressure = state
    new_locations = (location1, location2) if location1 < location2 else (location2, location1)
    return (new_locations, merge_valves(old_open, valve), old_flow_rate + cave[valve][0], old_turns + 1, old_pressure + old_flow_rate)

def open_and_open(state, valve1, valve2):
    locations, old_open, old_flow_rate, old_turns, old_pressure = state
    new_open = merge_valves2(old_open, valve1, valve2)
    return (locations, new_open, old_flow_rate + cave[valve1][0] + cave[valve2][0], old_turns + 1, old_pressure + old_flow_rate)

def moves(state):
    (old_location1, old_location2), old_open, old_flow_rate, turns, pressure = state

    if turns == MAX_TURNS:
        return

    for new_location1 in cave[old_location1][1]:
        for new_location2 in cave[old_location2][1]:
            yield move_and_move(state, new_location1, new_location2)

        if old_location2 not in old_open and cave[old_location2][0] > 0:
            yield move_and_open(state, new_location1, old_location2)

    if old_location1 not in old_open and cave[old_location1][0] > 0:
        for new_location2 in cave[old_location2][1]:
            yield open_and_move(state, old_location1, new_location2)

        if old_location1 != old_location2 and old_location2 not in old_open and cave[old_location2][0] > 0:
            yield open_and_open(state, old_location1, old_location2)

def state_to_seen(state):
    locations, open_valves, flow_rate, turns, pressure = state
    return (locations, open_valves)

initial_state = (('AA', 'AA'), tuple(), 0, 1, 0)
todo = [initial_state]
seen = {state_to_seen(initial_state): initial_state[4]}

all_pressure = sum([fr for (fr, _) in cave.values()])

n = 0

best_so_far = 0

while todo:
    state = todo.pop(0)
    n += 1

    key = state_to_seen(state)
    if seen[key] > state[4]:
        continue

    best_possible = state[4] + (MAX_TURNS - state[3]) * all_pressure
    if best_possible < best_so_far:
        continue

    for ns in moves(state):
        ns_key = state_to_seen(ns)
        if ns_key not in seen or ns[4] > seen[ns_key]:
            todo.append(ns)
            seen[ns_key] = ns[4]
            if ns[4] > best_so_far:
                best_so_far = ns[4]
                print(best_so_far, ns)

print(max(seen.values()))
print(n)
