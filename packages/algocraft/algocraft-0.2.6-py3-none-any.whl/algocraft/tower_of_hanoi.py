def tower_of_hanoi(n, s_pole, d_pole, i_pole):
    """
    Solve the Tower of Hanoi problem and print the steps required to move all discs.

    The Tower of Hanoi is a classic puzzle where the objective is to move a set of discs 
    from the source pole to the destination pole using an auxiliary pole, with the restriction 
    that only one disc can be moved at a time and no disc may be placed on top of a smaller disc.

    Parameters:
    -----------
    n : int
        The number of discs to be moved.
    s_pole : str
        The source pole where the discs are initially placed.
    d_pole : str
        The destination pole where the discs need to be moved.
    i_pole : str
        The auxiliary pole used to assist in moving the discs.

    Returns:
    --------
    None
        This function does not return anything, but prints the steps of the solution.

    Example:
    --------
    >>> tower_of_hanoi(3, 'A', 'C', 'B')
    Move disc 1 from pole A to pole C
    Move disc 2 from pole A to pole B
    Move disc 1 from pole C to pole B
    Move disc 3 from pole A to pole C
    Move disc 1 from pole B to pole A
    Move disc 2 from pole B to pole C
    Move disc 1 from pole A to pole C

    Notes:
    ------
    def tower_of_hanoi(n, s_pole, d_pole, i_pole):
        if n <= 0:
            raise ValueError("The number of discs must be a positive integer.")

        if n == 1:
            print(f"Move disc 1 from pole {s_pole} to pole {d_pole}")
            return

        # Move n-1 discs from source to auxiliary pole
        tower_of_hanoi(n - 1, s_pole, i_pole, d_pole)

        # Move the nth disc from source to destination
        print(f"Move disc {n} from pole {s_pole} to pole {d_pole}")

        # Move the n-1 discs from auxiliary to destination
        tower_of_hanoi(n - 1, i_pole, d_pole, s_pole)


    Raises:
    -------
    ValueError:
        If `n` is not a positive integer.
    """
    
    if n <= 0:
        raise ValueError("The number of discs must be a positive integer.")

    if n == 1:
        print(f"Move disc 1 from pole {s_pole} to pole {d_pole}")
        return

    # Move n-1 discs from source to auxiliary pole
    tower_of_hanoi(n - 1, s_pole, i_pole, d_pole)

    # Move the nth disc from source to destination
    print(f"Move disc {n} from pole {s_pole} to pole {d_pole}")

    # Move the n-1 discs from auxiliary to destination
    tower_of_hanoi(n - 1, i_pole, d_pole, s_pole)
