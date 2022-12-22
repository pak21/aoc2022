#!/usr/bin/env python3

import sys

DIRS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]

test_geometry = sys.argv[1] == 'test.txt'

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

def wrap(grid, y, x, direction, test_geometry):
    if test_geometry:
        match direction:
            case 0:
                if x == 11 and y >= 4 and y <= 7:
                    return [8, 19-y], 1

            case 1:
                if y == 11 and x >= 8 and x <= 11:
                    return [7, 11-x], 3

            case 2:
                pass

            case 3:
                if y == 4 and x >= 4 and x <= 7:
                    return [x-4, 8], 0
    else:
        match direction:
            case 0:
                if x == 49 and y >= 150 and y <= 199:
                    return [149, y-100], 3

                if x == 99 and y >= 50 and y <= 99:
                    return [49, y+50], 3

                if x == 99 and y >= 100 and y <= 149:
                    return [149-y, 149], 2

                if x == 149 and y >= 0 and y <= 49:
                    return [149-y, 99], 2

            case 1:
                if y == 49 and x >= 100 and x <= 149:
                    return [x-50, 99], 2

                if y == 149 and x >= 50 and x <= 99:
                    return [x+100, 49], 2

                if y == 199 and x >= 0 and x <= 49:
                    return [0, 100+x], 1 

            case 2:
                if x == 0 and y >= 100 and y <= 149:
                    return [149-y, 50], 0

                if x == 0 and y >= 150 and y <= 199:
                    return [0, y-100], 1
                
                if x == 50 and y >= 0 and y <= 49:
                    return [149-y, 0], 0

                if x == 50 and y >= 50 and y <= 99:
                    return [100, y-50], 1

            case 3:
                if y == 0 and x >= 50 and x <= 99:
                    return [x+100, 0], 0

                if y == 0 and x >= 100 and x <= 149:
                    return [199, x-100], 3

                if y == 100 and x >= 0 and x <= 49:
                    return [x+50, 50], 0
                    
        raise Exception(f'{test_geometry} {loc} {direction}')

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
                next_direction = direction

                if next_tile == ' ':
                    (y, x), next_direction = wrap(grid, loc[0], loc[1], direction, test_geometry)
                    next_tile = grid[y][x]

                match next_tile:
                    case '.':
                        loc = (y, x)
                        direction = next_direction
                    case '#':
                        break
                    case _:
                        raise Exception(f'Invalid tile: "{next_tile}"')

print(1000 * (loc[0] + 1) + 4 * (loc[1] + 1) + direction)
