#!/usr/bin/env python3

import builtins
import functools
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

extra_a = [[2]]
extra_b = [[6]]
with open(sys.argv[1]) as f:
    items = [eval(l) for l in f if l != '\n'] + [extra_a, extra_b]

s = sorted(items, key=functools.cmp_to_key(compare_lists))
print( (s.index(extra_a) + 1) * (s.index(extra_b) + 1) )
