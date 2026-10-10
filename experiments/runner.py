from pathlib import Path
import csv
import multiprocessing
from experiments.config import (
    RESULT_FIELDS,
    SAT_ENCODINGS,
    SOLVER_METHODS,
)
from src.cp.cplex_cp import solve_nqueens_cplex_cp
from src.cp_sat.solver import solve_nqueens_cp_sat
from src.mip.cplex_mip import solve_nqueens_cplex_mip
from src.mip.gurobi_mip import solve_nqueens_gurobi_mip
from src.sat.solver import solve_nqueens

def classify_error(error: Exception) -> str:
    """Classify benchmark execution errors.

    Args:
        error: Exception raised during solver execution.

    Returns:
        Normalized benchmark error type.
    """

    message = str(error).lower()
    license_terms = (
        "community edition",
        "problem size limits",
        "size-limited license",
        "license limit",
        "limits exceeded",
    )

    if any(
        term in message
        for term in license_terms
    ):
        return "LICENSE_LIMIT"

    return "ERROR"

def normalize_result(
    raw_result: dict,
    experiment: str,
    run: int,
    method: str,
    encoding: str | None = None,
) -> dict:
    """Normalize a solver result into the common benchmark schema.

    Args:
        raw_result: Result returned by a solver.
        experiment: Name of the benchmark experiment.
        run: Repetition number.
        method: Solving method identifier.
        encoding: SAT encoding if applicable.

    Returns:
        Normalized benchmark result.
    """

    return {
        "experiment": experiment,
        "run": run,
        "n": raw_result.get("n"),
        "method": method,
        "solver": raw_result.get("solver"),
        "encoding": encoding,
        "status": raw_result.get("status"),
        "valid": raw_result.get("valid"),
        "num_variables": raw_result.get("num_variables"),
        "num_clauses": raw_result.get("num_clauses"),
        "num_constraints": raw_result.get("num_constraints"),
        "encoding_time": raw_result.get("encoding_time"),
        "build_time": raw_result.get("build_time"),
        "solve_time": raw_result.get("solve_time"),
        "total_time": raw_result.get("total_time"),
        "raw_status": raw_result.get("raw_status"),
        "error_type": None,
        "error_message": None,
    }

def build_error_result(
    *,
    experiment: str,
    run: int,
    n: int,
    method: str,
    encoding: str | None,
    error: Exception,
) -> dict:
    """Build a normalized result for a failed solver run.

    Args:
        experiment: Name of the benchmark experiment.
        run: Repetition number.
        n: Board size.
        method: Solving method identifier.
        encoding: SAT encoding if applicable.
        error: Exception raised during execution.

    Returns:
        Benchmark row describing the failed run.
    """

    return {
        "experiment": experiment,
        "run": run,
        "n": n,
        "method": method,
        "solver": None,
        "encoding": encoding,
        "status": classify_error(error),
        "valid": None,
        "num_variables": None,
        "num_clauses": None,
        "num_constraints": None,
        "encoding_time": None,
        "build_time": None,
        "solve_time": None,
        "total_time": None,
        "raw_status": None,
        "error_type": type(error).__name__,
        "error_message": str(error),
    }

def run_solver(
    *,
    experiment: str,
    run: int,
    method: str,
    n: int,
    encoding: str | None = None,
) -> dict:
    """Run one solver and return a normalized benchmark result.

    Args:
        experiment: Name of the benchmark experiment.
        run: Repetition number.
        method: Solver method to execute.
        n: Size of the N x N board.
        encoding: SAT encoding if method is SAT.

    Returns:
        Normalized benchmark result.

    Raises:
        ValueError: If method or SAT encoding is unsupported.
    """

    if method not in SOLVER_METHODS:
        raise ValueError(f"Unsupported method: {method}")

    if method == "sat":
        if encoding not in SAT_ENCODINGS:
            raise ValueError(f"Unsupported SAT encoding: {encoding}")

    try:
        if method == "sat":
            raw_result = solve_nqueens(n=n, encoding=encoding)

        elif method == "cp_sat":
            raw_result = solve_nqueens_cp_sat(n)

        elif method == "cplex_cp":
            raw_result = solve_nqueens_cplex_cp(n)

        elif method == "cplex_mip":
            raw_result = solve_nqueens_cplex_mip(n)

        else:
            raw_result = solve_nqueens_gurobi_mip(n)

        return normalize_result(
            raw_result=raw_result,
            experiment=experiment,
            run=run,
            method=method,
            encoding=encoding,
        )

    except Exception as error:
        return build_error_result(
            experiment=experiment,
            run=run,
            n=n,
            method=method,
            encoding=encoding,
            error=error,
        )


