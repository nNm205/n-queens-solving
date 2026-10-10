import argparse
from experiments.config import (
    DEFAULT_SIZES,
    SAT_ENCODINGS,
)
from experiments.runner import (
    run_sat_encoding_experiment,
    run_solver_comparison_experiment,
    save_results,
)

def parse_args() -> argparse.Namespace:
    """Parse benchmark command-line arguments.

    Returns:
        Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser(description="N-Queens benchmark runner")

    parser.add_argument(
        "--experiment",
        choices=("sat-encodings", "solvers"),
        required=True,
        help="Benchmark experiment to run",
    )

    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=list(DEFAULT_SIZES),
        help="Board sizes to benchmark",
    )

    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Number of runs per configuration",
    )

    parser.add_argument(
        "--sat-encoding",
        choices=SAT_ENCODINGS,
        default="seqcounter",
        help="SAT encoding used in solver comparison",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV file",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=600.0,
        help="Hard timeout in seconds per solver configuration; use 0 to disable",
    )

    return parser.parse_args()

def main() -> None:
    """Run the selected benchmark experiment."""
    
    args = parse_args()

    if args.repeats < 1:
        raise ValueError("repeats must be >= 1")

    if any(n < 1 for n in args.sizes):
        raise ValueError("all board sizes must be >= 1")

    if args.timeout < 0:
        raise ValueError("timeout must be >= 0")

    timeout_seconds = args.timeout or None

    if args.experiment == "sat-encodings":
        results = run_sat_encoding_experiment(
            sizes=args.sizes,
            repeats=args.repeats,
            timeout_seconds=timeout_seconds,
        )

        output = args.output or "results/sat_encoding_results.csv"

    else:
        results = (
            run_solver_comparison_experiment(
                sizes=args.sizes,
                repeats=args.repeats,
                sat_encoding=args.sat_encoding,
                timeout_seconds=timeout_seconds,
            )
        )

        output = args.output or "results/solver_comparison_results.csv"

    save_results(
        results=results,
        output_path=output,
    )

if __name__ == "__main__":
    main()
