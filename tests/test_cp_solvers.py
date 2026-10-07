import pytest
from src.cp.cplex_cp import solve_nqueens_cplex_cp
from src.cp_sat.solver import solve_nqueens_cp_sat

SOLVERS = [
    solve_nqueens_cp_sat,
    solve_nqueens_cplex_cp,
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