import sys

with open(sys.argv[1], "r") as file:
    histories = [list(map(int, line.split())) for line in file.read().split("\n")]

def calc_prev(diffs):
    val = diffs[-1][0]
    for d in reversed(diffs[:-1]):
        val = d[0] - val
    return val

def calc_next(diffs):
    val = diffs[-1][-1]
    for d in reversed(diffs[:-1]):
        val = d[-1] + val
    return val

def calc_diff(history):
    diffs = [history]
    diff = [t - s for s, t in zip(history, history[1:])]
    diffs.append(diff)
    while not all(x == 0 for x in diff):
        diff = [t - s for s, t in zip(diffs[-1], diffs[-1][1:])]
        diffs.append(diff)
    return (calc_next(diffs), calc_prev(diffs))

next_histories = 0
prev_histories = 0
for history in histories[:-1]:
    sols = calc_diff(history)
    next_histories += sols[0]
    prev_histories += sols[1]

print(f"The next history values sum up to {next_histories}\n ")
# --------------- part 2
print(f"The previous history values sum up to {prev_histories}\n ")

