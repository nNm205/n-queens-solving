# N-Queens Solving: SAT Encoding and Exact Methods

This project studies the **N-Queens problem** using SAT solving and other exact solving approaches.

The project is developed for **Assignment 1 – Modern Problems in Computer Science** and focuses on comparing SAT-based solving with Constraint Programming, CP-SAT, and Mixed Integer Programming.

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
  - Model/encoding time
  - Solving time
  - Total execution time

## Current Progress

### Completed

- [x] Project structure initialized.
- [x] Solver environment configured and verified.
- [x] PySAT + Glucose3 verified.
- [x] OR-Tools verified.
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
- [x] CP/CP-SAT model build and solving times recorded.
- [x] Automated tests covering SAT, CP-SAT, and CPLEX CP.

### Planned

- [ ] Activate Gurobi Academic License.
- [ ] Implement CPLEX MIP solver.
- [ ] Implement Gurobi MIP solver.
- [ ] Build unified benchmark runner.
- [ ] Run SAT encoding experiments.
- [ ] Run SAT vs CP vs CP-SAT vs MIP experiments.
- [ ] Run large-instance experiments.
- [ ] Generate result tables and figures.
- [ ] Prepare the final scientific report.

## N-Queens Representation

For the SAT formulation, each board position is represented by a Boolean variable:

```text
x[row, col]
```

The SAT variable identifier is:

```text
variable_id = row * N + col + 1
```

For CP and CP-SAT, the project uses:

```text
queens[row] = column
```

where each variable has domain:

```text
0 ... N - 1
```

This representation guarantees exactly one queen for each row.

The following constraints are then enforced:

```text
AllDifferent(queens)
AllDifferent(queens[row] + row)
AllDifferent(queens[row] - row)
```

These constraints prevent queens from sharing columns or diagonals.

## SAT Formulation

The SAT formulation contains:

- Exactly one queen in every row.
- Exactly one queen in every column.
- At most one queen on every main diagonal.
- At most one queen on every anti-diagonal.

Exactly-One is represented as:

```text
ExactlyOne
=
AtLeastOne
+
AtMostOne
```

## Supported SAT Encodings

The current SAT implementation supports:

```text
pairwise
seqcounter
bitwise
```

### Pairwise

Pairwise encoding generates:

```text
NOT xi OR NOT xj
```

for every pair of literals participating in an At-Most-One constraint.

It does not introduce auxiliary variables.

### Sequential Counter

Sequential Counter is implemented using PySAT:

```python
CardEnc.atmost(
    lits=variables,
    bound=1,
    vpool=vpool,
    encoding=EncType.seqcounter,
)
```

It introduces auxiliary counter variables.

### Bitwise

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

## Auxiliary SAT Variables

Original board variables occupy:

```text
1 ... N^2
```

A shared `IDPool` allocates auxiliary variables beginning after the board variables:

```python
vpool = IDPool(
    start_from=n * n + 1
)
```

This prevents auxiliary-variable collisions between independent cardinality constraints.

## SAT Solving Pipeline

```text
N-Queens instance
        |
        v
Generate Boolean variables
        |
        v
Generate N-Queens constraints
        |
        v
Selected AMO encoding
   /       |       \
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

## CP / CP-SAT Formulation

Both OR-Tools CP-SAT and CPLEX CP use `N` integer variables:

```text
queens[row] = column
```

Constraints:

```text
AllDifferent(queens)
AllDifferent(queens[row] + row)
AllDifferent(queens[row] - row)
```

This produces a compact high-level formulation without explicitly generating CNF clauses.

## Implemented Solvers

### PySAT + Glucose3

Supported encodings:

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

Run:

```powershell
python -m src.cp_sat.solver --n 8 --show-board
```

### CPLEX CP Optimizer

Run:

```powershell
python -m src.cp.cplex_cp --n 8 --show-board
```

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

CP-SAT additionally records:

```text
num_conflicts
num_branches
```

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
│
├── experiments/
├── results/
├── report/
│
├── tests/
│   ├── test_sat_encodings.py
│   └── test_cp_solvers.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

## Environment Setup

The project uses Python 3.11.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Environment Check

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

## Testing

Run:

```powershell
python -m pytest -q
```

The current tests verify:

- `N = 1` is satisfiable.
- `N = 2` is unsatisfiable.
- `N = 3` is unsatisfiable.
- `N = 4` is satisfiable.
- `N = 8` is satisfiable.
- Returned solutions pass an independent validator.
- Pairwise, Sequential Counter, and Bitwise encodings behave correctly.
- OR-Tools CP-SAT behaves correctly.
- CPLEX CP behaves correctly.
- Pairwise CNF regression values remain unchanged.

## Current Experimental Plan

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

Compare:

```text
SAT
CPLEX CP
OR-Tools CP-SAT
CPLEX MIP
Gurobi MIP
```

The main metric will be solving performance as the board size increases.

## Next Milestone

The next implementation milestone is:

```text
CPLEX MIP
Gurobi MIP
```

Both will use binary decision variables:

```text
x[row, col] ∈ {0, 1}
```

with row, column, and diagonal constraints.

After these solvers are complete, all solving methods will be integrated into a unified benchmark pipeline.
