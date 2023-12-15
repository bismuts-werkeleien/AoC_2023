import sys
import copy
from collections import defaultdict

box = defaultdict(list)

with open(sys.argv[1], "r") as file:
    line = file.readline().splitlines()[0].split(',')

def get_hash(ch, curr):
    curr += ch
    curr *= 17
    rem = curr % 256
    curr = rem
    return curr

# part 2: Helping Elf haSHBOX - the elf helper for labelling boxes
def heshbox(line):
    res = 0
    for seq in line:
        curr = 0
        splitter = ''
        if '=' in seq: splitter = '='
        elif '-' in seq: splitter = '-'
        
        s = seq.split(splitter)
        for ch in map(ord, s[0]):
            curr = get_hash(ch, curr)
        updated = False
        if curr in box:
            for idx, item in enumerate(box[curr]):
                if item[0] == s[0] and splitter == '=':
                    updated = True
                    box[curr][idx] = (s[0],int(s[1]))
                    break
                if item[0] == s[0] and splitter == '-':
                    del (box[curr][idx])
                    break
        if not updated and splitter == '=':
            box[curr].append((s[0], int(s[1])))
        res += curr
    return box
            
# part 1: hesh == Helping Elf haSH 
def hesh(line):
    res = 0
    for seq in line:
        curr = 0
        for ch in map(ord, seq):
            curr = get_hash(ch, curr)
        res += curr
    return res

print(f"The hash of the initialization sequence is {hesh(line)}\n")

# --------------- part 2

focus_power = 0
for key, lenses in heshbox(line).items():
    for slot, lens in enumerate(lenses):
        focus_power += (1 + key) * (1 + slot) * lens[1]
print(f"The focusing power of the lens configuration is {focus_power}\n")