def _solver_process_entry(
    result_queue,
    solver_kwargs: dict,
) -> None:
    """Execute one solver call in a child process.

    A separate process is used so a timed-out solver can be terminated on
    Windows as well as on POSIX systems.
    """

    result_queue.put(run_solver(**solver_kwargs))


def build_timeout_result(
    *,
    experiment: str,
    run: int,
    n: int,
    method: str,
    encoding: str | None,
    timeout_seconds: float,
) -> dict:
    """Build a normalized result for a solver that exceeded its timeout."""

    return {
        "experiment": experiment,
        "run": run,
        "n": n,
        "method": method,
        "solver": None,
        "encoding": encoding,
        "status": "TIMEOUT",
        "valid": None,
        "num_variables": None,
        "num_clauses": None,
        "num_constraints": None,
        "encoding_time": None,
        "build_time": None,
        "solve_time": timeout_seconds,
        "total_time": timeout_seconds,
        "raw_status": None,
        "error_type": "TIMEOUT",
        "error_message": (
            f"Solver exceeded the {timeout_seconds:g}-second time limit"
        ),
    }


def run_solver_with_timeout(
    *,
    experiment: str,
    run: int,
    method: str,
    n: int,
    encoding: str | None = None,
    timeout_seconds: float | None = None,
) -> dict:
    """Run one solver directly or with a hard process timeout."""

    solver_kwargs = {
        "experiment": experiment,
        "run": run,
        "method": method,
        "n": n,
        "encoding": encoding,
    }

    if timeout_seconds is None:
        return run_solver(**solver_kwargs)

    context = multiprocessing.get_context("spawn")
    result_queue = context.Queue()
    process = context.Process(
        target=_solver_process_entry,
        args=(result_queue, solver_kwargs),
    )
    process.start()
    process.join(timeout_seconds)

    if process.is_alive():
        process.terminate()
        process.join()
        return build_timeout_result(
            experiment=experiment,
            run=run,
            n=n,
            method=method,
            encoding=encoding,
            timeout_seconds=timeout_seconds,
        )

    if not result_queue.empty():
        return result_queue.get()

    return build_error_result(
        experiment=experiment,
        run=run,
        n=n,
        method=method,
        encoding=encoding,
        error=RuntimeError(
            f"Solver process exited without returning a result (exit code {process.exitcode})"
        ),
    )


def run_sat_encoding_experiment(
    sizes: list[int],
    repeats: int,
    timeout_seconds: float | None = None,
) -> list[dict]:
    """Run the SAT encoding comparison experiment.

    Args:
        sizes: Board sizes to benchmark.
        repeats: Number of runs for each configuration.

    Returns:
        List of normalized benchmark results.
    """

    results = []

    for n in sizes:
        for encoding in SAT_ENCODINGS:
            for run in range(1, repeats + 1):
                print(
                    f"[RUN] SAT | "
                    f"N={n} | "
                    f"encoding={encoding} | "
                    f"run={run}"
                )

                result = run_solver_with_timeout(
                    experiment="sat_encodings",
                    run=run,
                    method="sat",
                    n=n,
                    encoding=encoding,
                    timeout_seconds=timeout_seconds,
                )

                results.append(result)
                print_result(result)

    return results

def run_solver_comparison_experiment(
    sizes: list[int],
    repeats: int,
    sat_encoding: str,
    timeout_seconds: float | None = None,
) -> list[dict]:
    """Run the cross-method solver comparison experiment."""

    if sat_encoding not in SAT_ENCODINGS:
        raise ValueError(f"Unsupported SAT encoding: {sat_encoding}")

    results = []

    for n in sizes:
        for method in SOLVER_METHODS:
            for run in range(1, repeats + 1):
                encoding = sat_encoding if method == "sat" else None

                print(
                    f"[RUN] {method} | "
                    f"N={n} | "
                    f"run={run}"
                )

                result = run_solver_with_timeout(
                    experiment="solver_comparison",
                    run=run,
                    method=method,
                    n=n,
                    encoding=encoding,
                    timeout_seconds=timeout_seconds,
                )

                results.append(result)
                print_result(result)

    return results

def print_result(result: dict) -> None:
    """Print a concise benchmark result.

    Args:
        result: Normalized benchmark result.
    """
    
    print(
        f"      status={result['status']} | "
        f"valid={result['valid']} | "
        f"total_time={result['total_time']}"
    )

def save_results(
    results: list[dict],
    output_path: str,
) -> None:
    """Save benchmark results to a CSV file.

    Args:
        results: Benchmark rows to save.
        output_path: Destination CSV path.
    """

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(results)

    print(f"[DONE] Saved {len(results)} rows to {path}")
