import numpy as np

def strassen_matrix_multiplication(x, y):
    """
    Perform matrix multiplication using Strassen's algorithm.

    Strassen's algorithm is an optimized recursive approach for multiplying two square matrices.
    This implementation supports matrices of odd sizes by padding them to the next even dimension.

    Parameters:
    -----------
    x : numpy.ndarray
        The first matrix to multiply.
    y : numpy.ndarray
        The second matrix to multiply.

    Returns:
    --------
    numpy.ndarray
        The result of multiplying matrix x by matrix y using Strassen's algorithm.
        The result will have the same dimensions as the input matrices.

    Example:
    --------
    >>> import numpy as np
    >>> from algocraft import strassen_matrix_multiplication
    >>> x = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    >>> y = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])
    >>> result = strassen_matrix_multiplication(x, y)
    >>> print(result)
    [[-1  0  0]
     [ 0 -1  0]
     [ 0  0 -1]]

    code:
    ------
    if x.size == 1 or y.size == 1:
        return x * y

    if x.shape != y.shape:
        raise ValueError("Input matrices must have the same dimensions.")

    n = x.shape[0]

    # Padding matrices to make the size even if it's odd
    if n % 2 == 1:
        x = np.pad(x, ((0, 1), (0, 1)), mode='constant')
        y = np.pad(y, ((0, 1), (0, 1)), mode='constant')

    m = int(np.ceil(n / 2))

    # Splitting the matrices into sub-matrices
    a = x[:m, :m]
    b = x[:m, m:]
    c = x[m:, :m]
    d = x[m:, m:]

    e = y[:m, :m]
    f = y[:m, m:]
    g = y[m:, :m]
    h = y[m:, m:]

    # Calculating the 7 products
    p1 = strassen_matrix_multiplication(a, f - h)
    p2 = strassen_matrix_multiplication(a + b, h)
    p3 = strassen_matrix_multiplication(c + d, e)
    p4 = strassen_matrix_multiplication(d, g - e)
    p5 = strassen_matrix_multiplication(a + d, e + h)
    p6 = strassen_matrix_multiplication(b - d, g + h)
    p7 = strassen_matrix_multiplication(a - c, e + f)

    # Constructing the resulting matrix
    result = np.zeros((2 * m, 2 * m), dtype=np.int32)
    result[:m, :m] = p5 + p4 - p2 + p6
    result[:m, m:] = p1 + p2
    result[m:, :m] = p3 + p4
    result[m:, m:] = p1 + p5 - p3 - p7

    return result[:n, :n]
    
    Raises:
    -------
    ValueError:
        If the input matrices do not have the same dimensions.
    """

    if x.size == 1 or y.size == 1:
        return x * y

    if x.shape != y.shape:
        raise ValueError("Input matrices must have the same dimensions.")

    n = x.shape[0]

    # Padding matrices to make the size even if it's odd
    if n % 2 == 1:
        x = np.pad(x, ((0, 1), (0, 1)), mode='constant')
        y = np.pad(y, ((0, 1), (0, 1)), mode='constant')

    m = int(np.ceil(n / 2))

    # Splitting the matrices into sub-matrices
    a = x[:m, :m]
    b = x[:m, m:]
    c = x[m:, :m]
    d = x[m:, m:]

    e = y[:m, :m]
    f = y[:m, m:]
    g = y[m:, :m]
    h = y[m:, m:]

    # Calculating the 7 products
    p1 = strassen_matrix_multiplication(a, f - h)
    p2 = strassen_matrix_multiplication(a + b, h)
    p3 = strassen_matrix_multiplication(c + d, e)
    p4 = strassen_matrix_multiplication(d, g - e)
    p5 = strassen_matrix_multiplication(a + d, e + h)
    p6 = strassen_matrix_multiplication(b - d, g + h)
    p7 = strassen_matrix_multiplication(a - c, e + f)

    # Constructing the resulting matrix
    result = np.zeros((2 * m, 2 * m), dtype=np.int32)
    result[:m, :m] = p5 + p4 - p2 + p6
    result[:m, m:] = p1 + p2
    result[m:, :m] = p3 + p4
    result[m:, m:] = p1 + p5 - p3 - p7

    return result[:n, :n]


