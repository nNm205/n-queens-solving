# Pilot benchmark analysis

This note records the current repeated benchmark evidence and the earlier pilot data. Successful solver results passed the shared independent N-Queens validator. License rejections remain statuses and are not treated as solver runtimes.

## Data used

- `results/final_sat_encodings_small.csv`: five runs per encoding at `N = 8, 16, 32`.
- `results/final_sat_encodings_n64.csv`: three runs per encoding at `N = 64`.
- `results/pilot/`: earlier exploratory data, including one run per encoding at `N = 96, 128`.
- `results/pairwise_solver_comparison_repeat3.csv`: new three-run comparison using Pairwise SAT at `N = 8, 16, 24, 31, 32, 44, 45, 64, 100, 128`.
- `results/cplex_activated_solver_comparison_repeat3.csv`: latest matched five-method batch, with three runs per method and size at the same ten board sizes.
- `report/sat_encodings_summary.csv`, `report/solver_comparison_summary.csv`, and `report/benchmark_summary.csv`: regenerated aggregate data. The current cross-solver summary uses the CPLEX-restored batch; both raw repeated datasets remain available for comparison.
- `report/sat_encoding_runtime.svg` and `report/sat_encoding_runtime.pdf`: SAT encoding comparison figures.
- `report/solver_runtime.svg` and `report/solver_runtime.pdf`: current matched five-method comparison figures.

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

### SAT formula size

Raw benchmark rows report the number of variables and clauses for each encoding. These counts are deterministic within each size; variable counts include board variables and encoder auxiliaries, and clause counts cover the full formula. ALO clauses are shared across encodings.

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

Pairwise minimizes variable count, whereas Sequential Counter minimizes clause count at each reported size. Bitwise lies between those two encodings in both variable and clause counts at all four sizes. These formula-size differences complement the runtime table; neither variable count nor clause count alone predicts the observed runtime.

### Cross-solver sizes and repetitions

The repeated comparison reuses pilot sizes to make old and new results traceable. `N = 8, 16, 24` provide small-to-medium reference cases. `N = 31/32` retains the earlier CPLEX Community Edition boundary pair (961 versus 1,024 board variables); the current CPLEX MIP license check now accepts models above that boundary. `N = 44/45` straddles the Gurobi restricted-license boundary: `N = 44` has 1,936 board variables and `N = 45` has 2,025. `N = 64, 100, 128` extend the comparison to larger instances.

Three runs per configuration were selected as a practical repeat batch and summaries use the median. This improves on the earlier one-run cross-solver pilot, but is still a small sample. The minimum, maximum, and all individual outcomes remain in the CSV so the median is not mistaken for a distribution estimate. A common 600-second hard timeout was retained from the existing benchmark policy; timeout and license-limit configurations have no runtime in the median.

### Latest matched five-method results

| N | SAT (s) | CP-SAT (s) | CPLEX CP (s) | CPLEX MIP (s) | Gurobi MIP (s) |
|---:|---:|---:|---:|---:|---:|
| 8 | 0.0012 | 0.0178 | 0.0283 | 0.0155 | 0.0022 |
| 16 | 0.0163 | 0.0301 | 0.0289 | 0.0189 | 0.0204 |
| 24 | 0.0678 | 0.0479 | 0.0292 | 0.0226 | 0.0055 |
| 31 | 0.0790 | 0.0765 | 0.0299 | 0.0326 | 0.0366 |
| 32 | 0.0837 | 0.0820 | 0.0315 | 0.0294 | 0.0400 |
| 44 | 0.2055 | 0.1469 | 0.0319 | 0.0419 | 0.0693 |
| 45 | 0.2119 | 0.1396 | 0.0328 | 0.0433 | LICENSE_LIMIT |
| 64 | 0.6672 | 0.3129 | 0.0366 | 0.0693 | LICENSE_LIMIT |
| 100 | 2.4379 | 0.8740 | 0.0389 | 0.1464 | LICENSE_LIMIT |
| 128 | 5.3069 | 1.5397 | 0.0414 | 0.2664 | LICENSE_LIMIT |

Each numeric value is the median of three successful runs. The batch contains 138 validated solver results and 12 Gurobi `LICENSE_LIMIT` rows; it has no timeout or error rows. CPLEX CP and CPLEX MIP each solved all 30 configurations, including `N = 128`. Separate 1,100-variable license checks also passed for both CPLEX engines.

## Interpretation and limits

The matched batch provides a local comparison of all five methods through `N = 44`; above that size, Gurobi is censored by its restricted license. CPLEX CP has the lowest median at `N = 31, 44, 45, 64, 100, 128`, while SAT leads at `N = 8, 16`, and CPLEX MIP leads at `N = 24, 32`. These observed rankings are based on three runs on one machine and should not be generalized. The earlier Bitwise cross-solver pilot ranged from `0.0037 s` at `N = 8` to `266.9 s` at `N = 44`; it remains single-observation exploratory evidence.

The machine was a Dell Inspiron 15 3511, Intel Core i5-1135G7, 8 GB RAM, Windows 11 Pro build 22631. The current runtime reported Python 3.11.8, PySAT 1.9.dev16, OR-Tools 9.15.6755, Gurobi 13.0.3, DOcplex 2.32.264, and CPLEX 22.2.0. CPLEX CP and MIP passed full-version smoke checks with 1,100 variables; Gurobi remains restricted. The current full test run passed: 43 tests.

Before treating the results as final, confirm the power mode/AC status and whether heavy background workloads were present during the run. The earlier October 10 CSVs do not record software versions or machine state, so describe them as a separate historical batch unless their environment can be confirmed. Keep the three-run order and 600-second timeout for any further rerun, and document the Gurobi license restriction alongside its censored rows.
