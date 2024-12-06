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

    Notes:
    ------
    The factorial of a number n is the product of all positive integers less than or equal to n.
    Factorial is denoted by n! and is defined as:
    n! = n * (n-1) * (n-2) * ... * 1
    Factorial of 0 is defined as 1.

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
