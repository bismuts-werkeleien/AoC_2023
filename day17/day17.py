import sys
import heapq

directions = [(0,-1), (-1, 0), (0,1), (1,0)]

with open(sys.argv[1], "r") as file:
    lines = [list(line) for line in file.read().splitlines()]
    row_c = len(lines)
    col_c = len(lines[0])

def heat_loss(pos, loss, p):
    flow_c = -1
    d = (1,1)
    queue = [(loss, pos, d, flow_c)]
    seen = {}
    debug = 0
    while queue:
        loss, pos, d_prev, flow_prev = heapq.heappop(queue)
        if (pos, d_prev, flow_prev) in seen:
            continue
        seen[(pos, d_prev, flow_prev)] = loss

        for d in directions:
            cubicle = tuple(map(sum, zip(pos, d)))
            flow_c = flow_prev+1 if d == d_prev else 1
            m = list(map(sum, zip(d_prev, d)))
            reverse = all(x == 0 for x in m) or sum(map(abs, m)) == 1
            #reverse = (directions[(i+2)%4] == d_prev)
            
            valid = False
            if p == 1 and flow_c <= 3:
                valid = True
            elif p == 2 and flow_c <= 10 and (d == d_prev or flow_prev >= 4 or flow_prev == -1):
                valid = True
            
            if 0 <= cubicle[1] < col_c and 0 <= cubicle[0] < row_c and valid and not reverse:
                cost = int(lines[cubicle[0]][cubicle[1]])
                heapq.heappush(queue, (loss+cost, cubicle, d, flow_c))

    loss = 1e9
    for (pos, d, flow_c), val in seen.items():
        if pos[0] == row_c - 1 and pos[-1] == col_c - 1:
            if p == 2 and flow_c < 4:
                continue
            loss = min(loss, val)
    return loss


print(f"The heat loss with regular crucibles is {heat_loss((0,0), 0, 1)}\n")

# --------------- part 2
print(f"The heat loss with ultra crucibles is {heat_loss((0,0), 0, 2)}\n")

