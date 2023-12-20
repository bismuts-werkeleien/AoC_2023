import sys
from math import prod

types = {}

def conjunctions(vals):
    for dest in vals:
        if types[dest][0] == '&':
            for source, dests in modules.items():
                if dest in dests:
                    types[dest][1].update({source: '-'})


with open(sys.argv[1], "r") as file:
    comm = file.read().splitlines()
    modules = dict()
    for line in comm:
        m, dest = line.split(' -> ')
        if m[0] == '%':
            types[m[1:]] = ('%', 'off')
        elif m[0] == '&':
            types[m[1:]] = ('&', dict())
        else:
            types[m[1:]] = ('->', 'start')
        modules.update({m[1:]: dest.split(', ')})
    conjunctions(modules.keys())
    types['rx'] = dict()

pulses = [0, 0]

presses = 0
pulse_c = 0
rx = 0
while True:
    if presses == 1000:
        pulse_c = pulses[0] * pulses[1]
    presses += 1
    
    mod = 'roadcaster'
    queue = []
    pulses[0] += 1
    [queue.append((x, 0, mod)) for x in modules[mod]]
    
    while queue:
        curr = queue.pop(0)
        last = curr[2]
        pulse = curr[1]
        dest = curr[0]
        pulses[pulse] += 1
        if dest not in modules.keys():
            continue
        nexts = modules[dest]
        if types[dest][0] == '%':
            if pulse == 0:
                if types[dest][1] == 'on':
                    types[dest] = ('%', 'off')
                    [queue.append((d, 0, dest)) for d in nexts]
                else:
                    types[dest] = ('%', 'on')
                    [queue.append((d, 1, dest)) for d in nexts]
        elif types[dest][0] == '&':
            types[dest][1][last] = pulse
            if all(x == 1 for x in types[dest][1].values()):
                [queue.append((d, 0, dest)) for d in nexts]
            else:
                [queue.append((d, 1, dest)) for d in nexts]
            if 'rx' in nexts:
                if pulse == 1 and last not in types['rx'].keys():
                    types['rx'][last] = presses
    
    if len(types['rx']) == 4 and all(x >= 1 for x in types['rx'].values()):
        rx = prod(types['rx'].values())
        break


print(f"The product of pulses is {pulse_c}\n")

# --------------- part 2
print(f"The number of button presses to deliver is {rx}\n")

