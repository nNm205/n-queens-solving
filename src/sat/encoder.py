from itertools import combinations
from pysat.formula import CNF

def var_id(
    row: int, 
    col: int, 
    n: int
) -> int:
    """Map a board position to a SAT variable identifier.

    Args:
        row: Zero-based row index.
        col: Zero-based column index.
        n: Size of the N x N board.

    Returns:
        Positive integer representing the SAT variable.
    """
    
    return row * n + col + 1

def add_at_least_one(
    cnf: CNF,
    variables: list[int],
) -> None:
    """Add an At-Least-One constraint to a CNF formula.

    Args:
        cnf: CNF formula to modify.
        variables: SAT variables participating in the constraint.
    """

    cnf.append(variables)

def add_at_most_one_pairwise(
    cnf: CNF,
    variables: list[int],
) -> None:
    """Add a pairwise At-Most-One constraint to a CNF formula.

    Args:
        cnf: CNF formula to modify.
        variables: SAT variables participating in the constraint.
    """

    for x_i, x_j in combinations(variables, 2):
        cnf.append([-x_i, -x_j])

def add_exactly_one_pairwise(
    cnf: CNF,
    variables: list[int],
) -> None:
    """Add an Exactly-One constraint using pairwise encoding.

    Args:
        cnf: CNF formula to modify.
        variables: SAT variables participating in the constraint.
    """

    add_at_least_one(cnf, variables)
    add_at_most_one_pairwise(cnf, variables)

def encode_nqueens_pairwise(n: int) -> CNF:
    """Encode the N-Queens problem into CNF using pairwise encoding.

    Args:
        n: Size of the N x N board.

    Returns:
        CNF formula representing the N-Queens problem.

    Raises:
        ValueError: If n is less than 1.
    """
    
    if n < 1:
        raise ValueError("n must be >= 1")

    cnf = CNF()

    # ==========================================
    # 1. Exactly one queen in every row
    # ==========================================
    for row in range(n):
        variables = [
            var_id(row, col, n)
            for col in range(n)
        ]

        add_exactly_one_pairwise(cnf, variables)

    # ==========================================
    # 2. Exactly one queen in every column
    # ==========================================
    for col in range(n):
        variables = [
            var_id(row, col, n)
            for row in range(n)
        ]

        add_exactly_one_pairwise(cnf, variables)

    # ==========================================
    # 3. Build diagonal groups
    # ==========================================
    main_diagonals: dict[int, list[int]] = {}
    anti_diagonals: dict[int, list[int]] = {}

    for row in range(n):
        for col in range(n):
            variable = var_id(row, col, n)

            main_key = row - col
            anti_key = row + col

            main_diagonals.setdefault(
                main_key,
                [],
            ).append(variable)

            anti_diagonals.setdefault(
                anti_key,
                [],
            ).append(variable)

    # ==========================================
    # 4. At most one queen / main diagonal
    # ==========================================
    for diagonal in main_diagonals.values():
        if len(diagonal) > 1:
            add_at_most_one_pairwise(cnf, diagonal)

    # ==========================================
    # 5. At most one queen / anti diagonal
    # ==========================================
    for diagonal in anti_diagonals.values():
        if len(diagonal) > 1:
            add_at_most_one_pairwise(cnf, diagonal)

    return cnf