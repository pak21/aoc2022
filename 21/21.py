#!/usr/bin/env python3

import collections
import sys

import numpy as np

monkeys = {}
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        args = l.split()
        monkeys[args[0][:-1]] = args[1:]

values = {}

def eval_monkey(monkey, monkeys, values):
    args = monkeys[monkey]
    if len(args) == 1:
        value = int(args[0])
    else:
        value1 = eval_monkey(args[0], monkeys, values)
        value2 = eval_monkey(args[2], monkeys, values)
        match args[1]:
            case '+':
                value = value1 + value2
            case '-':
                value = value1 - value2
            case '*':
                value = value1 * value2
            case '/':
                value = value1 / value2
            case _:
                raise Exception(args[1])

    values[monkey] = value
    return value

print(int(eval_monkey('root', monkeys, values)))
