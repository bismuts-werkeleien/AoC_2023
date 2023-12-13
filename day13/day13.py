import sys

with open(sys.argv[1], "r") as file:
    blocks = file.read().split("\n\n")
    patterns = [block.splitlines() for block in blocks]

h_refl = []
h_smudged = []
v_refl = []
v_smudged = []
for pattern in patterns:
    #horizontal
    for i in range(1, len(pattern)):
        #count number of non-equal characters
        #where all are the same, s will be 0
        #s will be 1 for the reflection with the smudge
        row_pairs = zip(pattern[i-1::-1], pattern[i:])
        s = sum(ash1 != ash2 for row_u, row_d in row_pairs for ash1, ash2 in zip(row_u, row_d))
        if s == 0:
            h_refl.append(i)
        if s == 1:
            h_smudged.append(i)

    #vertical
    columns = list(zip(*pattern))
    for i in range(1, len(columns)):
        #count number of non-equal characters
        #where all are the same, s will be 0
        #s will be 1 for the reflection with the smudge
        column_pairs = zip(columns[i-1::-1], columns[i:])
        s = sum(ash1 != ash2 for col_l, col_r in column_pairs for ash1, ash2 in zip(col_l, col_r))
        if s == 0:
            v_refl.append(i)
        if s == 1:
            v_smudged.append(i)

summary = sum([h*100 for h in h_refl]) + sum(v_refl)
print(f"The summary of reflections is {summary}\n ")

# --------------- part 2

smudges = sum([h*100 for h in h_smudged]) + sum(v_smudged)
print(f"The summary of smudged reflections is {smudges}\n ")

