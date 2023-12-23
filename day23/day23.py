import sys

sys.setrecursionlimit(1000000)

slope_dirs = {'>': (0, 1), 'v': (1,0)}
dirs = [(0,1),(1,0),(-1,0),(0,-1)]

slopes = dict()
forest = []
trees = []
condensed_map = dict()

with open(sys.argv[1], "r") as file:
    lines = file.read().splitlines()
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '#':
                trees.append((i,j))
                continue
            if c in ['>', 'v']:
                slopes[(i,j)] = c
            forest.append((i,j))
            condensed_map[i,j] = []

start = (0,1)
n, m = len(lines),len(lines[0])
end = (n-1, m-2)

def get_neighs(node, dirs_=dirs):
    if len(dirs_) == 0:
        return []
    neighs = list(tuple(map(sum, zip(node, d))) for d in dirs_)
    neighs = [n for n in neighs if n in forest]
    return neighs


def dfs(path, node):
    dirs_ = None
    if node == end:
        return len(path)
    elif node in slopes.keys():
        dirs_ = [slope_dirs[slopes[node]]]
    elif node in forest:
        dirs_ = dirs
    else:
        dirs_ = []
    best = None
    for pos in get_neighs(node, dirs_):
        if pos in path:
            continue
        path.add(pos)
        res = dfs(path, pos)
        if best is None or (res is not None and res > best):
            best = res
        path.remove(pos)
    return best

paths = dfs(set(), start)

print(f"The longest slippery hike has {paths} steps\n")
# --------------- part 2

def condense():
    v_map = set()
    v_map.add(start)
    for node in forest:
        neighs = get_neighs(node)
        if len(neighs) > 2:
            v_map.add(node)
    v_map.add(end)

    for node in v_map:
        queue = [node]
        seen = {node}
        dist = 0
        while len(queue)>0:
            new_queue = []
            dist += 1
            for pos in queue:
                for neigh in get_neighs(pos):
                    if neigh not in seen:
                        seen.add(neigh)
                        if neigh in v_map:
                            condensed_map[node].append((dist, neigh))
                        else:
                            new_queue.append(neigh)
            queue = new_queue


def dfs2(path, pathlen, node):
    if node == end:
        return pathlen
    longest = 0
    for path_len, pos in condensed_map[node]:
        if pos in path:
            continue
        path.add(pos)
        res = dfs2(path, pathlen+path_len, pos)
        if longest is None or res is not None:
            longest = max(res, longest)
        path.remove(pos)
    return longest

condense()

longest = dfs2(set(), 0, start)
print(f"The longest dry hike has {longest} steps\n")
