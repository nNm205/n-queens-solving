# N-Queens Solving: SAT Encoding and Exact Methods

This project studies the **N-Queens problem** using SAT solving and other exact solving approaches.

The project is developed for **Assignment 1 – Modern Problems in Computer Science** and focuses on experimentally comparing SAT-based solving with Constraint Programming, CP-SAT, and Mixed Integer Programming.

## Project Objectives

The main objectives are:

- Model the N-Queens problem using SAT.
- Compare different SAT At-Most-One encodings.
- Solve SAT instances using PySAT and Glucose3.
- Compare SAT solving with:
  - OR-Tools CP-SAT
  - CPLEX CP Optimizer
  - CPLEX MIP
  - Gurobi MIP
- Evaluate solver performance on increasingly large N-Queens instances.
- Compare:
  - Number of SAT variables
  - Number of SAT clauses
  - Number of MIP variables and constraints
  - Model/encoding time
  - Solving time
  - Total execution time
- Build a reproducible benchmark pipeline for experimental evaluation.

## Assignment and Report Information

This project is developed for Assignment 1 of the Modern Problems in Computer Science course. The selected topic is **N-Queens Solver** under the SAT Encoding for Logic Puzzles and N-Queens topic.

The final report will be written in English and structured as a scientific manuscript following the Elsevier-style report template provided for the assignment.

```text
Author      : Nguyen Nhat Minh
Student ID  : 23021631
Department  : Faculty of Information Technology
University  : VNU University of Engineering and Technology (VNU-UET)
Deadline    : 19 October 2026
Internal target: 16 October 2026
Repository  : https://github.com/nNm205/n-queens-solving
```

The repository link will be included in the report's **Data Availability** section. Experiments run before unrestricted academic licenses are available will explicitly report `LICENSE_LIMIT` and `TIMEOUT` outcomes as experimental limitations.

---

## Current Progress

### Completed

- [x] Project structure initialized.
- [x] Python environment configured and verified.
- [x] PySAT + Glucose3 verified.
- [x] OR-Tools CP-SAT verified.
- [x] Gurobi verified.
- [x] CPLEX MIP verified.
- [x] CPLEX CP Optimizer verified.
- [x] Generic SAT encoding architecture implemented.
- [x] Pairwise AMO encoding implemented.
- [x] Sequential Counter AMO encoding implemented.
- [x] Bitwise AMO encoding implemented.
- [x] Shared auxiliary-variable management using `IDPool`.
- [x] SAT solver implemented using Glucose3.
- [x] SAT model decoding and independent validation implemented.
- [x] SAT encoding, solving, and total execution times recorded.
- [x] OR-Tools CP-SAT N-Queens solver implemented.
- [x] CPLEX CP Optimizer N-Queens solver implemented.
- [x] CPLEX MIP N-Queens solver implemented.
- [x] Gurobi MIP N-Queens solver implemented.
- [x] Shared solution validation across all solving methods.
- [x] CP, CP-SAT, and MIP model build/solve times recorded.
- [x] Unified benchmark runner implemented.
- [x] Unified benchmark result schema implemented.
- [x] CSV result export implemented.
- [x] SAT encoding benchmark mode implemented.
- [x] Cross-solver benchmark mode implemented.
- [x] Repeated benchmark runs supported.
- [x] Solver errors are captured without terminating the full experiment.
- [x] CPLEX Community Edition size-limit errors are handled by the benchmark runner.
- [x] Automated tests cover SAT, CP, CP-SAT, MIP, and benchmark infrastructure.
- [x] Pilot SAT-encoding experiments completed for `N = 8, 16, 32, 64, 96, 128`.
- [x] Pilot cross-solver experiments completed for small, medium, large, and license-boundary cases.
- [x] Benchmark results exported to CSV under `results/`.
- [x] Environment check passes for all five solver families.
- [x] Full test suite passes: `43 passed`.
- [x] Report language, author metadata, deadline, and repository link confirmed.
- [x] Elsevier-style manuscript structure identified for the final report.
- [x] Hard per-configuration timeout implemented in the benchmark CLI.
- [x] Repeated SAT encoding benchmark completed for `N = 8, 16, 32` and `N = 64`.
- [x] Cross-solver core benchmark completed at `N = 8, 16, 24, 31, 32`.
- [x] Cross-solver extended benchmark completed at `N = 44, 45, 64, 100, 128`.
- [x] Pilot summary tables and SVG/PDF figures generated under `report/`.
- [x] English Elsevier-style report draft created in `report/manuscript.tex`.
- [x] Bibliography and report compilation instructions added.
- [x] MiKTeX CTAN repository configured and CAS dependencies installed.
- [x] CAS manuscript compiled successfully to `report/manuscript.pdf`.
- [x] Required Elsevier CAS class, bibliography style, thumbnails, and PDF figures tracked in the repository.
- [x] CAS report assets and reproducibility documentation committed locally; push is pending.
- [x] Latest report fixes pushed to the GitHub repository.

