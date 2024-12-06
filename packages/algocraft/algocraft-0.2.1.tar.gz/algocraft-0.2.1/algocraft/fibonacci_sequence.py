def fibonacci_sequence(n):
    """
    Generate the Fibonacci sequence up to the nth term.

    Parameters:
    -----------
    n : int
        The number of terms in the Fibonacci sequence to generate. The sequence starts from index 0.

    Returns:
    --------
    list
        A list containing the Fibonacci sequence up to the nth term.

    Example:
    --------
    >>> from algocraft import fibonacci_sequence
    >>> result = fibonacci_sequence(7)
    >>> print(result)
    [0, 1, 1, 2, 3, 5, 8]

    Notes:
    ------
    The Fibonacci sequence is a series of numbers where a number is the sum of the two preceding ones,
    starting from 0 and 1. The sequence is as follows:
    0, 1, 1, 2, 3, 5, 8, 13, 21, ...
    
    Raises:
    -------
    ValueError:
        If the input n is negative, as Fibonacci sequence is not defined for negative numbers.
    """
    if n < 0:
        raise ValueError("Fibonacci sequence is not defined for negative numbers.")
    
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    
    return sequence
