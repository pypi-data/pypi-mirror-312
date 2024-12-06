import heapq

def dijkstra(graph, start):
    """
    Find the shortest path in a weighted graph from the start node using Dijkstra's algorithm.

    Parameters:
    -----------
    graph : dict
        A dictionary representing the graph where keys are node identifiers and values are 
        dictionaries of neighboring node identifiers and their respective edge weights.
    start : str
        The starting node for Dijkstra's algorithm.

    Returns:
    --------
    dict
        A dictionary where the keys are node identifiers and the values are the shortest
        distances from the start node to that node.

    Example:
    --------
    >>> graph = {
    >>>     'A': {'B': 1, 'C': 4},
    >>>     'B': {'A': 1, 'C': 2, 'D': 5},
    >>>     'C': {'A': 4, 'B': 2, 'D': 1},
    >>>     'D': {'B': 5, 'C': 1}
    >>> }
    >>> dijkstra(graph, 'A')
    {'A': 0, 'B': 1, 'C': 3, 'D': 4}

    Notes:
    ------
    - Time complexity: O(E log V), where E is the number of edges and V is the number of vertices.
    """
    
    # Priority queue to keep track of the minimum distance nodes
    queue = [(0, start)]
    distances = {start: 0}  # Start node has a distance of 0
    visited = set()

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if neighbor not in visited and (neighbor not in distances or distance < distances[neighbor]):
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    
    return distances
