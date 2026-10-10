# Pilot Benchmark Analysis

This note summarizes the benchmark runs completed on the local laptop before unrestricted academic licenses became available. All reported SAT solutions and successful CP/MIP solutions passed the shared independent validator.

## Data used

- `results/final_sat_encodings_small.csv`: 45 rows, five repeats for `N = 8, 16, 32`.
- `results/final_sat_encodings_n64.csv`: 9 rows, three repeats for `N = 64`.
- `results/final_solver_comparison_core.csv`: 25 rows, one run for each solver at `N = 8, 16, 24, 31, 32`.
- `results/final_solver_comparison_extended.csv`: 25 rows, one run for each solver at `N = 44, 45, 64, 100, 128`.
- `results/pilot/`: earlier pilot data, including SAT encoding runs at `N = 96, 128`.

Aggregated tables are available in `report/sat_encodings_summary.csv`, `report/solver_comparison_summary.csv`, and `report/benchmark_summary.csv`. Figures use a logarithmic y-axis and are available as `report/sat_encoding_runtime.svg` and `report/solver_runtime.svg`.

## Initial observations

1. Pairwise is the fastest encoding in the new repeated runs at `N = 8, 16, 32, 64`.
2. Sequential Counter is competitive at `N = 16`, but becomes slower as `N` increases; it takes about `10.2 s` at `N = 64` in the repeated batch.
3. Bitwise is substantially slower than the other encodings in the new `N = 32` and `N = 64` runs, although earlier pilot runs showed different behavior at `N = 128`. This variation means the final baseline should be selected only after checking repeated runs, hardware conditions, and encoding/model statistics.
4. In the cross-solver runs, CP-SAT and CPLEX CP remain practical through `N = 128` in the local environment. Their observed times remain below five seconds in the extended batch.
5. The bitwise SAT cross-solver run is highly variable: it ranges from milliseconds at small `N` to `266.9 s` at `N = 44`, then returns to lower times at some larger `N`. This should be discussed as solver search variability rather than interpreted as a monotonic scaling curve from one run.
6. CPLEX MIP is blocked by the Community Edition size limit from `N = 32` onward in the completed cross-solver batch. Gurobi succeeds at `N = 32` but is blocked by its restricted license at `N = 45` and above.

## Interpretation for the report

The current results are suitable for a pilot-analysis section and for demonstrating the effect of AMO encoding, model size, solver family, and license restrictions. They are not yet a final statistically stable comparison because the large cases have only one run and the encoding baseline has not been selected conclusively. After license activation, the core and extended cross-solver experiments should be repeated with the same protocol.
