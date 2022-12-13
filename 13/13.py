#!/usr/bin/env python3

import builtins
import sys

def parse(s):
    return eval(s)

def sign(l, r):
    return -1 if l < r else (0 if l == r else 1)

def compare_items(l, r):
    match (type(l), type(r)):
        case (builtins.int, builtins.int):
            return sign(l, r)
        case (builtins.list, builtins.list):
            return compare_lists(l, r)
        case (builtins.int, builtins.list):
            return compare_lists([l], r)
        case (builtins.list, builtins.int):
            return compare_lists(l, [r])

def compare_lists(l, r):
    for item_l, item_r in zip(l, r):
        c = compare_items(item_l, item_r)
        if c:
            return c

    return sign(len(l), len(r))

with open(sys.argv[1]) as f:
    pairs = f.read().rstrip().split('\n\n')
    part1 = 0
    for i, pair in enumerate(pairs, 1):
        lines = pair.split('\n')
        left = parse(lines[0])
        right = parse(lines[1])
        if compare_lists(left, right) == -1:
            part1 += i
    print(part1)
