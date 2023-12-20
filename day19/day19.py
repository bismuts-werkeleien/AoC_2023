import sys,re
import copy

def parse_workflow(rule):
    label,rest = rule.split('{')
    return {label:rest[:-1].split(',')}

def parse_parts(line):
    parts = line[1:-1].split(',')
    res = {}
    for p in parts:
        res[p[0]] = int(p[2:])
    return res

with open(sys.argv[1], "r") as file:
    workstr, ratingstr = file.read().split('\n\n')
    workflows = dict()
    for line in workstr.splitlines():
        workflows.update(parse_workflow(line))
    ratings = list(map(parse_parts, ratingstr.splitlines()))
    

def split_ranges(rating, key, comp, val):
    true_range = copy.deepcopy(rating)
    false_range = copy.deepcopy(rating)
    rule = rating[key]
    if comp == '>':
        t = range(val+1, rule.stop)
        f = range(rule.start, val+1)
    elif comp == '<':
        t = range(rule.start, val)
        f = range(val, rule.stop)
    true_range[key] = t
    false_range[key] = f
    return true_range, false_range


def workflow(rule, rating, part):
    if rule == 'A':
        if part == 1:
            return True
        lengths = 1
        for val in rating.values():
            lengths *= (val.stop-val.start)
        return lengths
    if rule == 'R':
        return False if part == 1 else 0

    *rules,default = workflows[rule]
    total = 0
    for cond in rules:
        cond, target = cond.split(':')
        val = int(cond[2:])
        if part == 1:
            if cond[1] == '<' and rating[cond[0]] < val or cond[1] == '>' and rating[cond[0]] > val:
                #switch to target and don't return
                return workflow(target, rating, 1)
        elif part == 2:
            matching, rating = split_ranges(rating, cond[0], cond[1], val)
            total += workflow(target, matching, 2)
    return workflow(default, rating, 1) if part == 1 else total + workflow(default, rating, 2)


accepted = 0
for rating in ratings:
    if workflow('in', rating, 1):
        accepted += sum(rating.values())

print(f"The rating numbers of accepted parts is {accepted}\n")

# --------------- part 2
parts = {"x": range(1,4001), "m": range(1,4001), "a": range(1,4001), "s": range(1,4001)}
p2 = workflow('in', parts, 2)

print(f"There are {p2} distinct combination of ratings\n")

