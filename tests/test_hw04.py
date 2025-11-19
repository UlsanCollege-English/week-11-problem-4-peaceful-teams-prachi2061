import pytest
from hw04.main import bipartition

def is_valid_bipartition(graph, left, right):
    if left is None or right is None:
        return False
    # disjoint and covers all nodes
    if left & right:
        return False
    if set(graph) != (left | right):
        return False
    # edges cross
    for u, neigh in graph.items():
        for v in neigh:
            if (u in left and v in left) or (u in right and v in right):
                return False
    return True

def test_simple_chain():
    g = {'A':['B'], 'B':['A','C'], 'C':['B']}
    lr = bipartition(g)
    assert lr is not None and is_valid_bipartition(g, *lr)

def test_triangle_not_bipartite():
    g = {'A':['B','C'], 'B':['A','C'], 'C':['A','B']}
    assert bipartition(g) is None

def test_square_bipartite():
    g = {'A':['B','D'], 'B':['A','C'], 'C':['B','D'], 'D':['A','C']}
    lr = bipartition(g)
    assert lr is not None and is_valid_bipartition(g, *lr)

def test_disconnected_components():
    g = {
        'A':['B'], 'B':['A'],
        'C':['D'], 'D':['C'],
        'Z':[]
    }
    lr = bipartition(g)
    assert lr is not None and is_valid_bipartition(g, *lr)

@pytest.mark.parametrize("edge", [('X','Y'), ('Y','Z'), ('X','Z')])
def test_small_with_param(edge):
    X, Y, Z = 'X','Y','Z'
    g = {X:[Y], Y:[X,Z], Z:[Y]}
    # add an extra optional edge to test robustness
    u, v = edge
    g.setdefault(u, []).append(v)
    g.setdefault(v, []).append(u)
    lr = bipartition(g)
    # If we created a triangle, it must be None; else valid
    if set([tuple(sorted(edge))]) == {('X','Z')}:
        assert lr is None
    else:
        assert lr is not None and is_valid_bipartition(g, *lr)

def test_larger_grid_like():
    # 3x3 grid without diagonals is bipartite
    def idx(r,c): return f"{r},{c}"
    g = {}
    for r in range(3):
        for c in range(3):
            u = idx(r,c)
            g[u] = []
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                rr, cc = r+dr, c+dc
                if 0 <= rr < 3 and 0 <= cc < 3:
                    g[u].append(idx(rr,cc))
    lr = bipartition(g)
    assert lr is not None and is_valid_bipartition(g, *lr)
