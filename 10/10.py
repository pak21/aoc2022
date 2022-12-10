#!/usr/bin/env python3

import sys

state = {
    't': 0,
    'x': 1,
    'part1': 0, 
    'part2': ''
}

def clocktick(state):
    video = '#' if abs((state['t'] % 40) - state['x']) <= 1 else ' '
    state['part2'] += video

    state['t'] += 1

    match state['t'] % 40:
        case 0:
            state['part2'] += '\n'

        case 20:
            state['part1'] += state['t'] * state['x']

def noop(state, a):
    clocktick(state)

def addx(state, a):
    clocktick(state)
    clocktick(state)
    state['x'] += a

INSTRUCTIONS = {
    'addx': addx,
    'noop': noop,
}

program = []
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        words = l.split()
        match words[0]:
            case 'noop':
                program.append((noop, None))
            case 'addx':
                program.append((addx, int(words[1])))
            case _:
                raise Exception(f'Unknown opcode {words[0]}')

for opcode, a in program:
    opcode(state, a)

print(state['part1'])
print(state['part2'])
