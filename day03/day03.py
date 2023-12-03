import sys, re

with open(sys.argv[1], "r") as file:
    inputs = [line for line in file.read().splitlines()]

parts_map = dict()
gear_map = dict()

def get_adjacents(x, y):
    adjacents = set()
    x_list = [i+x for i in [-1, 0, 1]]
    y_list = [j+y for j in [-1, 0, 1]]
    for coord in parts_map.keys():
        if coord[0] in y_list and (coord[1] in x_list or coord[2] in x_list):
            adjacents.add(parts_map[coord])
    return adjacents

def build_parts(x, y):
    part = ''
    x_coords = []
    for i, sym in enumerate(inputs[y][x:]):
        if not sym.isdigit():
            break
        else:
            part += sym
            x_coords.append(i)
    number = int(part)
    parts_map[(y, x_coords[0]+x, x_coords[-1]+x)] = number
    return

def x_in_parts(x, y):
    for coord in parts_map.keys():
        if y== coord[0] and x >= coord[1] and x <= coord[2]:
            return True
    return False

machine_parts = []
gear_parts = []
for y, line in enumerate(inputs):
    for x, sym in enumerate(inputs[y]):
        if sym.isdigit() and not x_in_parts(x, y):
            build_parts(x, y)

for y, line in enumerate(inputs):
    for x, sym in enumerate(inputs[y]):
        if sym not in ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            adj = get_adjacents(x, y)
            machine_parts.append(sum(adj))
        if sym == "*":
            adj = list(get_adjacents(x, y))
            if len(adj) == 2:
                gear_parts.append(adj[0]*adj[1])


print(f"Found machine parts: {machine_parts}, \nyielding a sum of {sum(machine_parts)}\n")
print(f"Found gear parts: {gear_parts}, \nyielding a sum of {sum(gear_parts)}\n")

