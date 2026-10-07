from itertools import combinations
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool

SUPPORTED_ENCODINGS = (
    "pairwise",
    "seqcounter",
    "bitwise",
)

ENCODING_TYPES = {
    "seqcounter": EncType.seqcounter,
    "bitwise": EncType.bitwise,
}

def var_id(
    row: int,
    col: int,
    n: int,
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

def add_at_most_one(
    cnf: CNF,
    variables: list[int],
    encoding: str,
    vpool: IDPool,
) -> None:
    """Add an At-Most-One constraint using the selected encoding.

    Args:
        cnf: CNF formula to modify.
        variables: SAT variables participating in the constraint.
        encoding: AMO encoding name.
        vpool: Shared variable pool for auxiliary SAT variables.

    Raises:
        ValueError: If the encoding is not supported.
    """

    if encoding not in SUPPORTED_ENCODINGS:
        raise ValueError(
            f"Unsupported encoding: {encoding}. "
            f"Supported encodings: {SUPPORTED_ENCODINGS}"
        )

    if len(variables) <= 1:
        return

    if encoding == "pairwise":
        add_at_most_one_pairwise(
            cnf,
            variables,
        )
        return

    encoded = CardEnc.atmost(
        lits=variables,
        bound=1,
        vpool=vpool,
        encoding=ENCODING_TYPES[encoding],
    )

    cnf.extend(encoded.clauses)

def add_exactly_one(
    cnf: CNF,
    variables: list[int],
    encoding: str,
    vpool: IDPool,
) -> None:
    """Add an Exactly-One constraint using the selected AMO encoding.

    Args:
        cnf: CNF formula to modify.
        variables: SAT variables participating in the constraint.
        encoding: AMO encoding name.
        vpool: Shared variable pool for auxiliary SAT variables.
    """

    add_at_least_one(
        cnf,
        variables,
    )

    add_at_most_one(
        cnf,
        variables,
        encoding,
        vpool,
    )

def encode_nqueens(
    n: int,
    encoding: str = "pairwise",
) -> CNF:
    """Encode the N-Queens problem using the selected AMO encoding.

    Args:
        n: Size of the N x N board.
        encoding: AMO encoding method.

    Returns:
        CNF formula representing the N-Queens problem.

    Raises:
        ValueError: If n is less than 1 or the encoding is unsupported.
    """

    if n < 1:
        raise ValueError("n must be >= 1")

    if encoding not in SUPPORTED_ENCODINGS:
        raise ValueError(
            f"Unsupported encoding: {encoding}. "
            f"Supported encodings: {SUPPORTED_ENCODINGS}"
        )

    cnf = CNF()

    # Original board variables occupy IDs 1 ... n^2.
    # Auxiliary variables must start after them.
    vpool = IDPool(
        start_from=n * n + 1
    )

    # ==========================================
    # 1. Exactly one queen in every row
    # ==========================================
    for row in range(n):
        variables = [
            var_id(row, col, n)
            for col in range(n)
        ]

        add_exactly_one(
            cnf=cnf,
            variables=variables,
            encoding=encoding,
            vpool=vpool,
        )

    # ==========================================
    # 2. Exactly one queen in every column
    # ==========================================
    for col in range(n):
        variables = [
            var_id(row, col, n)
            for row in range(n)
        ]

        add_exactly_one(
            cnf=cnf,
            variables=variables,
            encoding=encoding,
            vpool=vpool,
        )

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
        add_at_most_one(
            cnf=cnf,
            variables=diagonal,
            encoding=encoding,
            vpool=vpool,
        )

    # ==========================================
    # 5. At most one queen / anti-diagonal
    # ==========================================
    for diagonal in anti_diagonals.values():
        add_at_most_one(
            cnf=cnf,
            variables=diagonal,
            encoding=encoding,
            vpool=vpool,
        )

    return cnf