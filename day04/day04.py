import sys, re

with open(sys.argv[1], "r") as file:
    inputs = [line for line in file.read().splitlines()]
    cards = []
    for line in inputs:
        sc = [l for l in re.split(':|\|', line)]
        cw = set(sc[1].strip().split())
        ca = set(sc[2].strip().split())
        cards.append([cw, ca])

points = []
wins = dict()
for cn, cv in enumerate(cards):
    wins[cn+1] = len(cv[1].intersection(cv[0]))
    p = 2**(wins[cn+1]-1)
    if p == 0.5:
        points.append(0)
    else:
        points.append(p)

print(f"Scratchcards wins: {points}, \nyielding a sum of {sum(points)}\n")

# all originals
exploding_cards = [1 for i in range(len(cards))]
# stack of cards doesn't wrap around, so start with first card, then finish second card, ...
for i in range(len(cards)):
    for w in range(wins[i+1]):
        exploding_cards[i+w+1] += exploding_cards[i]

print(f"Total number of scratchcards: {sum(exploding_cards)}")
