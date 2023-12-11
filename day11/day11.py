import sys
import math
from collections import deque
import numpy as np


with open(sys.argv[1], "r") as file:
    lines = [list(line) for line in file.read().split("\n")[:-1]]
    image = np.array(lines, str)

    rows = np.all(image == '.', axis = 1)
    row_idx = np.where(rows == True)[0]
    
    cols = np.all(image == '.', axis = 0)
    col_idx = np.where(cols == True)[0]

    indices = np.where(image == '#')


def build_galaxy(indices, expander):
    galaxies = dict()
    for i in range(len(indices[0])):
        y = indices[0][i]
        x = indices[1][i]
        inserted_rows = (row_idx < y).sum()*expander
        inserted_cols = (col_idx < x).sum()*expander
        galaxies[(y+inserted_rows, x+inserted_cols)] = i+1
    return galaxies


def calc_dists(galaxies):
    dists = []
    seen = set()
    queue = deque()
    for point in galaxies.keys():
        for point2 in galaxies.keys():
            if (point, point2) not in seen and (point2, point) not in seen:
                queue.append((point, point2))
        while queue:
            pair = queue.popleft()
            seen.add(pair)
            dy = abs(pair[0][0] - pair[1][0])
            dx = abs(pair[0][1] - pair[1][1])
            dist = dy + dx
            dists.append(dist)
    return dists


galaxies = build_galaxy(indices, 1)
dists = calc_dists(galaxies)
print(f"The sum of shortest path between galaxies is {sum(dists)}\n ")
# --------------- part 2
exp_galaxies = build_galaxy(indices, 1000000-1)
exp_dists = calc_dists(exp_galaxies)
print(f"The sum of shortest path between largely expanded galaxies is {sum(exp_dists)}\n ")

