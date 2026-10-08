import argparse
from time import perf_counter
import gurobipy as gp
from gurobipy import GRB
from src.common.validator import (
    render_board,
    validate_solution,
)

def solve_nqueens_gurobi_mip(n: int) -> dict:
    """Solve the N-Queens problem using Gurobi MIP.

    Args:
        n: Size of the N x N board.

    Returns:
        Dictionary containing solver status, model statistics, timing,
        and solution.

    Raises:
        ValueError: If n is less than 1.
        RuntimeError: If a feasible solution cannot be decoded.
    """

    if n < 1:
        raise ValueError("n must be >= 1")

    build_start = perf_counter()
    model = gp.Model("n_queens_gurobi_mip")
    model.Params.OutputFlag = 0
    rows = range(n)
    cols = range(n)
    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

    # ==========================================
    # 1. Exactly one queen in every row
    # ==========================================
    for row in rows:
        model.addConstr(
            gp.quicksum(
                x[row, col]
                for col in cols
            )
            == 1
        )

    # ==========================================
    # 2. Exactly one queen in every column
    # ==========================================
    for col in cols:
        model.addConstr(
            gp.quicksum(
                x[row, col]
                for row in rows
            )
            == 1
        )

    # ==========================================
    # 3. At most one queen / main diagonal
    # ==========================================
    for diagonal in range(-(n - 1), n):
        positions = [
            (row, row - diagonal)
            for row in rows
            if 0 <= row - diagonal < n
        ]

        if len(positions) > 1:
            model.addConstr(
                gp.quicksum(
                    x[row, col]
                    for row, col in positions
                )
                <= 1
            )

    # ==========================================
    # 4. At most one queen / anti-diagonal
    # ==========================================
    for diagonal in range(2 * n - 1):
        positions = [
            (row, diagonal - row)
            for row in rows
            if 0 <= diagonal - row < n
        ]

        if len(positions) > 1:
            model.addConstr(
                gp.quicksum(
                    x[row, col]
                    for row, col in positions
                )
                <= 1
            )

    # Process pending model modifications before
    # recording model statistics.
    model.update()

    build_time = perf_counter() - build_start
    num_variables = model.NumVars
    num_constraints = model.NumConstrs
    solve_start = perf_counter()
    model.optimize()
    solve_time = perf_counter() - solve_start

    if model.Status == GRB.OPTIMAL:
        queens = []

        for row in rows:
            queen_col = None

            for col in cols:
                if x[row, col].X > 0.5:
                    queen_col = col
                    break

            if queen_col is None:
                raise RuntimeError(f"No queen found in row {row}")

            queens.append(queen_col)

        valid = validate_solution(queens=queens, n=n)
        status = "SAT"

    elif model.Status == GRB.INFEASIBLE:
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
        "solver": "gurobi_mip",
        "status": status,
        "raw_status": model.Status,
        "num_variables": num_variables,
        "num_constraints": num_constraints,
        "build_time": build_time,
        "solve_time": solve_time,
        "total_time": build_time + solve_time,
        "solution": queens,
        "valid": valid,
    }


def main() -> None:
    """Run the command-line interface for the Gurobi MIP solver."""
    
    parser = argparse.ArgumentParser(
        description="N-Queens Gurobi MIP Solver"
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
    result = solve_nqueens_gurobi_mip(args.n)

    print("=" * 50)
    print("N-QUEENS GUROBI MIP SOLVER")
    print("=" * 50)
    print(f"N              : {result['n']}")
    print(f"Solver         : {result['solver']}")
    print(f"Status         : {result['status']}")
    print(f"Gurobi status  : {result['raw_status']}")
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