#!/usr/bin/env python3

import functools
import sys

import numpy as np

def parse_monkey(m):
    _, items_text, operation_text, test_text, true_text, false_text = m.split('\n')
    items = [int(i.replace(',', '')) for i in items_text.lstrip().split(' ')[2:]]
    operation = operation_text.lstrip().split(' ')[4:]
    test = int(test_text.lstrip().split(' ')[3])
    true = int(true_text.lstrip().split(' ')[5])
    false = int(false_text.lstrip().split(' ')[5])
    return [items, operation, test, true, false, 0]

def apply(operation, item):
    op, arg = operation
    v = item if arg == 'old' else int(arg)
    return item * v if op == '*' else item + v

def do_round(monkeys, worry_reduce, modulo):
    for m in monkeys:
        for item in m[0]:
            new_worry = (apply(m[1], item) // worry_reduce) % modulo
            target = m[3] if new_worry % m[2] == 0 else m[4]
            monkeys[target][0].append(new_worry)
            m[5] += 1
        m[0] = []

with open(sys.argv[1]) as f:
    monkeys = [parse_monkey(l) for l in f.read().rstrip().split('\n\n')]

    modulo = functools.reduce(
        lambda a, b: a * b,
        [m[2] for m in monkeys]
    )

    worry_reduce = int(sys.argv[3])

    for _ in range(int(sys.argv[2])):
        do_round(monkeys, worry_reduce, modulo)

    throws = sorted([m[5] for m in monkeys])
    print(throws[-2] * throws[-1])
