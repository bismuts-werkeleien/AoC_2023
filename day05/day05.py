import sys, re

sts_map = dict()
stf_map = dict()
ftw_map = dict()
wtl_map = dict()
ltt_map = dict()
tth_map = dict()
htl_map = dict()

def fill_map(some_map, lines):
    for line in lines:
        some_map[(line[1], line[2])] = line[0]

def get_contained(some_map, source):
    for ss, sr in some_map.keys():
        if source >= ss and source <= ss+sr:
            dest = some_map[(ss,sr)] + source - ss
            return dest
    return source

def calc_next(some_map, source):
    dests = []
    for s in source:
        dests.append(get_contained(some_map, s))
    print(dests)
    return dests

def build_seeds(seeds):
    ranges = []
    for i in range(0,len(seeds),2):
        r = seeds[i+1]
        ranges.extend(range(seeds[i],seeds[i]+r))
    return ranges

with open(sys.argv[1], "r") as file:
    blocks = file.read().split("\n\n")
    seeds = [int(x) for x in blocks[0][6:].split()]
    seeds_range = build_seeds(seeds)
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

dests = []
dests_p2 = []
print(seeds)
for i in range(7):
    if i == 0:
        dests = calc_next(sts_map, seeds)
        dests_p2 = calc_next(sts_map, seeds_range)
    if i == 1:
        dests = calc_next(stf_map, dests)
        dests_p2 = calc_next(stf_map, dests_p2)
    if i == 2:
        dests = calc_next(ftw_map, dests)
        dests_p2 = calc_next(ftw_map, dests_p2)
    if i == 3:
        dests = calc_next(wtl_map, dests)
        dests_p2 = calc_next(wtl_map, dests_p2)
    if i == 4:
        dests = calc_next(ltt_map, dests)
        dests_p2 = calc_next(ltt_map, dests_p2)
    if i == 5:
        dests = calc_next(tth_map, dests)
        dests_p2 = calc_next(tth_map, dests_p2)
    if i == 6:
        dests = calc_next(htl_map, dests)
        dests_p2 = calc_next(htl_map, dests_p2)

loc_min = min(dests)

print(f"Lowest Location number with single seeds: {loc_min}\n")
print(f"Lowest Location number with seed ranges: {min(dests_p2)}\n")

