def merge(arr, left, mid, right):
    """
    Helper function to merge two halves of the array.
    """
    n1 = mid - left + 1
    n2 = right - mid

    L = arr[left:mid+1]
    R = arr[mid+1:right+1]

    i = j = 0
    k = left

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def merge_sort(arr, left=0, right=None):
    """
    Sort a list of elements using the merge sort algorithm.

    Parameters:
    -----------
    arr : list
        The list of elements to be sorted.
    left : int, optional
        The starting index of the sublist to be sorted.
    right : int, optional
        The ending index of the sublist to be sorted.

    Returns:
    --------
    list
        The sorted list of elements.

    Example:
    --------
    >>> from algocraft import merge_sort
    >>> arr = [12, 11, 13, 5, 6, 7]
    >>> result = merge_sort(arr)
    >>> print(result)
    [5, 6, 7, 11, 12, 13]

    Notes:
    ------
    Merge sort works by recursively dividing the array in half and merging 
    the sorted halves back together.
    """
    if right is None:
        right = len(arr) - 1

    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)
    
    return arr
