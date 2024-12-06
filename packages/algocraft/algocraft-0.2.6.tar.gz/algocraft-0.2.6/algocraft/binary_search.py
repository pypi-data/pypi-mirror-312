def binary_search(arr, target):
    """
    Perform binary search on a sorted list to find the target element.

    Parameters:
    -----------
    arr : list
        The sorted list of elements in which to search for the target.
    target : int or float
        The element to search for in the list.

    Returns:
    --------
    int
        The index of the target element if found; otherwise, -1.

    Example:
    --------
    >>> from algocraft import binary_search
    >>> arr = [1, 2, 3, 4, 5]
    >>> result = binary_search(arr, 3)
    >>> print(result)
    2

    Code:
    -----
    def binary_search(arr, target):
        low = 0
        high = len(arr) - 1
        
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        
        return -1
    """
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1
