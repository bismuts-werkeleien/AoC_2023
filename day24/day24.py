import sys
import numpy as np
from z3 import BitVec, Solver


with open(sys.argv[1], "r") as file:
    lines = file.read().splitlines()
    positions2d, positions3d = [], []
    velocities2d, velocities3d = [], []
    for line in lines:
        pos, vel = [tuple(map(int, l.split(','))) for l in line.split('@')]
        positions2d.append(np.array(pos[:-1]).T)
        velocities2d.append(np.array(vel[:-1]).T)

        positions3d.append(np.array(pos).T)
        velocities3d.append(np.array(vel).T)

#min_r, max_r = np.array((7, 7)).T, np.array((27, 27)).T
min_r, max_r = np.array((200000000000000, 200000000000000)).T, np.array((400000000000000, 400000000000000)).T

def intersect_p1(positions, velocities):
    intersections = []
    for i, a in enumerate(zip(positions[:-1], velocities[:-1])):
        for j, b in enumerate(zip(positions[i+1:], velocities[i+1:])):
            c1, v1 = a
            c2, v2 = b
            if np.all(c2 == c1) and np.all(v1 == v2):
                continue
            x, residuals, rank = np.linalg.lstsq(np.array([v1, -v2]).T, c2-c1, rcond=None)[:3]
            if rank == 2 and np.all(x >= 0):
                intersections.append((v1 * x[0] + c1))
            #elif rank == 2: past intersection
            #else: no intersection
    return intersections


intersections = intersect_p1(positions2d, velocities2d)
num_i = 0
for i in intersections:
    if np.all(min_r < i) and np.all(i < max_r):
        num_i +=1

print(f"In 2D, {num_i} intersections occur within the test area\n")
# --------------- part 2
# use Z3 solver for this: https://z3prover.github.io/api/html/z3.html
def find_rock(positions, velocities):
    Ibv = lambda name: BitVec(name, 64)
    s = Solver()
    x, y, z = Ibv("x"), Ibv("y"), Ibv("z")
    vx, vy, vz = Ibv("vx"), Ibv("vy"), Ibv("vz")

    for i, a in enumerate(zip(positions, velocities)):
        c, v = a
        t = Ibv(f't_{i}')
        s.add(t >= 0)
        s.add(x + vx * t == c[0] + v[0] * t)
        s.add(y + vy * t == c[1] + v[1] * t)
        s.add(z + vz * t == c[2] + v[2] * t)

    assert str(s.check()) == 'sat'

    m = s.model()
    return m.eval(x + y + z)

rock_pos = find_rock(positions3d, velocities3d)
print(f"The sum of the hailstone-destroying rock's position is {rock_pos}\n")