### In Progress / Remaining

- [ ] Activate Gurobi Academic License before large-scale experiments.
- [ ] Install or activate an unrestricted CPLEX academic license if available.
- [ ] Analyze pilot experiments and select the final board-size ranges.
- [ ] Define final benchmark size ranges and repetition counts.
- [x] Define timeout and error-handling policy for final experiments.
- [ ] Run final SAT encoding comparison experiments.
- [ ] Select the SAT encoding used for cross-method comparison.
- [ ] Run SAT vs CP vs CP-SAT vs MIP experiments.
- [ ] Re-run large-instance experiments after license upgrades, if available.
- [ ] Analyze benchmark results.
- [ ] Generate experimental tables and figures.
- [ ] Prepare the final scientific report.

While waiting for the Gurobi and CPLEX academic licenses, the current report draft can be reviewed locally at `report/manuscript.pdf`. The remaining experimental work is to rerun the final benchmark protocol after the licenses are activated, then update the tables, figures, discussion, and conclusion.

---

## N-Queens Representations

The project uses two main formulations depending on the solving paradigm.

### SAT / MIP Representation

Each board position is represented by a decision variable:

```text
x[row, col]
```

For SAT:

```text
x[row, col] ∈ {False, True}
```

For MIP:

```text
x[row, col] ∈ {0, 1}
```

The SAT variable identifier is:

```text
variable_id = row * N + col + 1
```

The original board therefore contains:

```text
N^2
```

decision variables.

### CP / CP-SAT Representation

CPLEX CP and OR-Tools CP-SAT use:

```text
queens[row] = column
```

where:

```text
queens[row] ∈ {0, ..., N - 1}
```

This representation directly assigns exactly one queen to each row.

---

## SAT Formulation

The SAT formulation contains four constraint families:

- Exactly one queen in every row.
- Exactly one queen in every column.
- At most one queen on every main diagonal.
- At most one queen on every anti-diagonal.

Exactly-One is decomposed as:

```text
ExactlyOne
=
AtLeastOne
+
AtMostOne
```

---

## Supported SAT Encodings

The current SAT implementation supports:

```text
pairwise
seqcounter
bitwise
```

All three encodings use the same N-Queens formulation and the same SAT solver, Glucose3.

This allows the impact of the AMO encoding itself to be studied while keeping the underlying SAT solver fixed.

### Pairwise Encoding

For every pair of literals `xi` and `xj`, Pairwise encoding generates:

```text
NOT xi OR NOT xj
```

or in CNF:

```python
[-xi, -xj]
```

Pairwise encoding introduces no auxiliary variables.

### Sequential Counter Encoding

Sequential Counter is implemented using PySAT:

```python
CardEnc.atmost(
    lits=variables,
    bound=1,
    vpool=vpool,
    encoding=EncType.seqcounter,
)
```

It introduces auxiliary variables representing sequential counter states.

### Bitwise Encoding

Bitwise encoding is implemented using:

```python
CardEnc.atmost(
    lits=variables,
    bound=1,
    vpool=vpool,
    encoding=EncType.bitwise,
)
```

It introduces auxiliary variables representing binary selectors.

---

## Auxiliary SAT Variables

Original board variables occupy:

```text
1 ... N^2
```

A shared PySAT `IDPool` allocates auxiliary variables starting after the original board variables:

```python
vpool = IDPool(
    start_from=n * n + 1
)
```

