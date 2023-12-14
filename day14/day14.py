import sys
import copy

rounded = set()
cubes = set()
with open(sys.argv[1], "r") as file:
    platform = [list(line) for line in file.read().splitlines()]
    for i, line in enumerate(platform):
        for j, c in enumerate(line):
            if c == '#':
                cubes.add((i,j))
            elif c == 'O':
                rounded.add((i,j))

rounded2 = copy.deepcopy(rounded)

def build_platform(rounded):
    for i, line in enumerate(platform):
        for j, c in enumerate(line):
            if (i,j) not in cubes:
                platform[i][j] = 'O' if (i,j) in rounded else '.'
    return platform

def north_load(rounded):
    platform = build_platform(rounded)
    load = 0
    for i in range(len(platform)):
        #print(i, platform[i])
        load += (len(platform)-i)*platform[i].count('O')
    return load


def roll_north(r):
    for idx in range(1, len(platform)):
        for i in range(idx, 0, -1):
            for j in range(len(platform[0])):
                if (i-1,j) not in cubes and (i-1,j) not in r and (i,j) in r:
                    r.add((i-1,j))
                    r.remove((i,j))

def roll_south(r):
    for idx in range(len(platform)-2, -1, -1):
        for i in range(idx, len(platform)-1):
            for j in range(len(platform[0])):
                if (i+1,j) not in cubes and (i+1, j) not in r and (i,j) in r:
                    r.add((i+1,j))
                    r.remove((i,j))

def roll_west(r):
    for idx in range(1, len(platform[0])):
        for j in range(idx, 0, -1):
            for i in range(len(platform)):
                if (i,j-1) not in cubes and (i,j-1) not in r and (i,j) in r:
                    r.add((i,j-1))
                    r.remove((i,j))

def roll_east(r):
    for idx in range(len(platform[0])-2, -1, -1):
        for j in range(idx, len(platform[0])-1):
            for i in range(len(platform)):
                if (i,j+1) not in cubes and (i, j+1) not in r and (i,j) in r:
                    r.add((i,j+1))
                    r.remove((i,j))

roll_north(rounded)

print(f"The total load on the north support beam is {north_load(rounded)}\n")

# --------------- part 2
cycle_load = 0
cycle = 0
seen_rocks = dict()
remaining = 1000000000
while cycle < 1000000000:
    roll_north(rounded2)
    roll_west(rounded2)
    roll_south(rounded2)
    roll_east(rounded2)
    cycle += 1
    frozen_rocks = frozenset(rounded2)
    if frozen_rocks in seen_rocks.keys() and remaining == 1000000000:
        diff = cycle - seen_rocks[frozen_rocks]
        remaining = (1000000000 - cycle) % diff
        cycle = 1000000000 - remaining

    seen_rocks[frozen_rocks] = cycle

print(f"The total load on the north support beam after cycling is {north_load(rounded2)}\n")

