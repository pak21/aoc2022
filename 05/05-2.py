#!/usr/bin/env python3

import collections
import sys

with open(sys.argv[1]) as f:
    t = f.read().rstrip()
    start_t, moves_t = t.split('\n\n')

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

        config[dest] = config[dest] + config[src][-n:]
        config[src] = config[src][:-n]

    print(''.join([stack[-1] for stack in config]))
