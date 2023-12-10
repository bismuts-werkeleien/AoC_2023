import sys
from collections import deque


with open(sys.argv[1], "r") as file:
    fences = [list(line) for line in file.read().split("\n")[:-1]]

pipes_map = {
        "|": [(1, 0), (-1, 0)],
        "-": [(0, 1), (0, -1)],
        "7": [(1, 0), (0, -1)],
        "L": [(-1, 0), (0, 1)],
        "J": [(-1, 0), (0, -1)],
        "F": [(1, 0), (0, 1)]
        }

def get_neighbors(c, i, j):
    # we're 'lucky' with the borders, no padding needed
    n1, n2 = pipes_map[c]
    (d1y, d1x) = (n1[0]+i, n1[1]+j)
    (d2y, d2x) = (n2[0]+i, n2[1]+j)
    neighs = [(fences[d1y][d1x], d1y, d1x), (fences[d2y][d2x], d2y, d2x)]
    return neighs

def ignore_not_seen(fences, seen):
    for i in range(len(fences)):
        for j in range(len(fences[0])):
            if (fences[i][j], i, j) not in seen:
                fences[i][j] = '.'

def calc_between_area(fences):
    area = 0
    # enclosed in pipes per line
    for line in fences:
        pipes = 0
        stack = []
        for c in line:
            if c in ['F', 'L', 'J', '7']:
                last = c
                if len(stack) > 0:
                    last = stack.pop()
                else:
                    stack.append(c)
                    continue
                if last == 'F' and c == 'J' or last == 'L' and c == '7':
                    c = '|'
                elif last == 'F' and c == '7' or last == 'L' and c == 'J':
                    #"U" shaped can be ignored
                    c = ''
                else:
                    stack.append(c)
            if c == '|':
                pipes += 1
            elif pipes % 2 == 1 and c == '.':
                area +=1
    return area

queue = deque()
seen = set()
lengths = []
# find start and queue elements
for i, line in enumerate(fences):
    if 'S' in line:
        j = line.index('S')
        sub = '|' #substitute for S; only for this specific input
        fences[i][j] = sub
        queue.append((sub, 0, i, j))
        seen.add((sub, i, j))
        lengths.append(0)
        break
        
# find loop
while len(queue) > 0:
    curr = queue.pop()
    lengths.append(curr[1])
    neighs = get_neighbors(curr[0], curr[2], curr[3])
    for n in neighs:
        if n not in seen:
            queue.appendleft((n[0], curr[1] + 1, n[1], n[2]))
            seen.add(n)

print(f"The number of steps is {max(lengths)}\n ")
# --------------- part 2
ignore_not_seen(fences, seen)
area = calc_between_area(fences)
print(f"The inner area is {area}\n ")

