#!/usr/bin/env python3

import builtins
import sys

monkeys = {}
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        args = l.split()
        monkeys[args[0][:-1]] = args[1:]

def eval_monkey(monkey, monkeys):
    args = monkeys[monkey]
    if monkey == 'humn':
        return lambda t: t

    if len(args) == 1:
        return int(args[0])
    else:
        value1 = eval_monkey(args[0], monkeys)
        value2 = eval_monkey(args[2], monkeys)
        match (type(value1), type(value2)):
            case (builtins.int, builtins.int):
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
                        raise Exception(value1, args[1], value2)
            case (builtins.int, _):
                match args[1]:
                    case '+':
                        # value + unknown = target => unknown = target - value
                        return lambda t: value2(t - value1)
                    case '-':
                        # value - unknown = target => unknown = value - target
                        return lambda t: value2(value1 - t)
                    case '*':
                        # value * unknown = target => unknown = target / value
                        return lambda t: value2(t // value1)
                    case '/':
                        # value / unknown = target => unknown = value / target
                        return lambda t: value2(value1 / t)
                    case _:
                        raise Exception(value1, args[1], value2)
            case (_, builtins.int):
                match args[1]:
                    case '+':
                        # unknown + value = target => unknown = target - value
                        return lambda t: value1(t - value2)
                    case '-':
                        # unknown - value = target => unknown = target + value
                        return lambda t: value1(t + value2)
                    case '*':
                        # unknown * value = target => unknown = target / value
                        return lambda t: value1(t // value2)
                    case '/':
                        # unknown / value = target => unknown = target * value
                        return lambda t: value1(t * value2)
                    case _:
                        raise Exception(value1, args[1], value2)
            case _:
                raise Exception(value1, value2)

left = eval_monkey(monkeys['root'][0], monkeys)
right = eval_monkey(monkeys['root'][2], monkeys)

target, fn = (left, right) if type(left) is int else (right, left)

print(fn(target))
