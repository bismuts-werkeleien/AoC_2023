import sys, re
import copy
import math

max_load = {'red': 12, 'green': 13, 'blue': 14}

min_load = {'red': 0, 'green': 0, 'blue': 0}

with open(sys.argv[1], "r") as file:
    inputs = [line for line in file.read().splitlines()]
    game_inputs = []
    for line in inputs:
        game_inputs.append([item.split(',') for item in re.split(';', line[line.find(':')+1:])])

#print(game_inputs)

impossible_ids = set()
possible_ids = set()
min_cubes = []
for i, g in enumerate(game_inputs):
    possible_ids.add(i+1)
    min_cubes.append(copy.deepcopy(min_load))
    for s in g:
        for draw in s:
            test = draw.lstrip().split(' ')
            if int(test[0]) > min_cubes[i][test[1]]:
                min_cubes[i][test[1]] = int(test[0])
            if max_load[test[1]] < int(test[0]):
                impossible_ids.add(i+1)

possible_ids = possible_ids - impossible_ids

print(f"Possible IDs are: {possible_ids}, \nyielding a sum of {sum(possible_ids)}\n")

min_games = [math.prod(dict.values(c)) for c in min_cubes]
print(f"Power of the minimum sets are {min_games}, \nyielding a sum of {sum(min_games)}")
