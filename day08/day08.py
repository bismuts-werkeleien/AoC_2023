import sys
import math

nodes = dict()

with open(sys.argv[1], "r") as file:
    block = file.read().split("\n\n")
    instructions = block[0]
    lines = block[1].splitlines()
    for line in lines:
        l = line.split()
        nodes[l[0]] = (l[2][1:-1], l[3][:-1])

def step_through(start, part):
    steps = 0
    elem = start
    while True:
        for instruction in instructions:
            steps += 1
            if instruction == 'L':
                elem = nodes[elem][0]
            else:
                elem = nodes[elem][1]
            if part == 1 and elem == 'ZZZ':
                return steps
            elif part == 2 and elem[-1] == 'Z':
                return steps

steps = step_through("AAA", 1)
print(f"The network needs {steps} steps to navigate\n ")

# --------------- part 2
starts = []
for elem in nodes:
    if elem[-1] == 'A':
        starts.append(elem)

# Finish computing steps when individual Z is reached.
# The simultaneous finish is just a matter of finding the least common multiple
all_steps = [step_through(start, 2) for start in starts]

print(f"The ghost network needs {math.lcm(*all_steps)} steps to navigate\n ")
