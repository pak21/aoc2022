#!/usr/bin/env python3

import sys

def letterscore(c):
    return ord(c) - 38 if c.isupper() else ord(c) - 96

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    print(sum([
        letterscore(list(set(lines[i]).intersection(lines[i + 1]).intersection(lines[i + 2]))[0])
        for i
        in range(0, len(lines), 3)
    ]))
