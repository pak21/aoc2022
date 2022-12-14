#!/usr/bin/env python3

import sys

import numpy as np

DIRS = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1),
]

def bfs(grid, start, allow_fn, end_fn):
    seen = {start}
    todo = [(start, 0)]
    done = False

    while todo and not done:
        here, moves = todo.pop(0)
        if end_fn(here):
            done = True
            break
        for d in DIRS:
            n = tuple(np.array(here) + d)
            if n in seen or n[0] < 0 or n[0] >= grid.shape[0] or n[1] < 0 or n[1] >= grid.shape[1]:
                continue
            if allow_fn(grid[n], grid[here]):
                todo.append((n, moves + 1))
                seen.add(n)

    if not done:
        raise Exception('No solution found')

    return moves

with open(sys.argv[1]) as f:
    grid = np.array([[ord(c) - 97 for c in l.strip()] for l in f])
    start = np.where(grid == ord('S') - 97)
    end = np.where(grid == ord('E') - 97)
    grid[start] = 0
    grid[end] = 25

    start = tuple([start[0][0], start[1][0]])
    end = tuple([end[0][0], end[1][0]])

    print(bfs(grid, start, lambda a, b: a - b <= 1, lambda a: a == end))
    print(bfs(grid, end, lambda a, b: b - a <= 1, lambda a: grid[a] == 0))
