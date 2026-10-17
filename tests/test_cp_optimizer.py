
import sys
from pathlib import Path

from docplex.cp.model import CpoModel

# N-Queens configuration
n = 8
model = CpoModel(name="n_queens")

# Each variable represents the row of a queen in one column
q = model.integer_var_list(n, 0, n - 1, "q")

# No two queens share a row
model.add(model.all_diff(q))

# No two queens share a diagonal
model.add(model.all_diff([q[i] + i for i in range(n)]))
model.add(model.all_diff([q[i] - i for i in range(n)]))

# Locate the CP Optimizer executable in the virtual environment
exe = Path(sys.prefix) / "Scripts" / "cpoptimizer.exe"

print("CP Optimizer executable:", exe)
assert exe.is_file(), f"CP Optimizer not found: {exe}"

# Solve the model
result = model.solve(
    execfile=str(exe),
    TimeLimit=30,
    LogVerbosity="Quiet",
)

print("Solve status:", result.get_solve_status())
print("Solution found:", result.is_solution())

if result.is_solution():
    print("Queen positions:", [result[v] for v in q])
    print("CP OPTIMIZER: PASS")
else:
    print("CP OPTIMIZER: NOT VERIFIED")
