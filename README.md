# N-Queens Solving: SAT Encoding and Exact Methods

This project studies the **N-Queens problem** using SAT solving and other exact optimization methods.

The project is developed for **Assignment 1 – Modern Problems in Computer Science** and focuses on comparing different SAT cardinality encodings and exact solving approaches such as Constraint Programming, CP-SAT, and Mixed Integer Programming.

## Project Objectives

The main objectives are:

- Model the N-Queens problem as a SAT problem.
- Implement and compare different SAT At-Most-One encodings.
- Solve SAT instances using solvers provided by PySAT.
- Compare SAT solving with:
  - OR-Tools CP-SAT
  - CPLEX CP Optimizer
  - CPLEX MIP
  - Gurobi MIP
- Evaluate solving performance on increasingly large board sizes.
- Analyze the effect of SAT encodings on:
  - Number of variables
  - Number of clauses
  - Encoding time
  - Solving time
  - Total execution time

---

## Current Progress

### Completed

- [x] Project structure initialized.
- [x] Python virtual environment configured.
- [x] PySAT + Glucose3 environment verified.
- [x] OR-Tools CP-SAT environment verified.
- [x] Gurobi environment verified.
- [x] CPLEX MIP environment verified.
- [x] CPLEX CP Optimizer environment verified.
- [x] Generic SAT encoder implemented.
- [x] Pairwise AMO encoding implemented.
- [x] Sequential Counter AMO encoding integrated using PySAT.
- [x] Bitwise AMO encoding integrated using PySAT.
- [x] Shared auxiliary-variable management implemented using `IDPool`.
- [x] N-Queens SAT solver implemented using Glucose3.
- [x] Command-line selection of SAT encoding implemented.
- [x] SAT model decoding implemented.
- [x] Independent solution validator implemented.
- [x] Encoding, solving, and total execution times recorded separately.
- [x] Automated tests implemented for all supported SAT encodings.
- [x] SAT and UNSAT behavior verified for representative N-Queens instances.

### Planned

- [ ] Implement OR-Tools CP-SAT solver.
- [ ] Implement CPLEX CP solver.
- [ ] Implement CPLEX MIP solver.
- [ ] Implement Gurobi MIP solver.
- [ ] Build unified benchmark pipeline.
- [ ] Compare SAT encodings experimentally.
- [ ] Compare SAT, CP, CP-SAT, and MIP approaches.
- [ ] Run experiments on large N-Queens instances.
- [ ] Generate experimental tables and figures.
- [ ] Prepare the final scientific report.

---

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

Each board position is mapped to a positive SAT variable identifier using:

```text
variable_id = row * N + col + 1
```

Therefore, the original N-Queens formulation contains:

```text
N^2
```

board variables.

Additional auxiliary variables may be introduced depending on the selected SAT encoding.

---

## N-Queens Constraints

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

### Main Diagonal Constraints

Each main diagonal contains at most one queen.

Board positions belong to the same main diagonal when:

```text
row - col = constant
```

### Anti-Diagonal Constraints

Each anti-diagonal contains at most one queen.

Board positions belong to the same anti-diagonal when:

```text
row + col = constant
```

---

# SAT Encodings

The current implementation supports three At-Most-One encodings:

```text
pairwise
seqcounter
bitwise
```

All encodings use the same N-Queens formulation and the same SAT solver, **Glucose3**, allowing their CNF representations and solving performance to be compared under the same conditions.

---

## Pairwise Encoding

Pairwise encoding generates one binary clause for every pair of variables participating in an At-Most-One constraint.

For every pair:

```text
xi, xj
```

the following clause is generated:

```text
NOT xi OR NOT xj
```

In CNF representation:

```python
[-xi, -xj]
```

Pairwise encoding does not require auxiliary variables.

Its AMO representation grows approximately quadratically with the number of literals in a constraint:

```text
O(k^2)
```

where `k` is the number of literals.

---

## Sequential Counter Encoding

Sequential Counter encoding is implemented using PySAT's cardinality encoding utilities.

The encoding introduces auxiliary variables that represent intermediate states of a sequential counter.

Compared with Pairwise encoding, Sequential Counter can significantly reduce the number of clauses required for large At-Most-One constraints.

The implementation uses:

```python
CardEnc.atmost(
    lits=variables,
    bound=1,
    vpool=vpool,
    encoding=EncType.seqcounter,
)
```

---

## Bitwise Encoding

Bitwise encoding is also implemented using PySAT.

It introduces auxiliary variables that encode the identity of the selected literal using a binary representation.

The implementation uses:

```python
CardEnc.atmost(
    lits=variables,
    bound=1,
    vpool=vpool,
    encoding=EncType.bitwise,
)
```

Bitwise encoding provides another trade-off between the number of auxiliary variables and the number of generated clauses.

---

# Auxiliary Variable Management

Sequential Counter and Bitwise encodings introduce additional SAT variables.

