import sys
import copy
from collections import deque

directions = {
        '>': (0,1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1,0)
        }

forward_d = {
        '>': '^',
        'v': '<',
        '<': 'v',
        '^': '>'
        }

backward_d = {
        '>': 'v',
        'v': '>',
        '<': '^',
        '^': '<'
        }

with open(sys.argv[1], "r") as file:
    lines = [list(line) for line in file.read().splitlines()]

def energize(start_pos, start_d):
    beam = set()
    beam_next = deque()
    beam_next.append((start_pos, start_d))
    while beam_next:
        pos, d = beam_next.popleft()
        tile = lines[pos[0]][pos[1]]
        if tile == '-' and (d == '^' or d == 'v'):
            d = '<'
            if not (pos, d) in beam:
                pos1 = tuple(map(sum, zip(pos, directions[d])))
                if not -1 in pos1:
                    beam_next.append((pos1, d))
            d = '>'
        elif tile == '|' and (d == '>' or d == '<'):
            d = '^'
            if not (pos, d) in beam:
                pos1 = tuple(map(sum, zip(pos, directions[d])))
                if not -1 in pos1:
                    beam_next.append((pos1, d))
            d = 'v'
        elif tile == '/':
            d = forward_d[d]
        elif tile == '\\':
            d = backward_d[d]
        
        if not (pos, d) in beam:
            beam.add((pos, d))
            pos = tuple(map(sum, zip(pos, directions[d])))
            if not -1 in pos and not (d == '>' and len(lines[0]) in pos) and not (d == 'v' and len(lines) in pos):
                beam_next.append((pos, d))
    
    energized = set(list(zip(*beam))[0])
    return len(energized)


print(f"The number of energized tiles in (0,0) configuration is {energize((0,0), '>')}\n")

# --------------- part 2

energies = []
energies.extend([energize((0, y), 'v') for y in range(len(lines[0]))])
energies.extend([energize((len(lines)-1, y), '^') for y in range(len(lines[0])-1, -1, -1)])
energies.extend([energize((x, 0), '>') for x in range(len(lines))])
energies.extend([energize((x, len(lines[0])-1), '<') for x in range(len(lines)-1, -1, -1)])
print(f"The number of energized tiles in maximum configuration is {max(energies)}\n")

