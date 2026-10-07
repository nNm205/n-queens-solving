# N-Queens Solving: SAT Encoding and Exact Methods

This project studies the **N-Queens problem** using SAT solving and other exact optimization methods.

The project is developed for **Assignment 1 – Modern Problems in Computer Science** and focuses on comparing SAT-based solving with Constraint Programming, CP-SAT, and Mixed Integer Programming approaches.

## Project Objectives

The main objectives are:

- Model the N-Queens problem as a SAT problem.
- Implement different SAT cardinality encodings.
- Solve SAT instances using solvers provided by PySAT.
- Compare SAT solving with:
  - OR-Tools CP-SAT
  - CPLEX CP Optimizer
  - CPLEX MIP
  - Gurobi MIP
- Evaluate solving performance on increasingly large board sizes.
- Analyze the effect of different SAT encodings on:
  - Number of variables
  - Number of clauses
  - Solving time

## Current Progress

### Completed

- [x] Project structure initialized.
- [x] Python virtual environment configured.
- [x] PySAT + Glucose3 environment verified.
- [x] OR-Tools CP-SAT environment verified.
- [x] Gurobi environment verified.
- [x] CPLEX MIP environment verified.
- [x] CPLEX CP Optimizer environment verified.
- [x] Pairwise SAT encoding implemented.
- [x] N-Queens SAT solver implemented using Glucose3.
- [x] SAT model decoding implemented.
- [x] Independent solution validator implemented.
- [x] Command-line interface implemented.
- [x] Unit tests implemented for `N = 1, 2, 3, 4, 8`.

### Planned

- [ ] Implement Sequential Counter encoding.
- [ ] Implement Bitwise encoding.
- [ ] Compare SAT encodings.
- [ ] Implement OR-Tools CP-SAT solver.
- [ ] Implement CPLEX CP solver.
- [ ] Implement CPLEX MIP solver.
- [ ] Implement Gurobi MIP solver.
- [ ] Build unified benchmark pipeline.
- [ ] Run experiments on large N-Queens instances.
- [ ] Generate experimental tables and figures.
- [ ] Prepare the final scientific report.

## SAT Formulation

For an `N x N` chessboard, each board position is represented by a Boolean variable:

```text
x[row, col]
```

where:

```text
x[row, col] = True
```

means that a queen is placed at position `(row, col)`.

The board position is mapped to a SAT variable identifier using:

```text
variable_id = row * N + col + 1
```

The SAT formulation contains the following constraints.

### Row Constraints

Each row must contain exactly one queen.

```text
ExactlyOne(row)
=
AtLeastOne(row)
+
AtMostOne(row)
```

### Column Constraints

Each column must contain exactly one queen.

```text
ExactlyOne(column)
```

### Diagonal Constraints

Each main diagonal contains at most one queen.

Board positions on the same main diagonal satisfy:

```text
row - col = constant
```

Each anti-diagonal also contains at most one queen.

Board positions on the same anti-diagonal satisfy:

```text
row + col = constant
```

## Pairwise Encoding

The current implementation uses **Pairwise Encoding** for At-Most-One constraints.

For every pair of variables:

```text
xi, xj
```

the following clause is generated:

```text
NOT xi OR NOT xj
```

In CNF form:

```python
[-xi, -xj]
```

This prevents two variables in the same constraint group from being true simultaneously.

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
│   ├── cp/
│   ├── cp_sat/
│   └── mip/
│
├── experiments/
├── results/
├── report/
│
├── tests/
│   └── test_sat_pairwise.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

## Environment Setup

The project currently uses Python 3.11.

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

## Check Solver Environment

Run:

```powershell
python scripts/check_env.py
```

The expected output is similar to:

```text
==================================================
N-QUEENS ENVIRONMENT CHECK
==================================================
[OK] PySAT + Glucose3
[OK] OR-Tools CP-SAT
[OK] Gurobi
[OK] CPLEX MIP
[OK] CPLEX CP Optimizer
```

### Gurobi License

Gurobi is currently functional with a restricted non-production license.

An Academic License will be activated before running large-scale benchmark experiments.

## Run the SAT Solver

Solve the 8-Queens problem:

```powershell
python -m src.sat.solver --n 8
```

Display the resulting chessboard:

```powershell
python -m src.sat.solver --n 8 --show-board
```

Example output:

```text
==================================================
N-QUEENS SAT SOLVER
==================================================
N              : 8
Solver         : glucose3
Encoding       : pairwise
Status         : SAT
Variables      : 64
Clauses        : 744
Valid solution : True
Queen columns  : [3, 1, 6, 2, 5, 7, 4, 0]
```

Example board:

```text
. . . Q . . . .
. Q . . . . . .
. . . . . . Q .
. . Q . . . . .
. . . . . Q . .
. . . . . . . Q
. . . . Q . . .
Q . . . . . . .
```

## Known SAT Results

The current solver correctly produces:

|   N | Expected Result |
| --: | --------------- |
|   1 | SAT             |
|   2 | UNSAT           |
|   3 | UNSAT           |
|   4 | SAT             |
|   8 | SAT             |

For `N = 4`:

```text
Variables : 16
Clauses   : 84
```

For `N = 8`:

```text
Variables : 64
Clauses   : 744
```

## Testing

Run all unit tests with:

```powershell
python -m pytest -q
```

Current result:

```text
5 passed
```

The test suite verifies:

- `N = 1` is SAT.
- `N = 2` is UNSAT.
- `N = 3` is UNSAT.
- `N = 4` is SAT and produces a valid solution.
- `N = 8` is SAT and produces a valid solution.
- Expected CNF variable and clause counts are preserved for the current Pairwise encoding.

## Next Milestone

The next development milestone is to extend the SAT implementation with additional cardinality encodings:

1. Sequential Counter
2. Bitwise
3. Pairwise baseline comparison

After that, the project will implement:

- OR-Tools CP-SAT
- CPLEX CP
- CPLEX MIP
- Gurobi MIP

These implementations will later be integrated into a unified experimental benchmark.
