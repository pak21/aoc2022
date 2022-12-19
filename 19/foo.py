#!/usr/bin/env python3

import sys

import numpy as np

max_minutes = int(sys.argv[2])

bps = []
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        fields = l.split()
        ore = int(fields[6])
        clay = int(fields[12])
        obsidian = (int(fields[18]), int(fields[21]))
        geode = (int(fields[27]), int(fields[30]))
        bps.append((ore, clay, obsidian, geode))

def build_ore(state, bp):
    return (
        state[0] + 1,
        state[1] - bp[0],
        state[2],
        state[3],
        state[4],
        state[5],
        state[6],
        state[7],
        state[8]
    )

def build_clay(state, bp):
    return (
        state[0],
        state[1] - bp[1],
        state[2] + 1,
        state[3],
        state[4],
        state[5],
        state[6],
        state[7],
        state[8]
    )

def build_obsidian(state, bp):
    return (
        state[0],
        state[1] - bp[2][0],
        state[2],
        state[3] - bp[2][1],
        state[4] + 1,
        state[5],
        state[6],
        state[7],
        state[8]
    )

def build_geode(state, bp):
    return (
        state[0],
        state[1] - bp[3][0],
        state[2],
        state[3],
        state[4],
        state[5] - bp[3][1],
        state[6] + 1,
        state[7],
        state[8]
    )

def collect(state):
    return (
        state[0],
        state[1] + state[0],
        state[2],
        state[3] + state[2],
        state[4],
        state[5] + state[4],
        state[6],
        state[7] + state[6],
        state[8] + 1
    )

def run_minute(state, bp, max_geodes):
    minutes_to_go = max_minutes - state[8]

    if minutes_to_go == 0:
        return

    max_collectible = state[7] + (state[6] * minutes_to_go) + (minutes_to_go * (minutes_to_go - 1) // 2)

    if max_collectible <= max_geodes:
        return

    collected = collect(state)

    yield collected

    if state[1] >= bp[0]:
        yield build_ore(collected, bp)

    if state[1] >= bp[1]:
        yield build_clay(collected, bp)

    if state[1] >= bp[2][0] and state[3] >= bp[2][1]:
        yield build_obsidian(collected, bp)

    if state[1] >= bp[3][0] and state[5] >= bp[3][1]:
        yield build_geode(collected, bp)

def run_bp(bp):
    initial_state = (1, 0, 0, 0, 0, 0, 0, 0, 0)

    seen = {initial_state}
    todo = [initial_state]

    max_geodes = 0

    while todo:
        state = todo.pop()
        for ns in run_minute(state, bp, max_geodes):
            if ns not in seen:
                seen.add(ns)
                todo.append(ns)

                if ns[7] > max_geodes:
                    max_geodes = ns[7]

    return max_geodes, len(seen)

part1 = 0
part2 = 1
for i, bp in enumerate(bps):
    max_geodes, state_count = run_bp(bps[i])
    part1 += (i+1) * max_geodes
    part2 *= max_geodes
    print(f'Blueprint {i+1} found {max_geodes} geodes after {state_count} states; results are now {part1}, {part2}')
