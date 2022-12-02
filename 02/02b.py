#!/usr/bin/env python3

import sys

import numpy as np

def result(a, b):
    return ((1 + (b - a) % 3) * 3) % 9

def scores(line):
    a, b = line.split(' ')
    a = ord(a) - 65
    b = ord(b) - 88
    score = 1 + b + result(a, b)
    b2 = (a + b + 2) % 3
    score2 = 1 + b2 + result(a, b2)
    return score, score2

with open(sys.argv[1]) as f:
    print(np.sum([scores(l.strip()) for l in f], axis=0))
