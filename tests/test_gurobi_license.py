
import gurobipy as gp
from gurobipy import GRB

print("Gurobi version:", gp.gurobi.version())

model = gp.Model("academic_license_test")

# Exceed the restricted license's 2,000-variable limit
x = model.addVars(2100, vtype=GRB.BINARY, name="x")

model.addConstr(gp.quicksum(x.values()) >= 1000)
model.setObjective(
    gp.quicksum(x.values()),
    GRB.MINIMIZE,
)

model.update()
print("Variables:", model.NumVars)
print("Constraints:", model.NumConstrs)

model.optimize()

if model.Status == GRB.OPTIMAL:
    print("Objective:", model.ObjVal)
    print("GUROBI ACADEMIC: PASS")
else:
    print("Solver status:", model.Status)
    print("GUROBI ACADEMIC: NOT VERIFIED")
