import pytest
from src.sat.solver import solve_nqueens

ENCODINGS = [
    "pairwise",
    "seqcounter",
    "bitwise",
]

@pytest.mark.parametrize("encoding", ENCODINGS)
def test_n1_sat(encoding):
    result = solve_nqueens(n=1, encoding=encoding)

    assert result["status"] == "SAT"
    assert result["valid"] is True


@pytest.mark.parametrize("encoding", ENCODINGS)
def test_n2_unsat(encoding):
    result = solve_nqueens(n=2, encoding=encoding)

    assert result["status"] == "UNSAT"


@pytest.mark.parametrize("encoding", ENCODINGS)
def test_n3_unsat(encoding):
    result = solve_nqueens(n=3, encoding=encoding)

    assert result["status"] == "UNSAT"


@pytest.mark.parametrize("encoding", ENCODINGS)
def test_n4_sat(encoding):
    result = solve_nqueens(n=4, encoding=encoding)

    assert result["status"] == "SAT"
    assert result["valid"] is True


@pytest.mark.parametrize("encoding", ENCODINGS)
def test_n8_sat(encoding):
    result = solve_nqueens(n=8, encoding=encoding)

    assert result["status"] == "SAT"
    assert result["valid"] is True


def test_pairwise_n4_cnf_size():
    result = solve_nqueens(n=4, encoding="pairwise")

    assert result["num_variables"] == 16
    assert result["num_clauses"] == 84

def test_pairwise_n8_cnf_size():
    result = solve_nqueens(n=8, encoding="pairwise")

    assert result["num_variables"] == 64
    assert result["num_clauses"] == 744

def test_invalid_encoding():
    with pytest.raises(ValueError, match="Unsupported encoding"):
        solve_nqueens(n=8, encoding="invalid")