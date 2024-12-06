def floyd_warshall(graph):
    """
    Find the shortest paths between all pairs of nodes in a weighted graph using the Floyd-Warshall algorithm.

    Parameters:
    -----------
    graph : dict
        A dictionary representing the graph where keys are node identifiers and values are dictionaries
        of neighboring node identifiers and their respective edge weights.

    Returns:
    --------
    dict
        A dictionary where the keys are tuples of node pairs (i, j), and the values are the shortest
        distance between nodes i and j.

    Example:
    --------
    >>> graph = {
    >>>     'A': {'B': 3, 'C': 8, 'D': -4},
    >>>     'B': {'A': 3, 'D': 7},
    >>>     'C': {'A': 5, 'B': -2},
    >>>     'D': {'C': 4}
    >>> }
    >>> floyd_warshall(graph)
    {('A', 'A'): 0, ('A', 'B'): 3, ('A', 'C'): 5, ('A', 'D'): -4, 
     ('B', 'A'): 3, ('B', 'B'): 0, ('B', 'C'): -2, ('B', 'D'): 7, 
     ('C', 'A'): 5, ('C', 'B'): 1, ('C', 'C'): 0, ('C', 'D'): 4, 
     ('D', 'A'): 1, ('D', 'B'): 4, ('D', 'C'): 4, ('D', 'D'): 0}

    code:
    ------
    # Initialize distance matrix
    nodes = list(graph.keys())
    dist = { (i, j): float('inf') for i in nodes for j in nodes }
    
    # Set the distances for direct edges
    for node in nodes:
        dist[(node, node)] = 0  # Distance to itself is 0
        for neighbor, weight in graph[node].items():
            dist[(node, neighbor)] = weight
    
    # Floyd-Warshall algorithm
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[(i, j)] > dist[(i, k)] + dist[(k, j)]:
                    dist[(i, j)] = dist[(i, k)] + dist[(k, j)]
    
    return dist
    """
    
    # Initialize distance matrix
    nodes = list(graph.keys())
    dist = { (i, j): float('inf') for i in nodes for j in nodes }
    
    # Set the distances for direct edges
    for node in nodes:
        dist[(node, node)] = 0  # Distance to itself is 0
        for neighbor, weight in graph[node].items():
            dist[(node, neighbor)] = weight
    
    # Floyd-Warshall algorithm
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[(i, j)] > dist[(i, k)] + dist[(k, j)]:
                    dist[(i, j)] = dist[(i, k)] + dist[(k, j)]
    
    return dist
