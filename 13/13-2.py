#!/usr/bin/env python3

import builtins
import functools
import sys

import numpy as np

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

import functools

with open(sys.argv[1]) as f:
    extra_a = [[2]]
    extra_b = [[6]]
    items = [parse(l.rstrip()) for l in f if l != '\n']
    items = items + [extra_a, extra_b]
    s = sorted(items, key=functools.cmp_to_key(compare_lists))
    print( (s.index(extra_a) + 1) * (s.index(extra_b) + 1) )
