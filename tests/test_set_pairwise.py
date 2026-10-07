from src.sat.solver import solve_nqueens

def test_n1_sat():
    result = solve_nqueens(1)

    assert result["status"] == "SAT"
    assert result["valid"] is True


def test_n2_unsat():
    result = solve_nqueens(2)

    assert result["status"] == "UNSAT"


def test_n3_unsat():
    result = solve_nqueens(3)

    assert result["status"] == "UNSAT"


def test_n4_sat():
    result = solve_nqueens(4)

    assert result["status"] == "SAT"
    assert result["valid"] is True

    assert result["num_variables"] == 16
    assert result["num_clauses"] == 84


def test_n8_sat():
    result = solve_nqueens(8)

    assert result["status"] == "SAT"
    assert result["valid"] is True

    assert result["num_variables"] == 64
    assert result["num_clauses"] == 744