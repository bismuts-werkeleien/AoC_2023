import sys

directions = {
        'L': (0,-1),
        'U': (-1, 0),
        'R': (0,1),
        'D': (1,0),
        }

with open(sys.argv[1], "r") as file:
    lines = [line.split() for line in file.read().splitlines()]
    corrected = []
    for line in lines:
        code = line[2][2:-1]
        match code[-1]:
            case "0":
                direction = 'R'
            case "1":
                direction = 'D'
            case "2":
                direction = 'L'
            case "3":
                direction = 'U'
        corr_len = int(code[:5], base=16)
        corrected.append([direction, corr_len])

def build_trench(lines):
    curr_idx = (0,0)
    hull = 0
    sum1 = 0
    sum2 = 0
    for line in lines:
        start = curr_idx
        direction = directions[line[0]]
        curr_idx = tuple(map(sum, zip(curr_idx, (int(line[1])*d for d in direction))))
        sum1 = sum1 + (start[0]) * (curr_idx[1])
        sum2 = sum2 + (start[1]) * (curr_idx[0])
        hull += int(line[1])
    
    # calc inner area with shoelace formula for clculating areas of polygons
    area = abs(sum1 - sum2) // 2
    # print(area, hull)
    # add in the hull as well according to Pick's theorem
    return area + hull // 2 + 1

print(f"The trench can hold {build_trench(lines)} cubic meters of lava\n")

# --------------- part 2
print(f"The lagoon can hold {build_trench(corrected)} cubic meters of lava\n")

