#!/usr/bin/env python3

import sys

state = {
    't': 0,
    'x': 1,
    'part1': 0, 
    'part2': ''
}

def clocktick(state):
    state['part2'] += '#' if abs((state['t'] % 40) - state['x']) <= 1 else ' '

    state['t'] += 1

    match state['t'] % 40:
        case 0:
            state['part2'] += '\n'
        case 20:
            state['part1'] += state['t'] * state['x']

def noop(state):
    clocktick(state)

def addx(state, a):
    clocktick(state)
    clocktick(state)
    state['x'] += a

def parse(words):
    match words[0]:
        case 'noop':
            return lambda s: noop(s)
        case 'addx':
            return lambda s: addx(s, int(words[1]))
        case _:
            raise Exception(f'Unknown opcode {words[0]}')

program = []
with open(sys.argv[1]) as f:
    program = [parse(l.rstrip().split()) for l in f]

for opcode in program:
    opcode(state)

print(state['part1'])
print(state['part2'])
