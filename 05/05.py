#!/usr/bin/env python3

import sys

append_step = -1 if sys.argv[2] == '1' else 1

with open(sys.argv[1]) as f:
    start_t, moves_t = f.read().rstrip().split('\n\n')

config = [[]] * 9
for l in start_t.split('\n'):
    for i in range((len(l) + 1) // 4):
        t = l[4*i:4*i+3]
        if t[0] == '[':
            config[i] = [t[1]] + config[i]

for l in moves_t.split('\n'):
    _, n, _, src, _, dest = l.split()
    n = int(n)
    src = int(src) - 1
    dest = int(dest) - 1

    config[dest] = config[dest] + config[src][-n:][::append_step]
    config[src] = config[src][:-n]

print(''.join([stack[-1] for stack in config]))
