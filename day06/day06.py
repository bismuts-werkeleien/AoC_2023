import sys, re

with open(sys.argv[1], "r") as file:
    lines = file.read().splitlines()
    times = map(int, lines[0].split()[1:])
    big_time = ''
    for c in lines[0].split()[1:]:
        big_time += c
    big_time = int(big_time)
    dists = list(map(int, lines[1].split()[1:]))
    big_dist = ''
    for c in lines[1].split()[1:]:
        big_dist += c
    big_dist = int(big_dist)

ways_to_win = []
big_win = 0

for i, t in enumerate(times):
    wins = 0
    for s in range(t+1):
        dist = (t-s)*s
        if dist > dists[i]:
            wins += 1
    ways_to_win.append(wins)

margin = 1
for w in ways_to_win:
    margin *= w
print(f"There are {ways_to_win} ways to win,\n giving a margin of error of {margin}")

# --------------- part 2
for t in range(big_time+1):
    dist = (big_time - t) * t
    if dist > big_dist:
        big_win += 1


print(f"In a big race there are {big_win} ways to win\n")

