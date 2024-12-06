from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def _topological_sort_util(self, v, visited, stack):
        visited[v] = True

        for i in self.graph[v]:
            if not visited[i]:
                self._topological_sort_util(i, visited, stack)

        stack.insert(0, v)

    def topological_sort(self):
        """
        Perform topological sort on a directed acyclic graph (DAG).

        Returns:
        --------
        list
            A list representing the topological ordering of the vertices.

        Example:
        --------
        >>> from algocraft import Graph
        >>> g = Graph(6)
        >>> g.add_edge(5, 2)
        >>> g.add_edge(5, 0)
        >>> g.add_edge(4, 0)
        >>> g.add_edge(4, 1)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(3, 1)
        >>> result = g.topological_sort()
        >>> print(result)
        [5, 4, 2, 3, 1, 0]

        Notes:
        ------
        Topological sorting is applicable only for Directed Acyclic Graphs (DAGs).
        It orders the vertices such that for every directed edge u -> v, vertex u comes 
        before vertex v.
        """
        visited = [False] * self.V
        stack = []

        for i in range(self.V):
            if not visited[i]:
                self._topological_sort_util(i, visited, stack)

        return stack
