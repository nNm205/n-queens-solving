# N-Queens Solver Benchmark

An experimental comparison of SAT encodings and exact solving methods for the N-Queens problem, developed for Assignment 1 in Modern Problems in Computer Science.

- **Author:** Nguyen Nhat Minh
- **Student ID:** `23021631`
- **Class:** `INT3011E 3`
Faculty of Information Technology, VNU University of Engineering and Technology (VNU-UET)

## Methods

- **SAT:** PySAT with Glucose3 and Pairwise, Sequential Counter, or Bitwise at-most-one encodings.
- **Constraint programming:** OR-Tools CP-SAT and IBM ILOG CPLEX CP Optimizer.
- **Mixed-integer programming:** CPLEX MIP and Gurobi MIP.

All solutions are checked by a shared validator. The manuscript contains the methodology, detailed tables, and discussion.

## Latest results

The complete matched comparison was rerun as one batch after activating the Gurobi academic license. It covers ten board sizes (`N = 8` to `128`) with three runs per method and size. All 150 runs produced validated solutions, with no timeouts, license limits, or solver errors. CPLEX CP/MIP and Gurobi solve all tested sizes.

Across the repeated SAT encoding runs, Pairwise had the lowest median at `N = 8, 32, 64`; Sequential Counter was fastest at `N = 16`. In the matched solver batch, SAT led at `N = 8, 16`, Gurobi at `N = 24, 31, 45` and narrowly at `N = 64` (0.0359984 s versus 0.0361838 s for CPLEX CP), CPLEX MIP at `N = 32`, and CPLEX CP at `N = 44, 100, 128`. At `N = 128`, the Pairwise SAT median was 6.183 s versus 0.049 s for CPLEX CP. These results describe this local setup and do not establish a general solver ranking. See the [manuscript](report/manuscript.pdf), [aggregated results](report/benchmark_summary.csv), and [runtime charts](report/solver_runtime.svg) for details.

## Setup

Requires Python 3.11+ and [`uv`](https://docs.astral.sh/uv/). From the repository root:

```powershell
uv sync --python 3.11
```

CPLEX CP Optimizer requires a separate IBM installation. CPLEX and Gurobi runs require locally available solver installations and valid licenses. License-restricted runs are recorded as `LICENSE_LIMIT`.

## Run benchmarks

The commands below reproduce the current main raw datasets. The output path is stated after each command.

SAT encoding runs at `N = 8, 16, 32`, five repeats each:

```powershell
uv run python -m experiments.benchmark --experiment sat-encodings --sizes 8 16 32 --repeats 5 --timeout 600 --output results/sat_encoding_n8-32_repeat5.csv
```

Creates `results/sat_encoding_n8-32_repeat5.csv`.

SAT encoding runs at `N = 64`, three repeats:

```powershell
uv run python -m experiments.benchmark --experiment sat-encodings --sizes 64 --repeats 3 --timeout 600 --output results/sat_encoding_n64_repeat3.csv
```

Creates `results/sat_encoding_n64_repeat3.csv`.

Matched five-solver runs at ten sizes, three repeats each:

```powershell
uv run python -m experiments.benchmark --experiment solvers --sizes 8 16 24 31 32 44 45 64 100 128 --repeats 3 --sat-encoding pairwise --timeout 600 --output results/solver_comparison_matched_n8-128_repeat3.csv
```

Creates `results/solver_comparison_matched_n8-128_repeat3.csv`.

Regenerate the aggregate tables and charts from the main datasets:

```powershell
uv run python scripts/analyze_results.py
```

This creates or updates `report/benchmark_summary.csv`, `report/sat_encodings_summary.csv`, `report/solver_comparison_summary.csv`, and the SAT and solver runtime charts (`.svg` and `.pdf`) in `report/`. The analysis reads the three current raw datasets: the two repeated SAT-encoding CSVs and the matched cross-solver CSV. See [pilot analysis](report/pilot_analysis.md) for the data scope and limitations.

To solve one instance directly:

```powershell
uv run python -m src.sat.solver --n 8 --encoding pairwise
uv run python -m src.cp_sat.solver --n 8
uv run python -m src.cp.cplex_cp --n 8
uv run python -m src.mip.cplex_mip --n 8
uv run python -m src.mip.gurobi_mip --n 8
```

## Folder structure

```text
n-queens-solving/
├── experiments/
│   ├── benchmark.py
│   ├── config.py
│   └── runner.py
├── report/
│   ├── benchmark_summary.csv
│   ├── manuscript.pdf
│   ├── manuscript.tex
│   ├── pilot_analysis.md
│   ├── references.bib
│   ├── sat_encodings_summary.csv
│   ├── sat_encoding_runtime.pdf
│   ├── sat_encoding_runtime.svg
│   ├── solver_comparison_summary.csv
│   ├── solver_runtime.pdf
│   └── solver_runtime.svg
├── results/
│   ├── sat_encoding_n8-32_repeat5.csv
│   ├── sat_encoding_n64_repeat3.csv
│   └── solver_comparison_matched_n8-128_repeat3.csv
├── scripts/
│   ├── analyze_results.py
│   └── check_env.py
├── src/
│   ├── common/
│   │   └── validator.py
│   ├── cp/
│   │   └── cplex_cp.py
│   ├── cp_sat/
│   │   └── solver.py
│   ├── mip/
│   │   ├── cplex_mip.py
│   │   └── gurobi_mip.py
│   └── sat/
│       ├── encoder.py
│       └── solver.py
├── tests/
│   ├── test_benchmark.py
│   ├── test_cp_optimizer.py
│   ├── test_cp_optimizer_license.py
│   ├── test_cp_solvers.py
│   ├── test_cplex_license.py
│   ├── test_gurobi_license.py
│   ├── test_mip_solvers.py
│   └── test_sat_encodings.py
├── IMPLEMENTATION_PLAN.md
├── pyproject.toml
├── requirements.txt
└── uv.lock
```
