def is_satisfying(clauses, assignment):
    """CNF clauses: each literal is (variable_name, is_positive)."""
    return all(any(assignment[var] == positive for var, positive in clause)
               for clause in clauses)

def brute_force_sat(variables, clauses):
    """Brute-force SAT solver for small examples only."""
    from itertools import product
    for values in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if is_satisfying(clauses, assignment):
            return assignment
    return None

def three_sat_to_clique(clauses):
    """
    Map 3-SAT clauses to a graph: one vertex per literal occurrence;
    connect vertices from different clauses if their literals are not contradictory.
    Returns (vertices, edges); a clique of size number-of-clauses corresponds
    to a consistent choice of one literal per clause (for 3-literal clauses).
    """
    vertices = [(ci, li, lit) for ci, clause in enumerate(clauses)
                for li, lit in enumerate(clause)]
    edges = []
    for i, (ci, _, (vi, pi)) in enumerate(vertices):
        for j in range(i+1, len(vertices)):
            cj, _, (vj, pj) = vertices[j]
            if ci != cj and not (vi == vj and pi != pj):
                edges.append((i, j))
    return vertices, edges

def clique_to_independent_set(n, edges):
    """Complement graph edge list."""
    edge_set = {tuple(sorted(e)) for e in edges}
    return [(i, j) for i in range(n) for j in range(i+1, n)
            if (i, j) not in edge_set]

def independent_set_to_vertex_cover(n, independent_set_vertices):
    """For graph G, V\\I is a vertex cover when I is an independent set."""
    return set(range(n)) - set(independent_set_vertices)

def vertex_cover_2_approx(n, edges):
    """Standard 2-approximation: repeatedly select both endpoints of an uncovered edge."""
    uncovered = {tuple(sorted(e)) for e in edges}
    cover = set()
    while uncovered:
        u, v = next(iter(uncovered))
        cover.update((u, v))
        uncovered = {e for e in uncovered if u not in e and v not in e}
    return cover
