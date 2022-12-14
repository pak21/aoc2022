#!/usr/bin/env python3

import sys

max_minutes = int(sys.argv[2])

bps = []
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        fields = l.split()
        ore = int(fields[6])
        clay = int(fields[12])
        obsidian = (int(fields[18]), int(fields[21]))
        geode = (int(fields[27]), int(fields[30]))
        max_ore_cost = max(ore, clay, obsidian[0], geode[0])
        bps.append((ore, clay, obsidian, geode, max_ore_cost))

def build_ore(state, ore_robot_cost):
    return (
        state[0] + 1, state[1] - ore_robot_cost,
        state[2], state[3],
        state[4], state[5],
        state[6], state[7],
    )

def build_clay(state, clay_robot_cost):
    return (
        state[0], state[1] - clay_robot_cost,
        state[2] + 1, state[3],
        state[4], state[5],
        state[6], state[7],
    )

def build_obsidian(state, obsidian_robot_cost):
    return (
        state[0], state[1] - obsidian_robot_cost[0],
        state[2], state[3] - obsidian_robot_cost[1],
        state[4] + 1, state[5],
        state[6], state[7],
    )

def build_geode(state, geode_robot_cost):
    return (
        state[0], state[1] - geode_robot_cost[0],
        state[2], state[3],
        state[4], state[5] - geode_robot_cost[1],
        state[6] + 1, state[7],
    )

def collect(state):
    return (
        state[0], state[1] + state[0],
        state[2], state[3] + state[2],
        state[4], state[5] + state[4],
        state[6], state[7] + state[6],
    )

def run_minute(state, bp):
    collected = collect(state)

    yield collected

    if state[1] >= bp[0] and state[0] < bp[4]:
        yield build_ore(collected, bp[0])

    if state[1] >= bp[1] and state[2] < bp[2][1]:
        yield build_clay(collected, bp[1])

    if state[1] >= bp[2][0] and state[3] >= bp[2][1] and state[4] < bp[3][1]:
        yield build_obsidian(collected, bp[2])

    if state[1] >= bp[3][0] and state[5] >= bp[3][1]:
        yield build_geode(collected, bp[3])

def run_bp(bp):
    initial_state = (1, 0, 0, 0, 0, 0, 0, 0)

    seen = {initial_state: 0}
    todo = [(initial_state, 0)]

    max_geodes = 0

    while todo:
        state, minutes = todo.pop()

        new_minutes = minutes + 1
        for ns in run_minute(state, bp):
            if seen.get(ns, max_minutes + 1) > new_minutes:
                if ns[7] > max_geodes:
                    max_geodes = ns[7]

                to_go = max_minutes - new_minutes
                max_collectible = ns[7] + (ns[6] * to_go) + (to_go * (to_go - 1) // 2)
                if max_collectible <= max_geodes:
                    continue

                seen[ns] = new_minutes
                todo.append((ns, new_minutes))

    return max_geodes, len(seen)

part1 = 0
part2 = 1
for i, bp in enumerate(bps, 1):
    max_geodes, state_count = run_bp(bp)
    part1 += i * max_geodes
    part2 *= max_geodes
    print(f'Blueprint {i} found {max_geodes} geodes after {state_count} states; results are now {part1}, {part2}')
