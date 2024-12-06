def factorial(n):
    """
    Calculate the factorial of a non-negative integer.

    Parameters:
    -----------
    n : int
        A non-negative integer for which the factorial is to be computed.

    Returns:
    --------
    int
        The factorial of the input integer.

    Example:
    --------
    >>> from algocraft import factorial
    >>> result = factorial(5)
    >>> print(result)
    120

    code:
    ------
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

    Raises:
    -------
    ValueError:
        If the input n is negative, as factorial is not defined for negative numbers.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)
