#!/usr/bin/env python3

import functools
import sys

def parse_monkey(m):
    _, items_text, operation_text, test_text, true_text, false_text = m.split('\n')
    items = [int(i.replace(',', '')) for i in items_text.lstrip().split(' ')[2:]]
    operator, value = operation_text.lstrip().split(' ')[4:]
    operation_lambda = (lambda a, b: a * b) if operator == '*' else (lambda a, b: a + b)
    match value:
        case 'old':
            value_lambda = lambda x: x
        case _:
            v = int(value)
            value_lambda = lambda x: v
    test = int(test_text.lstrip().split(' ')[3])
    true = int(true_text.lstrip().split(' ')[5])
    false = int(false_text.lstrip().split(' ')[5])
    return [items, operation_lambda, value_lambda, test, true, false, 0]

def do_round(monkeys, worry_reduce, modulo):
    for m in monkeys:
        items, operation_lambda, value_lambda, test, true_target, false_target, _ = m
        for item in items:
            new_worry = (operation_lambda(item, value_lambda(item)) // worry_reduce) % modulo
            monkeys[false_target if new_worry % test else true_target][0].append(new_worry)
        m[6] += len(items)
        m[0] = []

with open(sys.argv[1]) as f:
    monkeys = [parse_monkey(l) for l in f.read().rstrip().split('\n\n')]

    modulo = functools.reduce(
        lambda a, b: a * b,
        [m[3] for m in monkeys]
    )

    worry_reduce = int(sys.argv[3])

    for _ in range(int(sys.argv[2])):
        do_round(monkeys, worry_reduce, modulo)

    throws = sorted([m[6] for m in monkeys])
    print(throws[-2] * throws[-1])
