def partition(arr, low, high):
    """
    Helper function to find the partition position for quicksort.
    """
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

def quick_sort(arr, low=0, high=None):
    """
    Sort a list of elements using the quick sort algorithm.

    Parameters:
    -----------
    arr : list
        The list of elements to be sorted.
    low : int, optional
        The starting index of the sublist to be sorted.
    high : int, optional
        The ending index of the sublist to be sorted.

    Returns:
    --------
    list
        The sorted list of elements.

    Example:
    --------
    >>> from algocraft import quick_sort
    >>> arr = [10, 7, 8, 9, 1, 5]
    >>> result = quick_sort(arr)
    >>> print(result)
    [1, 5, 7, 8, 9, 10]

    code:
    ------
    if high is None:
        high = len(arr) - 1

    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    
    return arr
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    
    return arr
