import itertools
def prime_factors(n):
    for i in itertools.chain([2], itertools.count(3, 2)):
        if n <= 1:
            break
        while n % i == 0:
            n //= i
            yield i

import heapq
class PrioritySet(object):
    def __init__(self):
        self.heap = []
        self.set = set()
    def add(self, pri, d):
        if not d in self.set:
            heapq.heappush(self.heap, (pri, d))
            self.set.add(d)
    def get(self):
        pri, d = heapq.heappop(self.heap)
        self.set.remove(d)
        return (pri, d)

# O(logV)
class UnionFind(object):
    def __init__(self, n):
        self.parents = [i for i in range(n)]
        self.rank = [0] * n
    def find(self, x):
        if self.parents[x] == x:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x != y:
            if self.rank[x] < self.rank[y]:
                x, y = y, x
            if self.rank[x] == self.rank[y]:
                self.rank[x] += 1
            self.parents[y] = x

# edges = defaultdict(dict)
#         src(int) => dst(int) => cost(int)
# O((E+V)logV)
import heapq
from collections import defaultdict
def dijkstra(edges, start=0):
    costs = defaultdict(lambda: float('inf'))
    costs[start] = 0
    prev = defaultdict(lambda: None)
    queue = [(0, start)]
    while len(queue) > 0:
        cost, node = heapq.heappop(queue)
        if costs[node] < cost:
            continue
        for next_node, c in edges[node].items():
            new_cost = cost + c
            if costs[next_node] > new_cost:
                costs[next_node] = new_cost
                prev[next_node] = node
                heapq.heappush(queue, (new_cost, next_node))
    return costs, prev

# edges = defaultdict(dict)
#         src(int) => dst(int) => cost(int)
# O(EV)
from collections import defaultdict
def belman_ford(edges, num_of_vertices, start=0):
    inf = float('inf')
    costs = defaultdict(lambda: inf)
    costs[start] = 0
    prev = defaultdict(lambda: None)
    for i in range(num_of_vertices):
        for src, sub_edges in edges.items():
            for dst, cost in sub_edges.items():
                if costs[src] == inf:
                    continue
                new_cost = costs[src] + cost
                if costs[dst] > new_cost:
                    costs[dst] = new_cost
                    prev[dst] = src
                    if i == num_of_vertices - 1:
                        return None, None
    return costs, prev

# edges = [(src, dst, cost), ...]
#         0 <= src, dst < num_of_vertices
# O(ElogV)
def minimum_spanning_tree(edges, num_of_vertices):
    edges = sorted(edges, key=lambda edge: edge[2])
    uf = UnionFind(num_of_vertices)
    mst = []
    for edge in edges:
        if uf.find(edge[0]) != uf.find(edge[1]):
            mst.append(edge)
    return mst

# edges = defaultdict(dict)
#         src(int) => dst(int) => capacity(int)
#         dst(int) => src(int) => 0
# O (EV^2)
# min edge cover = |V| - max matching (no ioslated vertice)
# min vertice cover = max matching (bipartite graph)
# max stable set = |V| - max matching (bipartite graph)
import queue
from collections import defaultdict
def max_flow(edges, num_of_vertices, start, goal):
    level = defaultdict(lambda: -1)
    seen = set()

    def bfs(s):
        level[s] = 0
        q = queue.Queue()
        q.put(s)
        while not q.empty():
            v = q.get()
            for nv, cap in edges[v].items():
                if cap > 0 and level[nv] < 0:
                    level[nv] = level[v] + 1
                    q.put(nv)

    def dfs(v, t, f):
        if v == t:
            return f
        for nv, cap in edges[v].items():
            if (v, nv) in seen:
                continue
            seen.add((v, nv))
            if cap > 0 and level[v] < level[nv]:
                d = dfs(nv, t, min(f, cap))
                if d > 0:
                    edges[v][nv] -= d
                    edges[nv][v] += d
                    return d
        return 0

    flow = 0
    while True:
        level.clear()
        bfs(start)
        if level[goal] < 0:
            return flow
        seen.clear()
        while True:
            f = dfs(start, goal, float('inf'))
            if f == 0:
                break
            flow += f
    return flow
