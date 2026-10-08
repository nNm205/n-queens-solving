SAT_ENCODINGS = (
    "pairwise",
    "seqcounter",
    "bitwise",
)

SOLVER_METHODS = (
    "sat",
    "cp_sat",
    "cplex_cp",
    "cplex_mip",
    "gurobi_mip",
)

DEFAULT_SIZES = (
    4,
    8,
    16,
)

RESULT_FIELDS = [
    "experiment",
    "run",
    "n",
    "method",
    "solver",
    "encoding",
    "status",
    "valid",
    "num_variables",
    "num_clauses",
    "num_constraints",
    "encoding_time",
    "build_time",
    "solve_time",
    "total_time",
    "raw_status",
    "error_type",
    "error_message",
]