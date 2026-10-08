import pytest
from src.mip.cplex_mip import solve_nqueens_cplex_mip
from src.mip.gurobi_mip import solve_nqueens_gurobi_mip

SOLVERS = [
    solve_nqueens_cplex_mip,
    solve_nqueens_gurobi_mip,
]

@pytest.mark.parametrize("solver", SOLVERS)
def test_n1_sat(solver):
    result = solver(1)

    assert result["status"] == "SAT"
    assert result["valid"] is True


@pytest.mark.parametrize("solver", SOLVERS)
def test_n2_unsat(solver):
    result = solver(2)

    assert result["status"] == "UNSAT"


@pytest.mark.parametrize("solver", SOLVERS)
def test_n3_unsat(solver):
    result = solver(3)

    assert result["status"] == "UNSAT"


@pytest.mark.parametrize("solver", SOLVERS)
def test_n4_sat(solver):
    result = solver(4)

    assert result["status"] == "SAT"
    assert result["valid"] is True


@pytest.mark.parametrize("solver", SOLVERS)
def test_n8_sat(solver):
    result = solver(8)

    assert result["status"] == "SAT"
    assert result["valid"] is True


@pytest.mark.parametrize("solver", SOLVERS)
def test_n8_model_size(solver):
    result = solver(8)

    assert result["num_variables"] == 64
    assert result["num_constraints"] > 0