import argparse
from time import perf_counter
from docplex.cp.model import CpoModel
from src.common.validator import (
    render_board,
    validate_solution,
)

def solve_nqueens_cplex_cp(n: int) -> dict:
    """Solve the N-Queens problem using CPLEX CP Optimizer.

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

    model = CpoModel()

    queens = model.integer_var_list(
        n,
        0,
        n - 1,
        "q",
    )

    # No two queens share the same column.
    model.add(
        model.all_diff(queens)
    )

    # No two queens share the same diagonals.
    model.add(
        model.all_diff(
            queens[row] + row
            for row in range(n)
        )
    )

    model.add(
        model.all_diff(
            queens[row] - row
            for row in range(n)
        )
    )

    build_time = perf_counter() - build_start

    solve_start = perf_counter()

    result = model.solve(
        LogVerbosity="Quiet"
    )

    solve_time = perf_counter() - solve_start

    solve_status = (
        str(result.get_solve_status())
        if result is not None
        else "Unknown"
    )

    if (
        result is not None
        and result.is_solution()
    ):
        solution = [
            int(result.get_value(queen))
            for queen in queens
        ]

        valid = validate_solution(
            queens=solution,
            n=n,
        )

        normalized_status = "SAT"

    elif "infeasible" in solve_status.lower():
        solution = None
        valid = None
        normalized_status = "UNSAT"

    else:
        solution = None
        valid = None
        normalized_status = "UNKNOWN"

    return {
        "n": n,
        "method": "cp",
        "solver": "cplex_cp",
        "status": normalized_status,
        "raw_status": solve_status,
        "build_time": build_time,
        "solve_time": solve_time,
        "total_time": build_time + solve_time,
        "solution": solution,
        "valid": valid,
    }


def main() -> None:
    """Run the command-line interface for the CPLEX CP solver."""
    parser = argparse.ArgumentParser(
        description="N-Queens CPLEX CP Optimizer Solver"
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

    result = solve_nqueens_cplex_cp(args.n)

    print("=" * 50)
    print("N-QUEENS CPLEX CP SOLVER")
    print("=" * 50)
    print(f"N              : {result['n']}")
    print(f"Solver         : {result['solver']}")
    print(f"Status         : {result['status']}")
    print(f"CPLEX status   : {result['raw_status']}")
    print(f"Build time     : {result['build_time']:.6f} s")
    print(f"Solve time     : {result['solve_time']:.6f} s")
    print(f"Total time     : {result['total_time']:.6f} s")

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