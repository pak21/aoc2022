#!/usr/bin/env python3

import functools
import sys

def parse_monkey(m):
    _, items_text, operation_text, monkey_mod_text, true_text, false_text = m.split('\n')
    items = [int(i.replace(',', '')) for i in items_text.lstrip().split(' ')[2:]]

    operator, value = operation_text.lstrip().split(' ')[4:]
    operation_fn = (lambda a, b: a * b) if operator == '*' else (lambda a, b: a + b)
    match value:
        case 'old':
            monkey_fn = lambda a: operation_fn(a, a)
        case _:
            v = int(value)
            monkey_fn = lambda a: operation_fn(a, v)

    monkey_mod = int(monkey_mod_text.lstrip().split(' ')[3])
    true_target = int(true_text.lstrip().split(' ')[5])
    false_target = int(false_text.lstrip().split(' ')[5])
    target_fn = lambda worry: false_target if worry % monkey_mod else true_target

    return [items, monkey_fn, monkey_mod, target_fn, 0]

def do_round(monkeys, worry_reduce, modulo):
    for m in monkeys:
        items, monkey_fn, _, target_fn, _ = m
        for worry in items:
            new_worry = (monkey_fn(worry) // worry_reduce) % modulo
            monkeys[target_fn(new_worry)][0].append(new_worry)
        m[-1] += len(items)
        m[0] = []

with open(sys.argv[1]) as f:
    monkeys = [parse_monkey(l) for l in f.read().rstrip().split('\n\n')]

modulo = functools.reduce(lambda a, b: a * b, [m[2] for m in monkeys])

worry_reduce = int(sys.argv[3])

for _ in range(int(sys.argv[2])):
    do_round(monkeys, worry_reduce, modulo)

throws = sorted([m[-1] for m in monkeys])
print(throws[-2] * throws[-1])
