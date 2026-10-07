def validate_solution(
    queens: list[int],
    n: int,
) -> bool:
    """Check whether a queen placement is a valid N-Queens solution.

    Args:
        queens: List where queens[row] is the queen's column.
        n: Size of the N x N board.

    Returns:
        True if the solution is valid, otherwise False.
    """

    if len(queens) != n:
        return False

    # Column must be inside board.
    if any(
        col < 0 or col >= n
        for col in queens
    ):
        return False

    # No two queens share a column.
    if len(set(queens)) != n:
        return False

    main_diagonals = set()
    anti_diagonals = set()

    for row, col in enumerate(queens):
        main_key = row - col
        anti_key = row + col

        if main_key in main_diagonals:
            return False

        if anti_key in anti_diagonals:
            return False

        main_diagonals.add(main_key)
        anti_diagonals.add(anti_key)

    return True


def render_board(
    queens: list[int],
    n: int,
) -> str:
    """Render an N-Queens solution as a text-based board.

    Args:
        queens: List where queens[row] is the queen's column.
        n: Size of the N x N board.

    Returns:
        Multi-line string representing the board.
    """
    
    lines = []

    for row in range(n):
        cells = []

        for col in range(n):
            if queens[row] == col:
                cells.append("Q")
            else:
                cells.append(".")

        lines.append(" ".join(cells))

    return "\n".join(lines)