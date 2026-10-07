def check_pysat():
    from pysat.solvers import Glucose3

    with Glucose3(bootstrap_with=[[1]]) as solver:
        assert solver.solve()

    print("[OK] PySAT + Glucose3")


def check_ortools():
    from ortools.sat.python import cp_model

    model = cp_model.CpModel()
    x = model.new_bool_var("x")
    model.add(x == 1)

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    assert status in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE,
    )

    print("[OK] OR-Tools CP-SAT")


def check_gurobi():
    import gurobipy as gp
    from gurobipy import GRB

    model = gp.Model("environment_test")
    model.Params.OutputFlag = 0

    x = model.addVar(vtype=GRB.BINARY, name="x")
    model.setObjective(x, GRB.MAXIMIZE)

    model.optimize()

    assert model.Status == GRB.OPTIMAL
    assert round(x.X) == 1

    print("[OK] Gurobi")


def check_cplex_mip():
    from docplex.mp.model import Model

    model = Model(name="environment_test")

    x = model.binary_var(name="x")
    model.maximize(x)

    solution = model.solve(log_output=False)

    assert solution is not None
    assert round(solution[x]) == 1

    print("[OK] CPLEX MIP")


def check_cplex_cp():
    from docplex.cp.model import CpoModel

    model = CpoModel()

    x = model.integer_var(min=0, max=1, name="x")
    model.add(x == 1)

    solution = model.solve(LogVerbosity="Quiet")

    assert solution is not None
    assert solution.is_solution()

    print("[OK] CPLEX CP Optimizer")


def run_check(name, fn):
    try:
        fn()
    except Exception as e:
        print(f"[FAIL] {name}")
        print(f"       {type(e).__name__}: {e}")


if __name__ == "__main__":
    checks = [
        ("PySAT", check_pysat),
        ("OR-Tools", check_ortools),
        ("Gurobi", check_gurobi),
        ("CPLEX MIP", check_cplex_mip),
        ("CPLEX CP", check_cplex_cp),
    ]

    print("=" * 50)
    print("N-QUEENS ENVIRONMENT CHECK")
    print("=" * 50)

    for name, fn in checks:
        run_check(name, fn)