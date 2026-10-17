
import cplex
from docplex.mp.model import Model

print("CPLEX version:", cplex.Cplex().get_version())

model = Model(name="academic_license_test")

# Create 1,100 binary decision variables
x = model.binary_var_list(1100, name="x")

model.add_constraint(model.sum(x) >= 10)
model.minimize(model.sum(x))

print("Variables:", model.number_of_variables)
print("Constraints:", model.number_of_constraints)

solution = model.solve(log_output=True)

if solution is not None:
    print("Objective:", solution.objective_value)
    print("CPLEX FULL VERSION: PASS")
else:
    print("Solve status:", model.solve_details.status)
    print("CPLEX FULL VERSION: NOT VERIFIED")