The same pool is shared across all encoded constraints in an instance.

This prevents auxiliary-variable collisions.

---

## SAT Solving Pipeline

```text
N-Queens instance
        |
        v
Generate board variables
        |
        v
Generate N-Queens constraints
        |
        v
Selected AMO encoding
   /        |        \
Pairwise  SeqCounter  Bitwise
        |
        v
       CNF
        |
        v
    Glucose3
        |
        v
    SAT / UNSAT
        |
        v
 Decode solution
        |
        v
Independent validator
```

---

## CP / CP-SAT Formulation

Both OR-Tools CP-SAT and CPLEX CP use `N` integer variables:

```text
queens[row] = column
```

Three `AllDifferent` constraint families are applied:

```text
AllDifferent(queens)
AllDifferent(queens[row] + row)
AllDifferent(queens[row] - row)
```

They prevent queens from sharing:

- Columns
- Main diagonals
- Anti-diagonals

This provides a compact high-level model without explicitly constructing `N^2` board variables.

---

## MIP Formulation

Both CPLEX MIP and Gurobi MIP use binary board variables:

```text
x[row, col] ∈ {0, 1}
```

### Row Constraints

```text
sum(x[row, col]) = 1
```

for every row.

### Column Constraints

```text
sum(x[row, col]) = 1
```

for every column.

### Main Diagonal Constraints

```text
sum(x[row, col]) <= 1
```

for positions having the same:

```text
row - col
```

### Anti-Diagonal Constraints

```text
sum(x[row, col]) <= 1
```

for positions having the same:

```text
row + col
```

For `N >= 2`, the formulation contains:

```text
N^2
```

binary variables and:

```text
6N - 6
```

linear constraints.

For example, with `N = 8`:

```text
Variables   : 64
Constraints : 42
```

---

## Implemented Solvers

### PySAT + Glucose3

Supported SAT encodings:

```text
pairwise
seqcounter
bitwise
```

Example:

```powershell
python -m src.sat.solver --n 8 --encoding pairwise --show-board
```

### OR-Tools CP-SAT

```powershell
python -m src.cp_sat.solver --n 8 --show-board
```

### CPLEX CP Optimizer

```powershell
python -m src.cp.cplex_cp --n 8 --show-board
```

### CPLEX MIP

```powershell
python -m src.mip.cplex_mip --n 8 --show-board
```

### Gurobi MIP

```powershell
python -m src.mip.gurobi_mip --n 8 --show-board
```

---

## Shared Solution Validation

Every solver returns solutions in the common form:

```text
queens[row] = column
```

All satisfiable solutions are validated independently using the same validator.

The validator checks that:

- Exactly one queen exists in every row.
- No two queens occupy the same column.
- No two queens share a main diagonal.
- No two queens share an anti-diagonal.

This keeps solver correctness verification independent from the model implementation.

---

## Performance Measurements

### SAT

The SAT implementation records:

```text
encoding_time
solve_time
total_time
num_variables
num_clauses
```

### CP / CP-SAT

The CP-based implementations record:

```text
build_time
solve_time
total_time
```

OR-Tools CP-SAT additionally records:

```text
num_conflicts
num_branches
```

### MIP

The MIP implementations record:

```text
build_time
solve_time
total_time
num_variables
num_constraints
```

---

## Benchmark Infrastructure

A unified benchmark runner is implemented under:

```text
experiments/
```

The benchmark layer provides a common interface over all solving methods.

Supported methods:

```text
sat
cp_sat
cplex_cp
cplex_mip
gurobi_mip
```

The benchmark runner normalizes solver-specific outputs into a shared result schema.

Each row can contain:

```text
experiment
run
n
method
solver
encoding
status
valid
num_variables
num_clauses
num_constraints
encoding_time
build_time
solve_time
total_time
raw_status
error_type
error_message
```

---

## Benchmark Experiments

### SAT Encoding Experiment

Run:

```powershell
python -m experiments.benchmark `
    --experiment sat-encodings `
    --sizes 4 8 16 `
    --repeats 1
