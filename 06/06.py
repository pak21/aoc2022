#!/usr/bin/env python3

import sys

n = int(sys.argv[2])

with open(sys.argv[1]) as f:
    for l in f:
        for i in range(len(l)):
            x = set(l[i:i+n])
            if len(x) == n:
                print(i+n)
                break
