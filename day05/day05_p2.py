import sys, re
from collections import deque

sts_map = [] 
stf_map = [] 
ftw_map = [] 
wtl_map = [] 
ltt_map = [] 
tth_map = [] 
htl_map = [] 

def fill_map(some_map, lines):
    for line in lines:
        some_map.append([(line[1], line[1] + line[2]), line[0]])

def get_contained(some_map, source):
    dest = set()
    queue = deque()
    for s in source:
        queue.append(s)
    while queue:
        s = queue.pop()
        fc = False
        for sr, d in some_map:
            if s[0] >= sr[0] and s[-1] <= sr[-1]:
                offset = s[0] - sr[0]
                len_s = s[-1] - s[0]
                dest.add((d + offset, d + offset + len_s))
                fc = True
                break
            elif s[0] >= sr[0] and s[0] < sr[-1] and s[-1] > sr[-1]:
                # overlap only right, build two ranges
                range1 = (s[0], sr[-1])
                range2 = (sr[-1], s[-1])
                queue.append(range1)
                queue.append(range2)
                continue
            elif s[0] < sr[0] and s[-1] > sr[0] and s[-1] < sr[-1]:
                # overlap only left, build two ranges
                range1 = (s[0], sr[0])
                range2 = (sr[0], s[-1])
                queue.append(range1)
                queue.append(range2)
                continue
        #no mapping found
        if not fc:
            dest.add(s)
    return list(dest)

def calc_next(some_map, source):
    return get_contained(some_map, source)

def build_seeds(seeds):
    ranges = []
    for i in range(0,len(seeds),2):
        r = seeds[i+1]
        ranges.append((seeds[i],seeds[i]+r))
    return ranges

with open(sys.argv[1], "r") as file:
    blocks = file.read().split("\n\n")
    seeds = [int(x) for x in blocks[0][6:].split()]
    seeds_range = build_seeds(seeds)
    print(seeds_range)
    for idx, block in enumerate(blocks[1:]):
        instr = block.split("\n")
        lines = [list(map(int, l.split())) for l in instr[1:]]
        if idx == 0:
            #seed-to-soil
            fill_map(sts_map, lines)
        if idx == 1:
            #soil-to-fertilizer
            fill_map(stf_map, lines)
        if idx == 2:
            #fertilizer-to-water
            fill_map(ftw_map, lines)
        if idx == 3:
            #water-to-light
            fill_map(wtl_map, lines)
        if idx == 4:
            #light-to-temperature
            fill_map(ltt_map, lines)
        if idx == 5:
            #temperature-to-humidity
            fill_map(tth_map, lines)
        if idx == 6:
            #humidity-to-locatio
            fill_map(htl_map, lines[:-1])

dests_p2 = []
for i in range(7):
    print(i)
    if i == 0:
        #dests = calc_next(sts_map, seeds)
        dests_p2 = calc_next(sts_map, seeds_range)

    if i == 1:
        #dests = calc_next(stf_map, dests)
        dests_p2 = calc_next(stf_map, dests_p2)

    if i == 2:
        #dests = calc_next(ftw_map, dests)
        dests_p2 = calc_next(ftw_map, dests_p2)

    if i == 3:
        #dests = calc_next(wtl_map, dests)
        dests_p2 = calc_next(wtl_map, dests_p2)
    if i == 4:
        #dests = calc_next(ltt_map, dests)
        dests_p2 = calc_next(ltt_map, dests_p2)
    if i == 5:
        #dests = calc_next(tth_map, dests)
        dests_p2 = calc_next(tth_map, dests_p2)
    if i == 6:
        #dests = calc_next(htl_map, dests)
        dests_p2 = calc_next(htl_map, dests_p2)

loc_min = dests_p2[0][0]
# zero is not valid
for p in dests_p2:
    if p[0] < loc_min and p[0] > 0:
        loc_min=p[0]

print(f"Lowest Location number with seed ranges: {loc_min}\n")

