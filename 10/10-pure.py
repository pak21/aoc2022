#!/usr/bin/env python3

import sys

def clocktick(state):
    char = '#' if abs((state['t'] % 40) - state['x']) <= 1 else ' '
    new_t = state['t'] + 1

    part1_increase = new_t * state['x'] if new_t % 40 == 20 else 0
    maybe_newline = '\n' if new_t % 40 == 0 else ''

    return {
        't': new_t,
        'x': state['x'],
        'part1': state['part1'] + part1_increase,
        'part2': state['part2'] + char + maybe_newline
    }

def addx(state, a):
    new_state = clocktick(clocktick(state))
    return {
        't': new_state['t'],
        'x': new_state['x'] + a,
        'part1': new_state['part1'],
        'part2': new_state['part2']
    }

def parse(words):
    match words[0]:
        case 'noop':
            return lambda s: clocktick(s)
        case 'addx':
            return lambda s: addx(s, int(words[1]))
        case _:
            raise Exception(f'Unknown opcode {words[0]}')

with open(sys.argv[1]) as f:
    program = [parse(l.rstrip().split()) for l in f]

def interpret(program, state):
    return interpret(program[1:], program[0](state)) if program else state

final_state = interpret(program, {'t': 0, 'x': 1, 'part1': 0, 'part2': ''})

print(final_state['part1'])
print(final_state['part2'])
