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

    Notes:
    ------
    The Fibonacci sequence is a series of numbers where a number is the sum of the two preceding ones,
    starting from 0 and 1. The sequence is as follows:
    0, 1, 1, 2, 3, 5, 8, 13, 21, ...
    
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
