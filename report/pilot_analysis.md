# Benchmark analysis and limitations

This note records the current repeated benchmark evidence. Successful solver results passed the shared independent N-Queens validator. License rejections remain statuses and are not treated as solver runtimes.

## Data used

- `results/sat_encoding_n8-32_repeat5.csv`: five runs per encoding at `N = 8, 16, 32`.
- `results/sat_encoding_n64_repeat3.csv`: three runs per encoding at `N = 64`.
- `results/solver_comparison_matched_n8-128_repeat3.csv`: latest matched five-method batch, with three runs per method and size at the same ten board sizes.
- `report/sat_encodings_summary.csv`, `report/solver_comparison_summary.csv`, and `report/benchmark_summary.csv`: regenerated aggregate data based on the three raw benchmark CSVs above.
- `report/sat_encoding_runtime.svg` and `report/sat_encoding_runtime.pdf`: SAT encoding comparison figures.
- `report/solver_runtime.svg` and `report/solver_runtime.pdf`: current matched five-method comparison figures.

## Decisions and evidence

### Provisional SAT baseline: Pairwise

Pairwise is the provisional SAT baseline for the cross-solver comparison because it was fastest at three of the four repeated sizes and performed substantially better than Sequential Counter at $N=32$ and $N=64$. Sequential Counter was fastest at $N=16$:

| N | Pairwise (s) | Sequential Counter (s) | Bitwise (s) | Repeats |
|---:|---:|---:|---:|---:|
| 8 | 0.0013 | 0.0013 | 0.0013 | 5 |
| 16 | 0.0171 | 0.0098 | 0.1111 | 5 |
| 32 | 0.0886 | 0.4772 | 30.0100 | 5 |
| 64 | 1.7194 | 37.9285 | 22.7103 | 3 |

The choice is limited to the measured PySAT/Glucose3 implementation and repeated range `N = 8..64`. Pairwise adds no auxiliary variables. Sequential Counter remains a meaningful alternative and is the fastest encoding at `N = 16`. Exploratory sizes `N = 96, 128` are excluded because their earlier raw files were removed and a refreshed batch could not complete within the timeout. Pairwise should not be described as fastest at every measured size or as a universally optimal encoding.

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

`N = 8, 16, 24` provide small-to-medium reference cases. `N = 31/32` provides a boundary pair around the former CPLEX Community Edition model limit (961 versus 1,024 board variables); current CPLEX MIP accepts models above that boundary. `N = 44/45` straddles the Gurobi restricted-license boundary: `N = 44` has 1,936 board variables and `N = 45` has 2,025. `N = 64, 100, 128` extend the comparison to larger instances.

Three runs per configuration were selected as a practical repeat batch and summaries use the median. This remains a small sample. The minimum, maximum, and all individual outcomes remain in the CSV so the median is not mistaken for a distribution estimate. A common 600-second hard timeout was retained from the benchmark policy; timeout and license-limit configurations have no runtime in the median.

### Latest matched five-method results

| N | SAT (s) | CP-SAT (s) | CPLEX CP (s) | CPLEX MIP (s) | Gurobi MIP (s) |
|---:|---:|---:|---:|---:|---:|
| 8 | 0.0027 | 0.0403 | 0.0559 | 0.0491 | 0.0059 |
| 16 | 0.0392 | 0.0636 | 0.0553 | 0.0383 | 0.0448 |
| 24 | 0.1707 | 0.0915 | 0.0593 | 0.0597 | 0.0150 |
| 31 | 0.1966 | 0.1915 | 0.0587 | 0.0697 | 0.0792 |
| 32 | 0.2147 | 0.2075 | 0.0623 | 0.0756 | 0.0819 |
| 44 | 0.5256 | 0.3793 | 0.0612 | 0.1135 | 0.1471 |
| 45 | 0.5583 | 0.3987 | 0.0623 | 0.1064 | LICENSE_LIMIT |
| 64 | 1.7175 | 0.8585 | 0.0644 | 0.1935 | LICENSE_LIMIT |
| 100 | 6.4890 | 2.6017 | 0.0773 | 0.4271 | LICENSE_LIMIT |
| 128 | 13.7358 | 1.9131 | 0.0449 | 0.2649 | LICENSE_LIMIT |

Each numeric value is the median of three successful runs. The batch contains 138 validated solver results and 12 Gurobi `LICENSE_LIMIT` rows; it has no timeout or error rows. CPLEX CP and CPLEX MIP each solved all 30 configurations, including `N = 128`. Separate 1,100-variable license checks also passed for both CPLEX engines.

## Interpretation and limits

The matched batch provides a local comparison of all five methods through `N = 44`; above that size, Gurobi is censored by its restricted license. CPLEX CP has the lowest median at `N = 31, 32, 44, 45, 64, 100, 128`; Gurobi leads at `N = 24`, CPLEX MIP at `N = 16`, and SAT at `N = 8`. These observed rankings are based on three runs on one machine and should not be generalized.

The machine was a Dell Inspiron 15 3511, Intel Core i5-1135G7, 8 GB RAM, Windows 11 Pro build 22631. The current runtime reported Python 3.11.8, PySAT 1.9.dev16, OR-Tools 9.15.6755, Gurobi 13.0.3, DOcplex 2.32.264, and CPLEX 22.2.0. CPLEX CP and MIP passed full-version smoke checks with 1,100 variables; Gurobi remains restricted. The existing full test run passed: 43 tests. The refreshed benchmark batch completed without timeout or solver errors, but power mode and concurrent background load were not recorded.

A fresh exploratory refresh at `N = 96, 128` was stopped after Bitwise at `N = 96` and Pairwise at `N = 128` each reached the 600-second timeout. The benchmark runner writes its CSV only after a batch completes, so this interrupted attempt produced no new pilot CSV. The earlier pilot and historical raw CSVs have now been removed from `results/` and are not part of the reported analysis.

Power mode/AC status and concurrent background load were not recorded during the refreshed runs. Keep the three-run order and 600-second timeout for any further rerun, and document the Gurobi license restriction alongside its censored rows.
