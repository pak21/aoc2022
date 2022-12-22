#!/usr/bin/env python3

import sys

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

loc = (0, grid[0].index('.'))
direction = 0

def wrap_horizontal(grid, y, x0, dx):
    x = x0
    while grid[y][x] == ' ':
        x += dx
    return x

def wrap_vertical(grid, x, y0, dy):
    y = y0
    while x >= len(grid[y]) or grid[y][x] == ' ':
        y += dy
    return y

for move in moves:
    match move:
        case 'L':
            direction = (direction - 1) % 4
        case 'R':
            direction = (direction + 1) % 4
        case _:
            for _ in range(move):
                step = DIRS[direction]
                y, x = loc[0] + step[0], loc[1] + step[1]
                next_tile = grid[y][x] if y >= 0 and y < len(grid) and x >= 0 and x < len(grid[y]) else ' '

                if next_tile == ' ':
                    match direction:
                        case 0:
                            x = wrap_horizontal(grid, y, 0, 1)
                        case 1:
                            y = wrap_vertical(grid, x, 0, 1)
                        case 2:
                            x = wrap_horizontal(grid, y, len(grid[y]) - 1, -1)
                        case 3:
                            y = wrap_vertical(grid, x, len(grid) - 1, -1)
                        case _:
                            raise Exception(f'Invalid direction: {direction}')

                    next_tile = grid[y][x]

                match next_tile:
                    case '.':
                        loc = (y, x)
                    case '#':
                        break
                    case _:
                        raise Exception(f'Invalid tile: "{next_tile}"')

print(1000 * (loc[0] + 1) + 4 * (loc[1] + 1) + direction)
