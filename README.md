# N-Queens Solver Benchmark

An experimental comparison of SAT encodings and exact solving methods for the N-Queens problem, developed for Assignment 1 in Modern Problems in Computer Science.

## Methods

- **SAT:** PySAT with Glucose3 and Pairwise, Sequential Counter, or Bitwise at-most-one encodings.
- **Constraint programming:** OR-Tools CP-SAT and IBM ILOG CPLEX CP Optimizer.
- **Mixed-integer programming:** CPLEX MIP and Gurobi MIP.

All returned solutions are checked by a shared validator. Benchmarks record runtime and formulation-size metrics where available.

## Results summary

The latest matched comparison covers ten board sizes (`N = 8` to `128`) with three runs per method and size. It produced 138 validated solutions and 12 Gurobi `LICENSE_LIMIT` outcomes, with no timeouts or solver errors. CPLEX CP and MIP solved all tested sizes; Gurobi is license-limited from `N = 45`.

For SAT encodings, Pairwise was fastest at `N = 8, 32, 64`, and Sequential Counter was fastest at `N = 16`. Measurements at `N = 96, 128` are exploratory single runs. Results are specific to this local setup and are not a general solver ranking.

The [manuscript](report/manuscript.pdf) contains the detailed tables and discussion. See [aggregated results](report/benchmark_summary.csv), [runtime charts](report/solver_runtime.svg), and the [pilot analysis](report/pilot_analysis.md) for data provenance and limitations.

## Setup

Requires Python 3.11+ and [`uv`](https://docs.astral.sh/uv/). From the repository root:

```powershell
uv sync --python 3.11
```

CPLEX CP Optimizer requires a separate IBM installation. CPLEX and Gurobi runs also require locally available solver installations and valid licenses. License-restricted runs are recorded as `LICENSE_LIMIT`.

## Run

Solve an instance with a selected method:

```powershell
uv run python -m src.sat.solver --n 8 --encoding pairwise
uv run python -m src.cp_sat.solver --n 8
uv run python -m src.cp.cplex_cp --n 8
uv run python -m src.mip.cplex_mip --n 8
uv run python -m src.mip.gurobi_mip --n 8
```

Run benchmarks; CSV output defaults to `results/`:

```powershell
uv run python -m experiments.benchmark --experiment sat-encodings --sizes 8 16 32 --repeats 5
uv run python -m experiments.benchmark --experiment solvers --sizes 8 16 24 31 32 --repeats 3 --sat-encoding pairwise --timeout 600
```

Check solver availability and run the test suite:

```powershell
uv run python scripts/check_env.py
uv run python -m pytest -q
```

## Folder structure

```text
n-queens-solving/
├── experiments/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── config.py
│   └── runner.py
├── report/
│   ├── thumbnails/
│   │   ├── cas-email.jpeg
│   │   ├── cas-facebook.jpeg
│   │   ├── cas-gplus.jpeg
│   │   ├── cas-linkedin.jpeg
│   │   ├── cas-twitter.jpeg
│   │   └── cas-url.jpeg
│   ├── README.md
│   ├── benchmark_summary.csv
│   ├── cas-common.sty
│   ├── cas-model2-names.bst
│   ├── cas-sc.cls
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
│   ├── historical/
│   │   └── solver_comparison_pairwise_n8-128_repeat3.csv
│   ├── pilot/
│   │   ├── sat_encodings_round1.csv
│   │   ├── sat_encodings_round2.csv
│   │   ├── solver_comparison_bitwise_n8-32.csv
│   │   ├── solver_comparison_bitwise_n44-128.csv
│   │   ├── solver_comparison_license_boundary.csv
│   │   ├── solver_comparison_large.csv
│   │   ├── solver_comparison_n32.csv
│   │   └── solver_comparison_round1.csv
│   ├── sat_encoding_n8-32_repeat5.csv
│   ├── sat_encoding_n64_repeat3.csv
│   └── solver_comparison_matched_n8-128_repeat3.csv
├── scripts/
│   ├── analyze_results.py
│   └── check_env.py
├── src/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   └── validator.py
│   ├── cp/
│   │   ├── __init__.py
│   │   └── cplex_cp.py
│   ├── cp_sat/
│   │   ├── __init__.py
│   │   └── solver.py
│   ├── mip/
│   │   ├── __init__.py
│   │   ├── cplex_mip.py
│   │   └── gurobi_mip.py
│   └── sat/
│       ├── __init__.py
│       ├── encoder.py
│       └── solver.py
├── tests/
│   ├── test_benchmark.py
│   ├── test_cp_optimizer.py
│   ├── test_cp_optimizer_license.py
│   ├── test_cp_solvers.py
│   ├── test_cplex_license.py
│   ├── test_mip_solvers.py
│   └── test_sat_encodings.py
├── .gitignore
├── IMPLEMENTATION_PLAN.md
├── README.md
├── pyproject.toml
├── requirements.txt
└── uv.lock
```
