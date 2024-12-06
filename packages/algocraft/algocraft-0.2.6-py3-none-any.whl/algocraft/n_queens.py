def n_queens(N):
    """
    Solve the N-Queens problem using backtracking.

    The N-Queens problem is a classic problem in computer science where the goal is to place 
    N chess queens on an NxN chessboard such that no two queens threaten each other. 
    This function uses backtracking to find one solution to the problem.

    Parameters:
    -----------
    N : int
        The number of queens and the size of the chessboard.

    Returns:
    --------
    bool
        True if a solution is found, else False if no solution exists.

    Example:
    --------
    >>> n_queens(4)
    [0, 0, 1, 0]
    [1, 0, 0, 0]
    [0, 1, 0, 0]
    [0, 0, 0, 1]

    code:
    ------
    if N < 1:
        raise ValueError("Number of queens must be at least 1.")
    
    # Create a chessboard with NxN matrix with all elements set to 0
    board = [[0] * N for _ in range(N)]
    
    def attack(i, j):
        for k in range(N):
            if board[i][k] == 1 or board[k][j] == 1:
                return True
        for k in range(N):
            for l in range(N):
                if (k + l == i + j) or (k - l == i - j):
                    if board[k][l] == 1:
                        return True
        return False

    def place_queen(n):
        if n == 0:
            return True
        for i in range(N):
            for j in range(N):
                if not attack(i, j) and board[i][j] != 1:  
                    board[i][j] = 1  
                    if place_queen(n - 1): 
                        return True
                    board[i][j] = 0  
        return False

    if place_queen(N):
        for row in board:
            print(row)  
        return True
    else:
        print("No solution exists")
        return False

    Raises:
    -------
    ValueError:
        If `N` is less than 1.
    """
    
    if N < 1:
        raise ValueError("Number of queens must be at least 1.")
    
    # Create a chessboard with NxN matrix with all elements set to 0
    board = [[0] * N for _ in range(N)]
    
    def attack(i, j):
        # Checking vertically and horizontally
        for k in range(N):
            if board[i][k] == 1 or board[k][j] == 1:
                return True
        # Checking diagonally
        for k in range(N):
            for l in range(N):
                if (k + l == i + j) or (k - l == i - j):
                    if board[k][l] == 1:
                        return True
        return False

    def place_queen(n):
        if n == 0:
            return True
        # Trying to place queens one by one
        for i in range(N):
            for j in range(N):
                if not attack(i, j) and board[i][j] != 1:  # If the position is safe
                    board[i][j] = 1  # Place the queen
                    if place_queen(n - 1):  # Recursively place the remaining queens
                        return True
                    board[i][j] = 0  # Backtrack if placing queen here doesn't work
        return False

    # Call the place_queen function to solve the problem
    if place_queen(N):
        for row in board:
            print(row)  # Print the board with 1s representing queens and 0s representing empty spots
        return True
    else:
        print("No solution exists")
        return False
