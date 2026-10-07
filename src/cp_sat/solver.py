import argparse
from time import perf_counter
from ortools.sat.python import cp_model
from src.common.validator import (
    render_board,
    validate_solution,
)

def solve_nqueens_cp_sat(n: int) -> dict:
    """Solve the N-Queens problem using OR-Tools CP-SAT.

    Args:
        n: Size of the N x N board.

    Returns:
        Dictionary containing solver status, timing statistics, and solution.

    Raises:
        ValueError: If n is less than 1.
    """

    if n < 1:
        raise ValueError("n must be >= 1")

    build_start = perf_counter()
    model = cp_model.CpModel()

    queens = [
        model.new_int_var(0, n - 1, f"q_{row}")
        for row in range(n)
    ]

    # No two queens share the same column.
    model.add_all_different(queens)

    # No two queens share the same diagonals.
    model.add_all_different(
        queens[row] + row
        for row in range(n)
    )

    model.add_all_different(
        queens[row] - row
        for row in range(n)
    )

    build_time = perf_counter() - build_start
    solver = cp_model.CpSolver()
    solve_start = perf_counter()
    status = solver.solve(model)
    solve_time = perf_counter() - solve_start

    if status in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE,
    ):
        solution = [
            solver.value(queen)
            for queen in queens
        ]

        valid = validate_solution(
            queens=solution,
            n=n,
        )

        normalized_status = "SAT"

    elif status == cp_model.INFEASIBLE:
        solution = None
        valid = None
        normalized_status = "UNSAT"

    else:
        solution = None
        valid = None
        normalized_status = "UNKNOWN"

    return {
        "n": n,
        "method": "cp_sat",
        "solver": "ortools_cp_sat",
        "status": normalized_status,
        "build_time": build_time,
        "solve_time": solve_time,
        "total_time": build_time + solve_time,
        "solution": solution,
        "valid": valid,
        "num_conflicts": solver.num_conflicts,
        "num_branches": solver.num_branches,
    }

def main() -> None:
    """Run the command-line interface for the CP-SAT solver."""

    parser = argparse.ArgumentParser(
        description="N-Queens OR-Tools CP-SAT Solver"
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

    result = solve_nqueens_cp_sat(args.n)

    print("=" * 50)
    print("N-QUEENS CP-SAT SOLVER")
    print("=" * 50)
    print(f"N              : {result['n']}")
    print(f"Solver         : {result['solver']}")
    print(f"Status         : {result['status']}")
    print(f"Build time     : {result['build_time']:.6f} s")
    print(f"Solve time     : {result['solve_time']:.6f} s")
    print(f"Total time     : {result['total_time']:.6f} s")
    print(f"Conflicts      : {result['num_conflicts']}")
    print(f"Branches       : {result['num_branches']}")

    if result["status"] == "SAT":
        print(f"Valid solution : {result['valid']}")
        print(f"Queen columns  : {result['solution']}")

        if args.show_board:
            print()
            print(
                render_board(
                    result["solution"],
                    result["n"],
                )
            )

if __name__ == "__main__":
    main()