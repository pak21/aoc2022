#!/usr/bin/env python3

import builtins
import sys

def compare_items(l, r):
    match (type(l), type(r)):
        case (builtins.int, builtins.int):
            return l - r
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

    return len(l) - len(r)

with open(sys.argv[1]) as f:
    pairs = [[eval(x) for x in pair.split('\n')] for pair in f.read().rstrip().split('\n\n')]

print(sum([i for i, (l, r) in enumerate(pairs, 1) if compare_lists(l, r) < 0]))
