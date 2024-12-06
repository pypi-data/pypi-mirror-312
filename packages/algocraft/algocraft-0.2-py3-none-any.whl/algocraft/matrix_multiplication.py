def matrix_multiplication(A, B):
    """
    Perform matrix multiplication of two 2D matrices A and B.

    Parameters:
    -----------
    A : list of lists
        The first matrix (a 2D list) where each element is a row in the matrix.
    B : list of lists
        The second matrix (a 2D list) where each element is a row in the matrix.

    Returns:
    --------
    list of lists
        The result of multiplying matrix A with matrix B. The result will also be a 2D matrix.

    Example:
    --------
    >>> from algocraft import matrix_multiplication
    >>> A = [[1, 2], [3, 4]]
    >>> B = [[5, 6], [7, 8]]
    >>> result = matrix_multiplication(A, B)
    >>> print(result)
    [[19, 22], [43, 50]]

    Notes:
    ------
    Matrix multiplication is possible if the number of columns in the first matrix (A)
    is equal to the number of rows in the second matrix (B). If these dimensions do not match,
    the function will raise a ValueError.

    Raises:
    -------
    ValueError:
        If the matrices cannot be multiplied due to incompatible dimensions.
    """
    # Get dimensions of A and B
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    # Check if the number of columns in A is equal to the number of rows in B
    if cols_A != rows_B:
        raise ValueError("Matrices cannot be multiplied, incompatible dimensions.")

    # Initialize the result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Perform matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result
