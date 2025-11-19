from collections import deque

def bipartition(graph):
    """Return (left_set, right_set) if bipartite; else None."""
    color = {}
    left, right = set(), set()

    for start in graph:
        if start not in color:
            color[start] = 0
            queue = deque([start])

            while queue:
                u = queue.popleft()
                if color[u] == 0:
                    left.add(u)
                else:
                    right.add(u)

                for v in graph.get(u, []):
                    if v not in color:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return None

    return (left, right)