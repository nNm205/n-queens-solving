
import sys
from pathlib import Path
from docplex.cp.model import CpoModel

model = CpoModel(name="cp_license_test")

# 1,100 binary variables:
# The initial domain space is 2^1100.
x = model.binary_var_list(1100, name="x")

# Keep all variables in the model.
model.add(model.sum(x) == 550)

exe = Path(sys.prefix) / "Scripts" / "cpoptimizer.exe"

result = model.solve(
    execfile=str(exe),
    TimeLimit=20,
    LogVerbosity="Normal",
)

print("Solve status:", result.get_solve_status())
print("Solution found:", result.is_solution())

if result.is_solution():
    values = [result[v] for v in x]
    assert sum(values) == 550
    print("CP OPTIMIZER FULL VERSION: PASS")
else:
    print("CP OPTIMIZER FULL VERSION: NOT VERIFIED")
