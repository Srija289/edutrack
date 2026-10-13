from collections import deque

def bipartite_matching(left_nodes, adjacency):
    """Kuhn augmenting-path matching. adjacency[u] lists eligible right nodes."""
    match_right = {}
    def augment(u, seen):
        for v in adjacency.get(u, []):
            if v in seen:
                continue
            seen.add(v)
            if v not in match_right or augment(match_right[v], seen):
                match_right[v] = u
                return True
        return False
    count = 0
    for u in left_nodes:
        if augment(u, set()):
            count += 1
    return count, {u: v for v, u in match_right.items()}

def _residual_from_edges(n, edges):
    cap = [[0]*n for _ in range(n)]
    for u, v, c in edges:
        if c < 0:
            raise ValueError("Capacity cannot be negative")
        cap[u][v] += c
    return cap

def ford_fulkerson(n, edges, source, sink):
    """Edmonds-Karp-style BFS augmentations, returning max flow and residual graph."""
    residual = _residual_from_edges(n, edges)
    flow = 0
    while True:
        parent = [-1]*n
        parent[source] = source
        q = deque([source])
        while q and parent[sink] == -1:
            u = q.popleft()
            for v, c in enumerate(residual[u]):
                if c > 0 and parent[v] == -1:
                    parent[v] = u
                    q.append(v)
        if parent[sink] == -1:
            break
        amount, v = float("inf"), sink
        while v != source:
            u = parent[v]
            amount = min(amount, residual[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= amount
            residual[v][u] += amount
            v = u
        flow += amount
    return flow, residual

def edmonds_karp(n, edges, source, sink):
    return ford_fulkerson(n, edges, source, sink)

def dinic(n, edges, source, sink):
    residual = _residual_from_edges(n, edges)
    total = 0
    while True:
        level = [-1]*n
        level[source] = 0
        q = deque([source])
        while q:
            u = q.popleft()
            for v, c in enumerate(residual[u]):
                if c > 0 and level[v] < 0:
                    level[v] = level[u]+1
                    q.append(v)
        if level[sink] < 0:
            return total
        it = [0]*n
        def send(u, pushed):
            if u == sink:
                return pushed
            while it[u] < n:
                v = it[u]
                if residual[u][v] > 0 and level[v] == level[u]+1:
                    got = send(v, min(pushed, residual[u][v]))
                    if got:
                        residual[u][v] -= got
                        residual[v][u] += got
                        return got
                it[u] += 1
            return 0
        while True:
            pushed = send(source, float("inf"))
            if not pushed:
                break
            total += pushed

def konig_min_vertex_cover(left_nodes, adjacency, matching):
    """Minimum vertex cover from a maximum matching in a bipartite graph."""
    match_left = {u: v for v, u in matching.items()}
    seen_l, seen_r = set(), set()
    q = deque(u for u in left_nodes if u not in match_left)
    seen_l.update(q)
    while q:
        u = q.popleft()
        for v in adjacency.get(u, []):
            if match_left.get(u) == v or v in seen_r:
                continue
            seen_r.add(v)
            if v in matching and matching[v] not in seen_l:
                seen_l.add(matching[v])
                q.append(matching[v])
    return (set(left_nodes)-seen_l) | seen_r