To prevent different constraints from accidentally reusing the same auxiliary variable identifiers, the project uses a shared PySAT `IDPool`.

Original board variables occupy:

```text
1 ... N^2
```

while auxiliary variables begin after the original board variables:

```python
vpool = IDPool(
    start_from=n * n + 1
)
```

The same variable pool is shared across all encoded constraints of a single N-Queens instance.

---

# SAT Solving Pipeline

The current SAT solving pipeline is:

```text
N
│
▼
Generate board variables
│
▼
Generate N-Queens constraints
│
├── Row Exactly-One
├── Column Exactly-One
├── Main-diagonal At-Most-One
└── Anti-diagonal At-Most-One
│
▼
Selected AMO Encoding
│
├── Pairwise
├── Sequential Counter
└── Bitwise
│
▼
CNF
│
▼
Glucose3
│
▼
SAT / UNSAT
│
▼
Decode SAT model
│
▼
Independent solution validation
```

---

# Performance Measurements

The SAT solver records three timing measurements.

### Encoding Time

Time required to transform the N-Queens instance into CNF:

```text
encoding_time
```

### Solving Time

Time required by Glucose3 to solve the generated CNF:

```text
solve_time
```

### Total Time

Combined encoding and solving time:

```text
total_time
=
encoding_time
+
solve_time
```

The solver also records:

```text
num_variables
num_clauses
```

These metrics will later be used for the experimental comparison of SAT encodings.

---

# Project Structure

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
│   └── test_sat_encodings.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# Environment Setup

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

# Check Solver Environment

Run:

```powershell
python scripts/check_env.py
```

Expected components:

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

## Gurobi License

Gurobi is currently functional with a restricted non-production license.

An Academic License will be activated before running large-scale benchmark experiments.

---

# Run the SAT Solver

The general command is:

```powershell
python -m src.sat.solver --n <N> --encoding <ENCODING>
```

Supported encodings are:

```text
pairwise
seqcounter
bitwise
```

---

## Pairwise Example

```powershell
python -m src.sat.solver --n 8 --encoding pairwise --show-board
```

Expected properties:

```text
Solver         : glucose3
Encoding       : pairwise
Status         : SAT
Variables      : 64
Clauses        : 744
Valid solution : True
```

---

## Sequential Counter Example

```powershell
python -m src.sat.solver --n 8 --encoding seqcounter --show-board
```

Expected behavior:

```text
Solver         : glucose3
Encoding       : seqcounter
Status         : SAT
Valid solution : True
```

Sequential Counter introduces auxiliary variables, so the total number of SAT variables is expected to be greater than `N^2`.

---

## Bitwise Example

```powershell
python -m src.sat.solver --n 8 --encoding bitwise --show-board
```

Expected behavior:

```text
Solver         : glucose3
Encoding       : bitwise
Status         : SAT
Valid solution : True
```

Bitwise encoding also introduces auxiliary variables.

---

# Known N-Queens Results

All currently supported SAT encodings correctly reproduce the standard satisfiability behavior:

|   N | Expected Result |
| --: | --------------- |
|   1 | SAT             |
|   2 | UNSAT           |
|   3 | UNSAT           |
|   4 | SAT             |
|   8 | SAT             |

The Pairwise baseline preserves the following CNF sizes.

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

These values are used as regression checks to ensure that later refactoring does not accidentally modify the original Pairwise encoding.

---

# Testing

Run the complete test suite with:

```powershell
python -m pytest -q
```

The current test suite verifies:

- SAT behavior for `N = 1`.
- UNSAT behavior for `N = 2`.
- UNSAT behavior for `N = 3`.
- SAT behavior for `N = 4`.
- SAT behavior for `N = 8`.
- Valid decoded solutions for satisfiable instances.
- Pairwise encoding correctness.
- Sequential Counter encoding correctness.
- Bitwise encoding correctness.
- Pairwise CNF variable and clause regression values.
- Rejection of unsupported encoding names.

---

# Current Experimental Design

The SAT encoding experiment will keep the SAT solver fixed:

```text
Glucose3
```

and vary only the At-Most-One encoding:

```text
Pairwise
Sequential Counter
Bitwise
```

The main comparison metrics will be:

```text
Number of variables
Number of clauses
Encoding time
Solving time
Total time
```

This design allows the effect of the SAT encoding itself to be evaluated independently from the choice of SAT solver.

---

# Next Milestone

The next milestone is to implement exact solving approaches outside SAT.

## Constraint Programming

Implement:

```text
CPLEX CP Optimizer
```

using an integer representation:

```text
queen[row] = column
```

with three `AllDifferent` constraint families.

## CP-SAT

Implement:

```text
OR-Tools CP-SAT
```

using the same high-level N-Queens formulation.

After these solvers are validated, the project will continue with:

```text
CPLEX MIP
Gurobi MIP
Unified benchmark runner
Large-instance experiments
Experimental figures and tables
```
