# Pilot benchmark analysis

This note records the evidence and rationale used to revise the manuscript. Successful solver results passed the shared independent N-Queens validator. License rejections and unavailable executables are kept as statuses and are not treated as solver runtimes.

## Data used

- `results/final_sat_encodings_small.csv`: five runs per encoding at `N = 8, 16, 32`.
- `results/final_sat_encodings_n64.csv`: three runs per encoding at `N = 64`.
- `results/pilot/`: earlier exploratory data, including one run per encoding at `N = 96, 128`.
- `results/pairwise_solver_comparison_repeat3.csv`: new three-run comparison using Pairwise SAT at `N = 8, 16, 24, 31, 32, 44, 45, 64, 100, 128`.
- `report/sat_encodings_summary.csv`, `report/solver_comparison_summary.csv`, and `report/benchmark_summary.csv`: regenerated aggregate data. The new cross-solver summary uses the repeated Pairwise dataset; raw run outcomes remain in the results CSV.
- `report/sat_encoding_runtime.svg` and `report/sat_encoding_runtime.pdf`: SAT encoding comparison figures.
- `report/solver_runtime.svg` and `report/solver_runtime.pdf`: repeated Pairwise comparison figures for methods available in the current rerun.

## Decisions and evidence

### Provisional SAT baseline: Pairwise

Pairwise is the provisional SAT baseline for the cross-solver comparison because it was fastest at three of the four repeated sizes and performed substantially better than Sequential Counter at $N=32$ and $N=64$. Sequential Counter was fastest at $N=16$:

| N | Pairwise (s) | Sequential Counter (s) | Bitwise (s) | Repeats |
|---:|---:|---:|---:|---:|
| 8 | 0.0010 | 0.0015 | 0.0013 | 5 |
| 16 | 0.0158 | 0.0086 | 0.1042 | 5 |
| 32 | 0.0749 | 0.4728 | 15.7860 | 5 |
| 64 | 0.6018 | 10.2342 | 6.2919 | 3 |

The choice is limited to the measured PySAT/Glucose3 implementation and repeated range `N = 8..64`. Pairwise adds no auxiliary variables. Sequential Counter remains a meaningful alternative and is the fastest encoding at `N = 16`. The exploratory `N = 96, 128` data have one run per encoding, so they are not used to override this provisional selection. The full report should not describe Pairwise as fastest at every repeatedly measured size or as a universally optimal encoding.

### Cross-solver sizes and repetitions

The repeated comparison reuses pilot sizes to make old and new results traceable. `N = 8, 16, 24` provide small-to-medium reference cases. `N = 31/32` straddles the CPLEX Community Edition limit: the MIP model has `N^2` binary variables, so `N = 31` has 961 while `N = 32` has 1,024. `N = 44/45` straddles the available Gurobi restricted-license boundary: `N = 44` has 1,936 board variables and `N = 45` has 2,025. `N = 64, 100, 128` extend the comparison to larger instances where the non-MIP methods can still run.

Three runs per configuration were selected as a practical repeat batch and summaries use the median. This improves on the earlier one-run cross-solver pilot, but is still a small sample. The minimum, maximum, and all individual outcomes remain in the CSV so the median is not mistaken for a distribution estimate. A common 600-second hard timeout was retained from the existing benchmark policy; timeout and license-limit configurations have no runtime in the median.

### Repeated Pairwise cross-solver results

| N | SAT (s) | CP-SAT (s) | CPLEX MIP (s) | Gurobi MIP (s) |
|---:|---:|---:|---:|---:|
| 8 | 0.0032 | 0.0406 | 0.0485 | 0.0038 |
| 16 | 0.0339 | 0.0674 | 0.0335 | 0.0400 |
| 24 | 0.1134 | 0.1179 | 0.0435 | 0.0106 |
| 31 | 0.3248 | 0.1694 | 0.0498 | 0.0678 |
| 32 | 0.1373 | 0.2266 | LICENSE_LIMIT | 0.0592 |
| 44 | 0.3639 | 0.2945 | LICENSE_LIMIT | 0.1849 |
| 45 | 0.4983 | 0.4212 | LICENSE_LIMIT | LICENSE_LIMIT |
| 64 | 1.3146 | 0.6318 | LICENSE_LIMIT | LICENSE_LIMIT |
| 100 | 4.6194 | 1.9347 | LICENSE_LIMIT | LICENSE_LIMIT |
| 128 | 9.9293 | 2.9433 | LICENSE_LIMIT | LICENSE_LIMIT |

Each numeric value is the median of three successful runs. In the current rerun, all CPLEX CP configurations returned `ERROR` because `cpoptimizer.exe` was not discoverable; they are excluded from the table rather than mixed with earlier single-run CPLEX CP values. The earlier pilot did solve CPLEX CP cases through `N = 128`, but a matched repeated comparison must wait until its executable is available again.

## Interpretation and limits

The repeated Pairwise data support a local comparison of total runtime and show that CP-SAT and Pairwise SAT solve all tested sizes under the current setup. They do not establish a general solver ranking: only three runs were collected, the MIP solvers are censored by restricted licenses for larger sizes, and CPLEX CP is absent from the repeated matrix. The earlier Bitwise cross-solver times ranged from `0.0037 s` at `N = 8` to `266.9 s` at `N = 44`; those single observations motivated replacing Bitwise with the better-supported repeated Pairwise baseline, rather than supporting a scaling claim.

The machine detected during the rerun was a Dell Inspiron 15 3511, Intel Core i5-1135G7, 8 GB RAM, Windows 11 Pro build 22631. The current runtime reported Python 3.11.8, PySAT 1.9.dev15, OR-Tools 9.15.6755, Gurobi 13.0.3, DOcplex 2.32.264, and CPLEX 22.2.0. The Gurobi and CPLEX MIP licenses were restricted. The project history records 43 passing tests, but tests were not rerun for this report revision.

Before describing this as a final comparison, confirm whether the earlier October 10 CSVs were produced on this same hardware and software environment. For the next fully licensed run, record the computer's power mode/AC status, close or note heavy background workloads, and keep the same order, repeat count, and timeout across solvers. Record CPLEX CP's executable/version and both license types. If these conditions cannot be held constant, describe them as separate benchmark batches.
