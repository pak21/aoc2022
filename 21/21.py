#!/usr/bin/env python3

import sys

monkeys = {}
with open(sys.argv[1]) as f:
    for args in [x.rstrip().split() for x in f]:
        monkeys[args[0][:-1]] = args[1:]

def eval_monkey(monkey, monkeys):
    args = monkeys[monkey]
    if len(args) == 1:
        return int(args[0])
    else:
        value1 = eval_monkey(args[0], monkeys)
        value2 = eval_monkey(args[2], monkeys)
        match args[1]:
            case '+':
                return value1 + value2
            case '-':
                return value1 - value2
            case '*':
                return value1 * value2
            case '/':
                return value1 // value2
            case _:
                raise Exception(args[1])

print(eval_monkey('root', monkeys))
