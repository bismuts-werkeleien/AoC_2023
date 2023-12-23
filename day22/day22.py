import sys

bricks = []
with open(sys.argv[1], "r") as file:
    lines = file.read().splitlines()
    for line in lines:
        b_s, b_e = [tuple(map(int, l.split(','))) for l in line.split('~')]
        bricks.append([b_s, b_e])


def land_brick(tallest, brick):
    x_range = range(brick[0][0], brick[1][0] + 1)
    y_range = range(brick[0][1], brick[1][1] + 1)
    peak = max(tallest[(x, y)] for x in x_range for y in y_range)
    z_diff = max(brick[0][2] - peak - 1, 0)
    new_s = (brick[0][0], brick[0][1], brick[0][2] - z_diff)
    new_e = (brick[1][0], brick[1][1], brick[1][2] - z_diff)
    return [new_s, new_e]

def sim_fall(bricks):
    tallest = defaultdict(int)
    fallen_bricks = []
    falls = 0
    for brick in bricks:
        new_brick = land_brick(tallest, brick)
        if new_brick[0][2] != brick[0][2]:
            falls += 1
        fallen_bricks.append(new_brick)
        for x in range(brick[0][0], brick[1][0] + 1):
            for y in range(brick[0][1], brick[1][1] + 1):
                tallest[(x, y)] = new_brick[1][2] # assign z end
    return falls, fallen_bricks

def solve(bricks):
    bricks.sort(key=lambda brick: brick[0][2])
    _, fallen_bricks = sim_fall(bricks)
    p1 = p2 = 0
    for i in range(len(fallen_bricks)):
        removed = fallen_bricks[:i] + fallen_bricks[i + 1:]
        falls, _ = sim_fall(removed)
        if not falls:
            p1 += 1
        else:
            p2 += falls
    return p1, p2


disintegrators, cascade = solve(bricks)

print(f"{disintegrators} rocks could be disintegrated\n")
# --------------- part 2
print(f"{cascade} cascading rocks would fall\n")
