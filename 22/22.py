#!/usr/bin/env python3

import collections
import sys

import numpy as np

DIRS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]

with open(sys.argv[1]) as f:
    grid_text, moves_text = f.read().rstrip().split('\n\n')

grid = [[c for c in l] for l in grid_text.split('\n')]

moves = []
n = 0
for c in moves_text:
    if c >= '0' and c <= '9':
        n = 10 * n + ord(c) - ord('0')
    else:
        moves.append(n)
        moves.append(c)
        n = 0
moves.append(n)

start_x = grid[0].index('.')

loc = (0, start_x)
direction = 0

def wrap_right(grid, y):
    x = 0
    while grid[y][x] == ' ':
        x += 1
    return x

def wrap_left(grid, y):
    x = len(grid[y]) - 1
    while grid[y][x] == ' ':
        x -= 1
    return x

def wrap_down(grid, x):
    y = 0
    while grid[y][x] == ' ':
        y += 1
    return y

def wrap_up(grid, x):
    y = len(grid) - 1
    while x >= len(grid[y]) or grid[y][x] == ' ':
        y -= 1
    return y

def get_next_tile(grid, y, x):
    if y < 0 or y >= len(grid):
        return ' '

    if x < 0 or x >= len(grid[y]):
        return ' '

    return grid[y][x]

for move in moves:
    match move:
        case 'L':
            direction = (direction - 1) % 4
        case 'R':
            direction = (direction + 1) % 4
        case _:
            for _ in range(move):
                step = DIRS[direction]
                next_loc = [loc[0] + step[0], loc[1] + step[1]]
                next_tile = get_next_tile(grid, next_loc[0], next_loc[1])

                if next_tile == ' ':
                    match direction:
                        case 0:
                            next_loc[1] = wrap_right(grid, next_loc[0])
                        case 1:
                            next_loc[0] = wrap_down(grid, next_loc[1])
                        case 2:
                            next_loc[1] = wrap_left(grid, next_loc[0])
                        case 3:
                            next_loc[0] = wrap_up(grid, next_loc[1])
                        case _:
                            raise Exception('nope')

                    next_tile = grid[next_loc[0]][next_loc[1]]

                match next_tile:
                    case '.':
                        loc = next_loc
                    case '#':
                        break
                    case _:
                        raise Exception(f'Invalid tile: "{next_tile}"')

row = loc[0] + 1
column = loc[1] + 1

password = 1000 * row + 4 * column + direction
print(password)
