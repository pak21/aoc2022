#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    elves = f.read().strip().split('\n\n')
    calories = sorted(map(
        lambda elf: sum(map(
            lambda snack: int(snack),
            elf.split('\n')
        )),
        elves
    ))
    print(calories[-1])
    print(sum(calories[-3:]))
