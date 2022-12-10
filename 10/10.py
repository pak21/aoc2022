#!/usr/bin/env python3

import sys

import vm

def pretick(state):
    video = '#' if abs((state['t'] % 40) - state['x']) <= 1 else ' '
    return {**state, 'part2': state['part2'] + video}

def posttick(state):
    match state['t'] % 40:
        case 0:
            return {**state, 'part2': state['part2'] + '\n'}
        case 20:
            return {**state, 'part1': state['part1'] + state['t'] * state['x']}
        case _:
            return state

interpreter = vm.Interpreter(pretick, posttick)
interpreter.parse(sys.argv[1])
final_state = interpreter.run({'t': 0, 'x': 1, 'part1': 0, 'part2': ''})

print(final_state['part1'])
print(final_state['part2'])
