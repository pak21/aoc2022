#!/usr/bin/env python3

import sys

def letterscore(c):
    return ord(c) - 38 if c.isupper() else ord(c) - 96

def rowscore(line):
    half = len(line) // 2
    return letterscore(list(set(line[:half]).intersection(line[half:]))[0])

with open(sys.argv[1]) as f:
    print(sum([rowscore(l.strip()) for l in f]))
