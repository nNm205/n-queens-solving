from experiments.runner import (
    run_sat_encoding_experiment,
    run_solver,
    run_solver_comparison_experiment,
)

def test_normalized_sat_result():
    result = run_solver(
        experiment="test",
        run=1,
        method="sat",
        n=4,
        encoding="pairwise",
    )

    assert result["method"] == "sat"
    assert result["encoding"] == "pairwise"
    assert result["status"] == "SAT"
    assert result["valid"] is True
    assert result["num_variables"] == 16
    assert result["num_clauses"] == 84


def test_sat_encoding_experiment():
    results = run_sat_encoding_experiment(
        sizes=[4],
        repeats=1,
    )

    assert len(results) == 3

    assert {
        result["encoding"]
        for result in results
    } == {
        "pairwise",
        "seqcounter",
        "bitwise",
    }


def test_solver_comparison_experiment():
    results = run_solver_comparison_experiment(
        sizes=[4],
        repeats=1,
        sat_encoding="seqcounter",
    )

    assert len(results) == 5

    assert all(
        result["status"] == "SAT"
        for result in results
    )

    assert all(
        result["valid"] is True
        for result in results
    )