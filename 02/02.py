#!/usr/bin/env python3

import sys

import numpy as np

SCORES = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

RESULT = {
    ('A', 'X'): 3,
    ('A', 'Y'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('B', 'Y'): 3,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
    ('C', 'Y'): 0,
    ('C', 'Z'): 3,
}

TRANSFORM = {
    ('A', 'X'): 'Z',
    ('A', 'Y'): 'X',
    ('A', 'Z'): 'Y',
    ('B', 'X'): 'X',
    ('B', 'Y'): 'Y',
    ('B', 'Z'): 'Z',
    ('C', 'X'): 'Y',
    ('C', 'Y'): 'Z',
    ('C', 'Z'): 'X',
}

def scores(line):
    opp, me = line.split(' ')
    score = SCORES[me] + RESULT[(opp, me)]
    me2 = TRANSFORM[(opp, me)]
    score2 = SCORES[me2] + RESULT[(opp, me2)]
    return score, score2

with open(sys.argv[1]) as f:
    print(np.sum([scores(l.strip()) for l in f], axis=0))
