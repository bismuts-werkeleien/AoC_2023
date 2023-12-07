import sys

with open(sys.argv[1], "r") as file:
    lines = file.read().splitlines()
    hands = []
    bids = dict()
    for line in lines:
        l = line.split()
        hands.append(l[0])
        bids[l[0]] = int(l[1])

order_cards = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}
order_cards_p2 = {'A': 13, 'K': 12, 'Q': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}

def get_type(hand, part):
    hand_set = set(hand)
    freqs = {c: hand.count(c) for c in hand_set}

    if part == 2 and 'J' in hand and len(hand_set) > 1:
        num_j = freqs['J']
        freqs['J'] = 0
        freqs[(max(freqs, key=freqs.get))] += num_j
        hand_set -= set('J')

    if len(hand_set) == 1:
        # Five of a kind
        return 6
    elif len(hand_set) == 2:
        if all(x < 4 for x in freqs.values()):
            # Full house
            return 4
        else:
            # Four of a kind
            return 5
    elif len(hand_set) == 3:
        if all(x < 3 for x in freqs.values()):
            # Two pair
            return 2
        else:
            # Three of a kind
            return 3
    elif all(x == 1 for x in freqs.values()):
        # High card
        return 0
    else:
        # One pair
        return 1

def get_order(hand, part):
    order = []
    for h in hand:
        if part == 1:
            order.append(order_cards[h])
        else:
            order.append(order_cards_p2[h])
    return tuple(order)

strengths = []
strengths2 = []
for hand in hands:
    strengths.append((get_type(hand, 1), get_order(hand, 1), hand))
    strengths2.append((get_type(hand, 2), get_order(hand, 2), hand))

#sort strengths after type, then order
strengths = sorted(strengths)
winnings = 0
for i, strength in enumerate(strengths):
    rank = i + 1
    winnings += (bids[strength[2]] * rank)

print(f"The total winnings are {winnings}\n ")

# --------------- part 2
strengths2 = sorted(strengths2)
winning2 = 0
for i, strength in enumerate(strengths2):
    rank = i + 1
    winning2 += (bids[strength[2]] * rank)

print(f"The total winnings with Jokers are {winning2}\n")

