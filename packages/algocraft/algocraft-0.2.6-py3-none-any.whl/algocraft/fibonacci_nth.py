def fibonacci_nth(n):
    """
    Retrieve the nth Fibonacci number.

    Parameters:
    -----------
    n : int
        The position of the Fibonacci sequence to retrieve. The sequence starts at index 0.

    Returns:
    --------
    int
        The nth Fibonacci number.

    Example:
    --------
    >>> from algocraft import fibonacci_nth
    >>> result = fibonacci_nth(7)
    >>> print(result)
    13

    code:
    ------
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative indices.")
    
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
    
    Raises:
    -------
    ValueError:
        If the input n is negative, as Fibonacci number is not defined for negative indices.
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative indices.")
    
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
