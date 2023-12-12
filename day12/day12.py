import sys, re
from copy import deepcopy

with open(sys.argv[1], "r") as file:
    lines = [line for line in file.read().splitlines()]
    rows = []
    broken = []
    for line in lines:
        l = line.split()
        rows.append(l[0])
        broken.append(list(map(int, l[1].split(','))))


def find_matches(seen, row, pos, match_len, springs, spring_pos, act_row):

    key = (pos, match_len, spring_pos)
    #print(key)
    if key in seen:
        #print("already calculated ", key, seen[key])
        return seen[key]
    ret = 0
    if pos == len(row):
        if spring_pos == len(springs):
            #print(act_row)
            # finished with match if done with all springs at end of row
            ret =  1
    elif row[pos] == '#':
        # take that in and continue with next position to see if we fit the match
        #print("take # and continue")
        ret = find_matches(seen, row, pos + 1, match_len + 1, springs, spring_pos, act_row + '#')
    elif row[pos] == '.' and spring_pos < len(springs):
        if match_len == springs[spring_pos]:
            # match of curr spring is finished, continue with next spring
            #print("found match; continue with next spring")
            ret = find_matches(seen, row, pos + 1, 0, springs, spring_pos + 1, act_row + '.')
        elif match_len == 0:
            # no match, continue with next character
            #print("nothing fitting read; continue with next pos")
            ret = find_matches(seen, row, pos + 1, 0, springs, spring_pos, act_row + '.')
    elif spring_pos == len(springs):
        if match_len == 0:
            #print("already through all springs; continue with next pos and see if all dottable afterwards")
            ret = 1 if '#' not in row[pos+1:] else 0
            #ret = find_matches(seen, row, pos + 1, 0, springs, spring_pos, act_row + row[pos])
            
    elif row[pos] == '?':
        # try to place # by increasing the match length and continuing
        #print("try_hash")
        try_hash = find_matches(seen, row, pos + 1, match_len + 1, springs, spring_pos, act_row + '#')
        try_dot = 0
        if match_len == springs[spring_pos]:
            # match_len already correct, so place a dot and check next spring sequence
            #print("try_dot with next spring")
            try_dot = find_matches(seen, row, pos + 1, 0, springs, spring_pos + 1, act_row + '.')
        elif match_len == 0:
            #print("try_dot")
            try_dot = find_matches(seen, row, pos + 1, 0, springs, spring_pos, act_row + '.')
        ret = try_hash + try_dot
    
    seen[key] = ret
    #print(key, ret)
    return ret
    

arrangements = 0
for i, row in enumerate(rows):
    print(row, broken[i])
    seen = dict()
    arr = find_matches(seen, row + '.', 0, 0, broken[i], 0, '')
    print(arr)
    arrangements += arr

print(f"The sum of spring arrangements {arrangements}\n ")

# --------------- part 2
arrangements = 0
for i, row in enumerate(rows):
    unfolded = "".join([row + '?']*5)
    springs = broken[i]*5
    arr = find_matches({}, unfolded[:-1] + '.', 0, 0, springs, 0, '')
    #print(arr)
    arrangements += arr

print(f"The sum of shortest path between galaxies is {arrangements}\n ")

