import sys
import math

with open(sys.argv[1], "r") as file:
    lines = [list(line) for line in file.read().splitlines()]
    rows = len(lines)
    cols = len(lines[0])
    #print(rows, cols) # square grid
    start = (-1, -1)
    gardens = set()

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '#':
                continue
            elif c == 'S':
                start = (i,j)
            gardens.add((i,j))


def get_neighs(plot):
    neighs = set()
    for d in [(0,-1), (0,1), (-1,0), (1,0)]:
        pos = tuple(map(sum, zip(d, plot)))
        if (pos[0]%rows, pos[1]%cols) in gardens:
            neighs.add(pos)
    return neighs

def calc_polynom(p1, p2, p3, n):
    # 3778 33833 93864 183871
    #   30055 60031 90007
    #      29976 29976
    # -> 2a == 2nd difference == 29976 == const
    # -> 3a + b == 1st difference between coeffs[1] and coeffs[0]
    # -> a + b + c == coeffs[0] (n == 1)
    # -> calc coeffs[n-1] for n == steps through solving a*n^2 + b*n + c
    # -> equal to solving (a+b+c)+(n-1)b+(n-1)n*a
    # -> equal to solving (a+b+c)+(n-1)b+(n-1)n*2a/2
    # -> equal to solving coeffs[0]+(n-1)b+(n-1)n*2a/2
    d1 = p2 - p1 # == 1st diff between coeffs[1] and coeffs[0] == 3a+b
    d2 = p3 - p2 - d1 # == 2a
    a = d2 // 2
    b = d1 - 3*a
    return p1 + b*(n-1) + n*(n-1)*a

p1 = 64

steps = 26501365
curr_plots = set()
curr_plots.add(start)
coeffs = []
covered = 0

for step in range(1, 1000):
    next_plots = set()
    for plot in curr_plots:
        neighs = get_neighs(plot)
        next_plots.update(neighs)
    curr_plots = next_plots
    if step == p1:
        print(f"The elf can reach {len(curr_plots)} garden plots with his {steps} steps\n")

    if step%rows == steps%rows:
        coeffs.append(len(curr_plots))

    if len(coeffs) == 3:
        # coeff sequence is quadratic sequence
        # n has to be converted from single steps to "mod rows space"
        covered = calc_polynom(*coeffs, math.ceil(steps/rows))
        break

# --------------- part 2
print(f"The elf can reach {covered} garden plots with his {steps} steps\n")

