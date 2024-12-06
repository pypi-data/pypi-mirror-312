def heapify(arr, n, i):
    """
    Helper function to maintain the heap property.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    """
    Sort a list of elements using the heap sort algorithm.

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
    >>> from algocraft import heap_sort
    >>> arr = [12, 11, 13, 5, 6, 7]
    >>> result = heap_sort(arr)
    >>> print(result)
    [5, 6, 7, 11, 12, 13]

    Notes:
    ------
    Heap sort first builds a max heap and then repeatedly extracts the maximum element 
    to get the sorted list.
    """
    n = len(arr)

    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

    return arr
