import numpy as np

def simplex(c, A, b):
    """
    Solve a Linear Programming problem using the Simplex method.

    Parameters:
    -----------
    c : list or np.array
        Coefficients of the objective function (1D array).
        
    A : list or np.array
        Coefficients of the constraints (2D array, each row represents a constraint).
        
    b : list or np.array
        Right-hand side values of the constraints (1D array).
        
    Returns:
    --------
    dict
        A dictionary containing:
        - 'optimal_value': the optimal value of the objective function
        - 'solution': the optimal values of the decision variables
        - 'iterations': number of iterations performed
    
    Example:
    --------
    >>> c = [-3, -2]
    >>> A = [[1, 1], [2, 1]]
    >>> b = [4, 5]
    >>> result = simplex(c, A, b)
    >>> print(result)
    {'optimal_value': -10.0, 'solution': [2.0, 2.0], 'iterations': 2}

    code:

    ------
    # Convert inputs to numpy arrays for easier manipulation
    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    m, n = A.shape
    # Augment A with identity matrix for slack variables
    A = np.hstack([A, np.eye(m)])
    c = np.concatenate([c, np.zeros(m)])
    
    # Initial Basic Feasible Solution (BFS)
    basic_vars = list(range(n, n + m))  # Slack variables
    non_basic_vars = list(range(n))  # Original variables
    
    # Iterating until optimality condition is satisfied
    iteration = 0
    while True:
        # Calculate the reduced costs (c_j - z_j)
        c_b = c[basic_vars]
        A_b = A[:, basic_vars]
        b_b = b
        
        # Solve for z_j
        z = np.linalg.solve(A_b, b_b)
        
        # Compute the objective value for each non-basic variable
        reduced_costs = c[non_basic_vars] - np.dot(c_b, np.linalg.inv(A_b) @ A[:, non_basic_vars])
        
        # If all reduced costs are non-negative, we've found the optimal solution
        if np.all(reduced_costs >= 0):
            break
        
        # Find entering variable (most negative reduced cost)
        entering = non_basic_vars[np.argmin(reduced_costs)]
        
        # Compute the direction of the pivot (the amount of each variable that can increase)
        d = np.linalg.solve(A_b, A[:, entering])
        
        # Compute the ratio of the right-hand side to the pivot direction
        ratios = b_b / d
        ratios[d > 0] = np.inf  # Ignore negative or zero directions
        leaving_idx = np.argmin(ratios)
        
        # Perform pivot operation
        leaving = basic_vars[leaving_idx]
        basic_vars[leaving_idx] = entering
        non_basic_vars[non_basic_vars == entering] = leaving
        
        # Update b, A, and c for the new tableau
        b_b = b_b - ratios[leaving_idx] * d
        
        iteration += 1
    
    # Final optimal solution
    optimal_value = np.dot(c[basic_vars], z)
    
    # Create a solution vector with both original and slack variables
    solution = np.zeros(n + m)  # Extended size to account for slack variables
    solution[basic_vars] = z
    
    return {'optimal_value': optimal_value, 'solution': solution.tolist(), 'iterations': iteration}
    """
    
    # Convert inputs to numpy arrays for easier manipulation
    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    m, n = A.shape
    # Augment A with identity matrix for slack variables
    A = np.hstack([A, np.eye(m)])
    c = np.concatenate([c, np.zeros(m)])
    
    # Initial Basic Feasible Solution (BFS)
    basic_vars = list(range(n, n + m))  # Slack variables
    non_basic_vars = list(range(n))  # Original variables
    
    # Iterating until optimality condition is satisfied
    iteration = 0
    while True:
        # Calculate the reduced costs (c_j - z_j)
        c_b = c[basic_vars]
        A_b = A[:, basic_vars]
        b_b = b
        
        # Solve for z_j
        z = np.linalg.solve(A_b, b_b)
        
        # Compute the objective value for each non-basic variable
        reduced_costs = c[non_basic_vars] - np.dot(c_b, np.linalg.inv(A_b) @ A[:, non_basic_vars])
        
        # If all reduced costs are non-negative, we've found the optimal solution
        if np.all(reduced_costs >= 0):
            break
        
        # Find entering variable (most negative reduced cost)
        entering = non_basic_vars[np.argmin(reduced_costs)]
        
        # Compute the direction of the pivot (the amount of each variable that can increase)
        d = np.linalg.solve(A_b, A[:, entering])
        
        # Compute the ratio of the right-hand side to the pivot direction
        ratios = b_b / d
        ratios[d > 0] = np.inf  # Ignore negative or zero directions
        leaving_idx = np.argmin(ratios)
        
        # Perform pivot operation
        leaving = basic_vars[leaving_idx]
        basic_vars[leaving_idx] = entering
        non_basic_vars[non_basic_vars == entering] = leaving
        
        # Update b, A, and c for the new tableau
        b_b = b_b - ratios[leaving_idx] * d
        
        iteration += 1
    
    # Final optimal solution
    optimal_value = np.dot(c[basic_vars], z)
    
    # Create a solution vector with both original and slack variables
    solution = np.zeros(n + m)  # Extended size to account for slack variables
    solution[basic_vars] = z
    
    return {'optimal_value': optimal_value, 'solution': solution.tolist(), 'iterations': iteration}
