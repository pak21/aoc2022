#!/usr/bin/env python3

import sys

import vm

def pretick(vm0, puzzle0):
    video = '#' if abs((vm0['t'] % 40) - vm0['x']) <= 1 else ' '
    return {**puzzle0, 2: puzzle0[2] + video}

def posttick(vm0, puzzle0):
    match vm0['t'] % 40:
        case 0:
            return {**puzzle0, 2: puzzle0[2] + '\n'}
        case 20:
            return {**puzzle0, 1: puzzle0[1] + vm0['t'] * vm0['x']}
        case _:
            return puzzle0

interpreter = vm.Interpreter(pretick, posttick)
interpreter.parse(sys.argv[1])
final_vm, final_puzzle = interpreter.run({'t': 0, 'x': 1}, {1: 0, 2: ''})

for v in final_puzzle.values():
    print(v)
