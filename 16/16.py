#!/usr/bin/env python3

import sys

MAX_TURNS = 30 + 1

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

    if old_location not in old_open and cave[old_location][0] > 0:
        yield open_valve(state, old_location)

def state_to_seen(state):
    location, open_valves, flow_rate, turns, pressure = state
    return (location, open_valves)

initial_state = ('AA', tuple(), 0, 1, 0)
todo = [initial_state]
seen = {state_to_seen(initial_state): initial_state[4]}

all_pressure = sum([fr for (fr, _) in cave.values()])
print(all_pressure)

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
