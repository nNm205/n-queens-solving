# Benchmark analysis and limitations

This note summarizes the complete current benchmark refresh. The three raw datasets were rerun in the current environment after activating the Gurobi academic license. Every SAT result was checked by the shared independent N-Queens validator.

## Data used

- `results/sat_encoding_n8-32_repeat5.csv`: five runs per encoding at `N = 8, 16, 32` (45 rows).
- `results/sat_encoding_n64_repeat3.csv`: three runs per encoding at `N = 64` (9 rows).
- `results/solver_comparison_matched_n8-128_repeat3.csv`: five methods, three runs per method, at ten board sizes (150 rows).
- `report/sat_encodings_summary.csv`, `report/solver_comparison_summary.csv`, and `report/benchmark_summary.csv`: aggregates regenerated from those three current raw datasets.
- `report/sat_encoding_runtime.svg` / `.pdf` and `report/solver_runtime.svg` / `.pdf`: figures regenerated from the current aggregates.

The total is 204 benchmark rows. Every row has status `SAT` and `valid=True`; there are no timeout, error, or license-limit rows.

## SAT encoding results

Pairwise is the provisional SAT baseline for the cross-solver comparison because it had the lowest median at three of four tested sizes. Sequential Counter was fastest at `N = 16`:

| N | Pairwise (s) | Sequential Counter (s) | Bitwise (s) | Repeats |
|---:|---:|---:|---:|---:|
| 8 | 0.0013 | 0.0015 | 0.0020 | 5 |
| 16 | 0.0169 | 0.0093 | 0.1088 | 5 |
| 32 | 0.0891 | 0.5117 | 16.7465 | 5 |
| 64 | 0.6686 | 12.3846 | 22.6755 | 3 |

These are observed medians from the measured PySAT/Glucose3 implementation and one computer; they do not establish a universal encoding ranking. Pairwise adds no auxiliary variables. Sequential Counter minimizes clause count at each reported size, while Pairwise minimizes variable count. Bitwise lies between them on both counts. Earlier exploratory SAT runs at `N = 96, 128` reached the 600-second timeout and are outside the repeated comparison.

## SAT formula size

Variable counts include board variables and encoder auxiliaries; clause counts cover the full formula. The at-least-one constraints are shared among encodings.

| N | Encoding | Variables | Clauses |
|---:|---|---:|---:|
| 8 | Pairwise | 64 | 744 |
| 8 | Sequential Counter | 270 | 600 |
| 8 | Bitwise | 170 | 724 |
| 16 | Pairwise | 256 | 6,352 |
| 16 | Sequential Counter | 1,182 | 2,728 |
| 16 | Bitwise | 568 | 3,924 |
| 32 | Pairwise | 1,024 | 52,640 |
| 32 | Sequential Counter | 4,926 | 11,592 |
| 32 | Bitwise | 1,846 | 19,796 |
| 64 | Pairwise | 4,096 | 428,864 |
| 64 | Sequential Counter | 20,094 | 47,752 |
| 64 | Bitwise | 6,132 | 95,572 |

## Matched five-method results

Each value is the median total time in seconds from three runs. The current batch ran all five methods under the active licenses.

| N | SAT | CP-SAT | CPLEX CP | CPLEX MIP | Gurobi MIP |
|---:|---:|---:|---:|---:|---:|
| 8 | 0.003 | 0.034 | 0.059 | 0.039 | 0.010 |
| 16 | 0.037 | 0.074 | 0.057 | 0.046 | 0.046 |
| 24 | 0.172 | 0.119 | 0.062 | 0.059 | 0.016 |
| 31 | 0.197 | 0.209 | 0.090 | 0.088 | 0.084 |
| 32 | 0.238 | 0.215 | 0.089 | 0.073 | 0.079 |
| 44 | 0.528 | 0.427 | 0.064 | 0.122 | 0.150 |
| 45 | 0.402 | 0.217 | 0.047 | 0.054 | 0.016 |
| 64 | 0.727 | 0.389 | 0.036 | 0.085 | 0.036 |
| 100 | 2.765 | 0.979 | 0.044 | 0.171 | 0.059 |
| 128 | 6.183 | 1.935 | 0.049 | 0.312 | 0.146 |

All five methods solved every size. By lowest measured median, SAT leads at `N = 8, 16`; Gurobi at `N = 24, 31, 45, 64`; CPLEX MIP at `N = 32`; and CPLEX CP at `N = 44, 100, 128`. At `N = 16`, SAT's median is 0.0368 s versus 0.0460 s for Gurobi. At `N = 64`, Gurobi and CPLEX CP are nearly tied (0.0360 s and 0.0362 s). Rankings are based on three runs and should not be generalized beyond this local setup.

## Environment and limitations

The machine was a Dell Inspiron 15 3511 with an Intel Core i5-1135G7, 8 GB RAM, and Windows 11 Pro build 22631. The runtime reported Python 3.11.8, PySAT 1.9.dev16, OR-Tools 9.15.6755, Gurobi 13.0.3, DOcplex 2.32.264, and CPLEX 22.2.0. CPLEX CP and MIP passed 1,100-variable license checks; Gurobi passed a 2,100-variable academic-license check. The last recorded full test-suite run passed 43 tests; pytest was not rerun for this benchmark refresh.

All current benchmark datasets were collected in a single refresh, but the sample is still small and timings can vary with warm-up, thermal conditions, background processes, and power state. Power mode and background load were not recorded. The 600-second timeout policy remains in effect; prior exploratory SAT `N = 96, 128` runs are excluded because they reached that limit.
