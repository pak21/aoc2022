#!/usr/bin/env python3

import collections
import sys

with open(sys.argv[1]) as f:
    t = f.read().rstrip()
    start_t, moves_t = t.split('\n\n')

    config = collections.defaultdict(list)
    for l in start_t.split('\n'):
        for i in range(0, len(l), 4):
            t = l[i:i+3]
            if t[0] == '[':
                config[1 + i//4] = [t[1]] + config[1 + i//4]

    moves = []
    for l in moves_t.split('\n'):
        _, n, _, src, _, dest = l.split()
        moves.append((int(n), int(src), int(dest)))

    for n, src, dest in moves:
        config[dest] = config[dest] + config[src][-n:]
        config[src] = config[src][:-n]

    p1 = ''.join([config[1+i][-1] for i in range(len(config))])
    print(p1)
