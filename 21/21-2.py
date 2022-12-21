#!/usr/bin/env python3

import builtins
import collections
import sys

import numpy as np

class ValueNode():
    def __init__(self, v):
        self.v = v

class AddNode():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

class MinusNode():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

class TimesNode():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

class DivideNode():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

class PlaceholderNode():
    pass

monkeys = {}
with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        args = l.split()
        monkeys[args[0][:-1]] = args[1:]

def eval_monkey(monkey, monkeys):
    args = monkeys[monkey]
    if monkey == 'humn':
        return PlaceholderNode()

    if len(args) == 1:
        return float(args[0])
    else:
        value1 = eval_monkey(args[0], monkeys)
        value2 = eval_monkey(args[2], monkeys)
        if type(value1) == builtins.float and type(value2) == builtins.float:
            match args[1]:
                case '+':
                    return value1 + value2
                case '-':
                    return value1 - value2
                case '*':
                    return value1 * value2
                case '/':
                    return value1 / value2
                case _:
                    raise Exception(args[1])
        else:
            match args[1]:
                case '+':
                    return AddNode(value1, value2)
                case '-':
                    return MinusNode(value1, value2)
                case '*':
                    return TimesNode(value1, value2)
                case '/':
                    return DivideNode(value1, value2)
                case _:
                    raise Exception(args[1])

left = eval_monkey(monkeys['root'][0], monkeys)
right = eval_monkey(monkeys['root'][2], monkeys)

tree, target = (left, right) if type(right) == builtins.float else (right, left)

def reverse_tree(tree, target):
    if type(tree) is AddNode:
        match (type(tree.v1), type(tree.v2)):
            case (_, builtins.float):
                # unknown + number = target
                # unknown = target - number
                return reverse_tree(tree.v1, target - tree.v2)
            case (builtins.float, _):
                # number + unknown = target
                # unknown = target - number
                return reverse_tree(tree.v2, target - tree.v1)
            case _:
                raise Exception(tree, tree.v1, tree.v2, target)
    elif type(tree) is MinusNode:
        match (type(tree.v1), type(tree.v2)):
            case (builtins.float, _):
                # number - unknown = target
                # number = target + unknown
                # unknown = number - target
                return reverse_tree(tree.v2, tree.v1 - target)
            case (_, builtins.float):
                # unknown - number = target
                # unknown = target + number
                return reverse_tree(tree.v1, target + tree.v2)
            case _:
                raise Exception(tree, tree.v1, tree.v2, target)
    elif type(tree) is TimesNode:
        match (type(tree.v1), type(tree.v2)):
            case (builtins.float, _):
                # number * unknown = target
                # unknown = target / number
                return reverse_tree(tree.v2, target / tree.v1)
            case (_, builtins.float):
                # unknown * number = target
                # unknown = target / number
                return reverse_tree(tree.v1, target / tree.v2)
            case _:
                raise Exception(tree, tree.v1, tree.v2, target)
    elif type(tree) is DivideNode:
        match (type(tree.v1), type(tree.v2)):
            case (_, builtins.float):
                # unknown / number = target
                # unknown = target * number
                return reverse_tree(tree.v1, target * tree.v2)
            case (builtins.float, _):
                # number / unknown = target
                # number = target * unknown
                # unknown = number / target
                return reverse_tree(tree.v2, tree.v1 / target)
            case _:
                raise Exception(tree, tree.v1, tree.v2, target)
    elif type(tree) is PlaceholderNode:
        return int(target)
    else:
        raise Exception(tree)

print(reverse_tree(tree, target))
