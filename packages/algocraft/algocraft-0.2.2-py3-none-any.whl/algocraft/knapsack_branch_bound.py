import math

class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.ratio = value / weight

def knapsack_branch_bound(capacity, items):
    """
    Solves the 0/1 Knapsack Problem using Branch and Bound.

    Parameters:
    -----------
    capacity : int
        The capacity of the knapsack.
    items : list of Item
        The list of items where each item has a value and a weight.

    Returns:
    --------
    dict
        A dictionary containing:
        - 'optimal_value': The maximum value that can be carried in the knapsack.
        - 'selected_items': List of selected items (indices of the items).
        - 'iterations': Number of nodes visited during the search.

    Example:
    --------
    >>> items = [Item(60, 10), Item(100, 20), Item(120, 30)]
    >>> capacity = 50
    >>> result = knapsack_branch_bound(capacity, items)
    >>> print(result)
    {'optimal_value': 220, 'selected_items': [0, 1], 'iterations': 6}
    """
    
    # Sort items based on the value-to-weight ratio
    items.sort(key=lambda x: x.ratio, reverse=True)
    
    # Node definition: (level, current value, current weight, bound)
    def bound(node, capacity, items):
        if node['weight'] >= capacity:
            return 0
        profit_bound = node['value']
        j = node['level'] + 1
        total_weight = node['weight']
        
        while j < len(items) and total_weight + items[j].weight <= capacity:
            total_weight += items[j].weight
            profit_bound += items[j].value
            j += 1
        
        if j < len(items):
            profit_bound += (capacity - total_weight) * items[j].ratio
        
        return profit_bound
    
    def branch_and_bound(capacity, items):
        max_value = 0
        selected_items = []
        queue = []
        queue.append({'level': -1, 'value': 0, 'weight': 0, 'items': [], 'bound': 0})
        
        iterations = 0
        
        while queue:
            node = queue.pop(0)
            iterations += 1
            
            if node['level'] == len(items) - 1:
                continue
            
            level = node['level'] + 1
            
            # Include the current item
            include_node = {'level': level, 'value': node['value'] + items[level].value,
                            'weight': node['weight'] + items[level].weight, 'items': node['items'] + [level],
                            'bound': 0}
            if include_node['weight'] <= capacity:
                if include_node['value'] > max_value:
                    max_value = include_node['value']
                    selected_items = include_node['items']
                include_node['bound'] = bound(include_node, capacity, items)
                if include_node['bound'] > max_value:
                    queue.append(include_node)
            
            # Exclude the current item
            exclude_node = {'level': level, 'value': node['value'], 'weight': node['weight'],
                            'items': node['items'], 'bound': 0}
            exclude_node['bound'] = bound(exclude_node, capacity, items)
            if exclude_node['bound'] > max_value:
                queue.append(exclude_node)
        
        return max_value, selected_items, iterations
    
    optimal_value, selected_items, iterations = branch_and_bound(capacity, items)
    
    return {
        'optimal_value': optimal_value,
        'selected_items': selected_items,
        'iterations': iterations
    }