```

This compares:

```text
Pairwise
Sequential Counter
Bitwise
```

while keeping:

```text
SAT solver = Glucose3
```

fixed.

The default result file is:

```text
results/sat_encoding_results.csv
```

### Solver Comparison Experiment

Run:

```powershell
python -m experiments.benchmark `
    --experiment solvers `
    --sizes 4 8 16 `
    --repeats 1 `
    --sat-encoding seqcounter
```

This compares:

```text
SAT + Glucose3
OR-Tools CP-SAT
CPLEX CP
CPLEX MIP
Gurobi MIP
```

The default result file is:

```text
results/solver_comparison_results.csv
```

### Custom Output

A custom output file can also be specified:

```powershell
python -m experiments.benchmark `
    --experiment solvers `
    --sizes 4 8 `
    --output results/custom_results.csv
```

### Existing Pilot Results

Pilot and smoke-test results are already available in the repository:

```text
results/day12_sat_smoke.csv
results/day12_solver_smoke.csv
results/day12_license_test.csv
results/pilot/sat_encodings_round1.csv
results/pilot/sat_encodings_round2.csv
results/pilot/solver_comparison_round1.csv
results/pilot/solver_comparison_n32.csv
results/pilot/solver_comparison_license_boundary.csv
results/pilot/solver_comparison_large.csv
results/final_sat_encodings_small.csv
results/final_sat_encodings_n64.csv
results/final_solver_comparison_core.csv
results/final_solver_comparison_extended.csv
```

The current pilot coverage is:

- SAT encoding comparison at `N = 8, 16, 32, 64, 96, 128`.
- Cross-solver comparison at `N = 8, 16, 24, 31, 32, 44, 45, 64, 100, 128`.
- Repeated and smoke-test runs at smaller board sizes.
- License-boundary cases where failed solver runs are recorded as `LICENSE_LIMIT` instead of stopping the experiment.

These files are pilot data, not yet the final statistical benchmark. Final sizes, repetition counts, timeout policy, and the baseline SAT encoding still need to be selected after analysis.

The first analysis artifacts are available in `report/`:

```text
report/pilot_analysis.md
report/sat_encodings_summary.csv
report/solver_comparison_summary.csv
report/benchmark_summary.csv
report/sat_encoding_runtime.svg
report/solver_runtime.svg
```

The current analysis confirms that the solver implementation and benchmark pipeline are functional, but the SAT encoding baseline should not be finalized from a single large-instance run because the observed solving time varies substantially across runs and board sizes.

---

## Benchmark Error Handling

A failed solver run does not terminate the full experiment.

Errors are normalized into benchmark results containing:

```text
status
error_type
error_message
```

Known license-related failures are classified as:

```text
LICENSE_LIMIT
```

This allows remaining solver configurations to continue running.

For example, the currently installed CPLEX Community Edition cannot solve the `N = 32` MIP instance because the model contains:

```text
1024 variables
```

which exceeds the current license limit.

The benchmark runner records this failure instead of terminating the experiment.

---

## Current License Notes

### CPLEX

The currently installed CPLEX Community Edition has a model-size restriction.

The current MIP formulation can run successfully through:

```text
N = 31
```

with:

```text
31^2 = 961 variables
```

while `N = 32` contains:

```text
1024 variables
```

and exceeds the current license limit.

An unrestricted academic license is preferred before final large-scale MIP experiments.

### Gurobi

Gurobi is currently functional using a restricted non-production license.

The current license successfully solves the tested `N = 32` model:

```text
Variables   : 1024
Constraints : 186
```

The same restricted license rejects larger tested models such as `N = 64`. An Academic License should be activated before final large-scale benchmark experiments.

---

## Project Structure

```text
n-queens-solving/
│
├── scripts/
│   └── check_env.py
│
├── src/
│   ├── common/
│   │   ├── __init__.py
│   │   └── validator.py
│   │
│   ├── sat/
│   │   ├── __init__.py
│   │   ├── encoder.py
│   │   └── solver.py
│   │
│   ├── cp_sat/
│   │   ├── __init__.py
│   │   └── solver.py
│   │
│   ├── cp/
│   │   ├── __init__.py
│   │   └── cplex_cp.py
│   │
│   └── mip/
│       ├── __init__.py
│       ├── cplex_mip.py
│       └── gurobi_mip.py
│
├── experiments/
│   ├── __init__.py
│   ├── config.py
│   ├── runner.py
│   └── benchmark.py
│
├── results/
├── report/
│
├── tests/
│   ├── test_sat_encodings.py
│   ├── test_cp_solvers.py
│   ├── test_mip_solvers.py
│   └── test_benchmark.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Environment Setup

The project uses Python 3.11.

Create a virtual environment:

```powershell
py -3.11 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Environment Check

