#!/usr/bin/env python3

import sys

n = int(sys.argv[2])

with open(sys.argv[1]) as f:
    for l in f:
        for i in range(len(l)):
            if len(set(l[i:i+n])) == n:
                print(i+n)
                break
