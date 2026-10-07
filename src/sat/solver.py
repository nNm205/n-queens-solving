import argparse
from time import perf_counter
from pysat.solvers import Glucose3
from src.common.validator import (
    render_board,
    validate_solution,
)
from src.sat.encoder import (
    encode_nqueens_pairwise,
    var_id,
)

def decode_model(
    model: list[int],
    n: int,
) -> list[int]:
    """Decode a SAT model into queen positions.

    Args:
        model: SAT model represented as signed literals.
        n: Size of the N x N board.

    Returns:
        List where queens[row] is the queen's column.

    Raises:
        RuntimeError: If no queen is found for a row.
    """

    positive_literals = {
        literal
        for literal in model
        if literal > 0
    }

    queens = []

    for row in range(n):
        queen_col = None

        for col in range(n):
            variable = var_id(row, col, n)

            if variable in positive_literals:
                queen_col = col
                break

        if queen_col is None:
            raise RuntimeError(f"No queen found in row {row}")

        queens.append(queen_col)

    return queens

def solve_nqueens(n: int) -> dict:
    """Solve the N-Queens problem using Glucose3 and pairwise encoding.

    Args:
        n: Size of the N x N board.

    Returns:
        Dictionary containing solver status, statistics, and solution.

    Raises:
        ValueError: If n is less than 1.
        RuntimeError: If a satisfiable model cannot be decoded correctly.
    """

    # ==========================================
    # Encode problem
    # ==========================================
    cnf = encode_nqueens_pairwise(n)

    # ==========================================
    # SAT solving
    # ==========================================
    start = perf_counter()

    with Glucose3(bootstrap_with=cnf.clauses) as solver:
        is_sat = solver.solve()
        solve_time = perf_counter() - start

        if not is_sat:
            return {
                "n": n,
                "status": "UNSAT",
                "solver": "glucose3",
                "encoding": "pairwise",
                "num_variables": cnf.nv,
                "num_clauses": len(cnf.clauses),
                "solve_time": solve_time,
                "solution": None,
                "valid": None,
            }

        model = solver.get_model()

    # ==========================================
    # Decode SAT model
    # ==========================================
    queens = decode_model(model=model, n=n)

    # ==========================================
    # Validate independently
    # ==========================================
    valid = validate_solution(queens=queens, n=n)

    return {
        "n": n,
        "status": "SAT",
        "solver": "glucose3",
        "encoding": "pairwise",
        "num_variables": cnf.nv,
        "num_clauses": len(cnf.clauses),
        "solve_time": solve_time,
        "solution": queens,
        "valid": valid,
    }

def main():
    parser = argparse.ArgumentParser(description="N-Queens SAT Solver")

    parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Board size",
    )

    parser.add_argument(
        "--show-board",
        action="store_true",
        help="Display solution board",
    )

    args = parser.parse_args()
    result = solve_nqueens(args.n)

    print("=" * 50)
    print("N-QUEENS SAT SOLVER")
    print("=" * 50)
    print(f"N              : {result['n']}")
    print(f"Solver         : {result['solver']}")
    print(f"Encoding       : {result['encoding']}")
    print(f"Status         : {result['status']}")
    print(f"Variables      : {result['num_variables']}")
    print(f"Clauses        : {result['num_clauses']}")
    print(f"Solve time     : {result['solve_time']:.6f} s")

    if result["status"] == "SAT":
        print(f"Valid solution : {result['valid']}")
        print(f"Queen columns  : {result['solution']}")

        if args.show_board:
            print()
            print(render_board(result["solution"], result["n"]))

if __name__ == "__main__":
    main()