#!/usr/bin/env python3

import sys

import numpy as np

def process_line(line):
    (start_a, end_a), (start_b, end_b) = [[int(n) for n in elf.split('-')] for elf in line.strip().split(',')]

    part1 = (start_a <= start_b and end_a >= end_b) or (start_b <= start_a and end_b >= end_a)
    part2 = (end_a >= start_b and start_a <= end_b) or (end_b >= start_a and start_b <= end_a)

    return part1, part2

with open(sys.argv[1]) as f:
    print(np.sum([process_line(line) for line in f], axis=0))
