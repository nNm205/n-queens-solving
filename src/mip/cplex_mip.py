import argparse
from time import perf_counter
from docplex.mp.model import Model
from src.common.validator import (
    render_board,
    validate_solution,
)

def solve_nqueens_cplex_mip(n: int) -> dict:
    """Solve the N-Queens problem using CPLEX MIP.

    Args:
        n: Size of the N x N board.

    Returns:
        Dictionary containing solver status, model statistics, timing,
        and solution.

    Raises:
        ValueError: If n is less than 1.
    """

    if n < 1:
        raise ValueError("n must be >= 1")

    build_start = perf_counter()
    model = Model(name="n_queens_cplex_mip")
    rows = range(n)
    cols = range(n)
    x = model.binary_var_matrix(rows, cols, name="x")

    # ==========================================
    # 1. Exactly one queen in every row
    # ==========================================
    for row in rows:
        model.add_constraint(
            model.sum(
                x[row, col]
                for col in cols
            )
            == 1
        )

    # ==========================================
    # 2. Exactly one queen in every column
    # ==========================================
    for col in cols:
        model.add_constraint(
            model.sum(
                x[row, col]
                for row in rows
            )
            == 1
        )

    # ==========================================
    # 3. At most one queen / main diagonal
    #    row - col = constant
    # ==========================================
    for diagonal in range(-(n - 1), n):
        positions = [
            (row, row - diagonal)
            for row in rows
            if 0 <= row - diagonal < n
        ]

        if len(positions) > 1:
            model.add_constraint(
                model.sum(
                    x[row, col]
                    for row, col in positions
                )
                <= 1
            )

    # ==========================================
    # 4. At most one queen / anti-diagonal
    #    row + col = constant
    # ==========================================
    for diagonal in range(2 * n - 1):
        positions = [
            (row, diagonal - row)
            for row in rows
            if 0 <= diagonal - row < n
        ]

        if len(positions) > 1:
            model.add_constraint(
                model.sum(
                    x[row, col]
                    for row, col in positions
                )
                <= 1
            )

    build_time = perf_counter() - build_start
    num_variables = model.number_of_variables
    num_constraints = model.number_of_constraints
    solve_start = perf_counter()
    solution = model.solve(log_output=False)
    solve_time = perf_counter() - solve_start
    solve_details = model.solve_details
    raw_status = solve_details.status

    if solution is not None:
        queens = []

        for row in rows:
            queen_col = None

            for col in cols:
                if solution.get_value(
                    x[row, col]
                ) > 0.5:
                    queen_col = col
                    break

            if queen_col is None:
                raise RuntimeError(f"No queen found in row {row}")

            queens.append(queen_col)

        valid = validate_solution(queens=queens, n=n)
        status = "SAT"

    elif (
        raw_status is not None
        and "infeasible"
        in raw_status.lower()
    ):
        queens = None
        valid = None
        status = "UNSAT"
    else:
        queens = None
        valid = None
        status = "UNKNOWN"

    return {
        "n": n,
        "method": "mip",
        "solver": "cplex_mip",
        "status": status,
        "raw_status": raw_status,
        "num_variables": num_variables,
        "num_constraints": num_constraints,
        "build_time": build_time,
        "solve_time": solve_time,
        "total_time": build_time + solve_time,
        "solution": queens,
        "valid": valid,
    }


def main() -> None:
    """Run the command-line interface for the CPLEX MIP solver."""
    
    parser = argparse.ArgumentParser(
        description="N-Queens CPLEX MIP Solver"
    )

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
    result = solve_nqueens_cplex_mip(args.n)

    print("=" * 50)
    print("N-QUEENS CPLEX MIP SOLVER")
    print("=" * 50)
    print(f"N              : {result['n']}")
    print(f"Solver         : {result['solver']}")
    print(f"Status         : {result['status']}")
    print(f"CPLEX status   : {result['raw_status']}")
    print(f"Variables      : {result['num_variables']}")
    print(f"Constraints    : {result['num_constraints']}")
    print(f"Build time     : {result['build_time']:.6f} s")
    print(f"Solve time     : {result['solve_time']:.6f} s")
    print(f"Total time     : {result['total_time']:.6f} s")

    if result["status"] == "SAT":
        print(f"Valid solution : {result['valid']}")
        print(f"Queen columns  : {result['solution']}")

        if args.show_board:
            print()
            print(render_board(result["solution"], result["n"]))

if __name__ == "__main__":
    main()