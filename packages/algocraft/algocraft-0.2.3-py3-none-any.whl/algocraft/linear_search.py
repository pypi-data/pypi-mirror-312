def linear_search(list1, n, key):
    """
    Perform a linear search to find the index of the given element in a list.

    A linear search is a simple search algorithm that checks each element of the list 
    sequentially until the desired element is found.

    Parameters:
    -----------
    list1 : list
        The list in which the search will be performed.
    n : int
        The length of the list (number of elements).
    key : int
        The element to search for in the list.

    Returns:
    --------
    int
        The index of the element if found, else -1 if the element is not present in the list.

    Example:
    --------
    >>> linear_search([1, 3, 5, 4, 7, 9], 6, 4)
    3

    >>> linear_search([1, 3, 5, 4, 7, 9], 6, 10)
    -1

    Notes:
    ------
    - The function performs a linear search and works on both unsorted and sorted lists.
    - Time complexity: O(n), where n is the number of elements in the list.
    - The function will return the index of the first occurrence of the key if it exists.

    Raises:
    -------
    ValueError:
        If `n` is not a positive integer or if `list1` is empty.
    """
    
    if n <= 0:
        raise ValueError("The length of the list must be a positive integer.")
    
    for i in range(n):
        if list1[i] == key:
            return i
    return -1
