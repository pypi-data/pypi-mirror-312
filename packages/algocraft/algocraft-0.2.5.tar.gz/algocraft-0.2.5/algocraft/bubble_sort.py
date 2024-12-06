def bubble_sort(arr):
    """
    Sort a list of elements using the bubble sort algorithm.

    Parameters:
    -----------
    arr : list
        The list of elements to be sorted.

    Returns:
    --------
    list
        The sorted list of elements.

    Example:
    --------
    >>> from algocraft import bubble_sort
    >>> arr = [5, 1, 4, 2, 8]
    >>> result = bubble_sort(arr)
    >>> print(result)
    [1, 2, 4, 5, 8]

    Notes:
    ------
    Bubble sort repeatedly swaps adjacent elements if they are in the wrong order.
    This process continues until the list is sorted.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
