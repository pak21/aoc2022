#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    cave = {}
    for l in [x.rstrip() for x in f]:
        fields = l.split()
        flow_rate = int(fields[4][5:-1])
        tunnels = [x.replace(',', '') for x in fields[9:]]
        cave[fields[1]] = (flow_rate, tunnels)

def open_valve(state, valve):
    old_location, old_open, old_flow_rate, old_turns, old_pressure = state
    return (old_location, old_open.union({valve}), old_flow_rate + cave[valve][0], old_turns + 1, old_pressure + old_flow_rate)

def move(state, location):
    old_location, old_open, old_flow_rate, old_turns, old_pressure = state
    return (location, old_open, old_flow_rate, old_turns + 1, old_pressure + old_flow_rate)

def moves(state):
    old_location, old_open, old_flow_rate, turns, pressure = state

    for new_location in cave[old_location][1]:
        yield move(state, new_location)

    if old_location not in old_open and cave[old_location][0] > 0:
        yield open_valve(state, old_location)

def state_to_seen(state):
    location, open_valves, flow_rate, turns, pressure = state
    return (location, tuple(sorted(tuple(open_valves))))

initial_state = ('AA', set(), 0, 1, 0)
todo = [initial_state]
seen = {state_to_seen(initial_state): initial_state[4]}

all_valves = {v for v, (fr, _) in cave.items() if fr > 0}

predicted_best = 0

while todo:
    state = todo.pop(0)
    if state[3] == 31:
        continue
    for ns in moves(state):
        if ns[1] == all_valves:
            predicted = ns[4] + (31 - ns[3]) * ns[2]
            if predicted > predicted_best:
                predicted_best = predicted
                print(predicted_best, ns)
        else:
            ns_key = state_to_seen(ns)
            if ns_key not in seen or ns[4] > seen[ns_key]:
                todo.append(ns)
                seen[ns_key] = ns[4]

print(max(seen.values()))