Run:

```powershell
python scripts/check_env.py
```

Expected components:

```text
[OK] PySAT + Glucose3
[OK] OR-Tools CP-SAT
[OK] Gurobi
[OK] CPLEX MIP
[OK] CPLEX CP Optimizer
```

---

## Testing

Run the complete test suite with:

```powershell
python -m pytest -q
```

The current test suite verifies:

- `N = 1` is satisfiable.
- `N = 2` is unsatisfiable.
- `N = 3` is unsatisfiable.
- `N = 4` is satisfiable.
- `N = 8` is satisfiable.
- Returned solutions pass the shared independent validator.
- Pairwise encoding behaves correctly.
- Sequential Counter encoding behaves correctly.
- Bitwise encoding behaves correctly.
- Pairwise CNF regression values remain unchanged.
- OR-Tools CP-SAT behaves correctly.
- CPLEX CP behaves correctly.
- CPLEX MIP behaves correctly.
- Gurobi MIP behaves correctly.
- MIP model-size regression values are correct.
- Benchmark result normalization works correctly.
- SAT encoding experiments execute through the unified runner.
- Cross-method solver experiments execute through the unified runner.

---

## Experimental Plan

### Experiment A — SAT Encoding Comparison

Keep the SAT solver fixed:

```text
Glucose3
```

Compare:

```text
Pairwise
Sequential Counter
Bitwise
```

Metrics:

```text
Number of variables
Number of clauses
Encoding time
Solving time
Total time
```

### Experiment B — Solving Paradigm Comparison

Select one SAT encoding based on Experiment A, then compare:

```text
SAT + Glucose3
CPLEX CP
OR-Tools CP-SAT
CPLEX MIP
Gurobi MIP
```

Metrics include:

```text
Build/encoding time
Solving time
Total time
Maximum practical board size
Solver status
```

### Agreed Initial Experimental Protocol

The following protocol is used for the current local-laptop phase and can be revised after license activation:

```text
SAT encoding experiment sizes : 8, 16, 32, 64, 96, 128
Cross-solver core sizes       : 8, 16, 24, 31, 32
Cross-solver extended sizes   : 44, 45, 64, 100, 128
Repeats for N <= 32           : 5
Repeats for N = 64            : 3
Repeats for N >= 96           : 1 initially
Per-run timeout               : 600 seconds
Cross-solver SAT encoding     : bitwise candidate baseline
```

The `bitwise` encoding is the current candidate baseline because the pilot results show better scalability at `N = 128` than `seqcounter`. The final choice will be justified using the completed SAT-encoding comparison rather than assumed in advance.

When a solver cannot run because of the local license, the result remains in the CSV with `status = LICENSE_LIMIT`. When a solver exceeds the time limit, the result will be recorded with `status = TIMEOUT`. Neither outcome should terminate the remaining benchmark configurations.

---

## Next Milestone

The solver implementations, validation layer, automated tests, benchmark infrastructure, pilot experiments, and first analysis artifacts are complete. The project is now in the **final benchmark and report-writing phase**.

The next milestone is to finalize the SAT baseline, repeat the cross-solver benchmark after license activation when possible, and incorporate the analysis into the scientific report.

The existing pilot runs cover candidate board sizes such as:

```text
8
16
32
64
100
128
```

The purpose is to determine:

- Which methods remain practical as `N` increases.
- Where SAT encoding size begins to grow significantly.
- Which solvers become slow or encounter resource limits.
- Which final board sizes should be used in the official experiments.
- Whether explicit solver time limits are necessary.
- Which SAT encoding should be used as the candidate baseline for the later cross-method comparison.

The remaining workflow is:

```text
Final SAT encoding experiments
        ↓
Final solver comparison experiments
        ↓
Result analysis
        ↓
Tables and figures
        ↓
Scientific report
```
