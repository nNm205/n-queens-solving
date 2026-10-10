"""Create lightweight benchmark tables and SVG figures using only the stdlib."""

from __future__ import annotations

import csv
import html
import math
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "report"


def read_rows(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        with path.open(encoding="utf-8", newline="") as file:
            rows.extend(csv.DictReader(file))
    return rows


def number(value: str | None) -> float | None:
    if value in (None, "", "None"):
        return None
    return float(value)


def aggregate(rows: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str, str, str], list[dict]] = {}
    for row in rows:
        key = (
            row["experiment"],
            row["method"],
            row["n"],
            row.get("encoding") or "",
        )
        groups.setdefault(key, []).append(row)

    output = []
    for (experiment, method, n, encoding), group in sorted(
        groups.items(), key=lambda item: (item[0][0], int(item[0][2]), item[0][1], item[0][3])
    ):
        times = [number(row.get("total_time")) for row in group]
        times = [value for value in times if value is not None]
        output.append(
            {
                "experiment": experiment,
                "method": method,
                "n": int(n),
                "encoding": encoding,
                "runs": len(group),
                "sat_runs": sum(row.get("status") == "SAT" for row in group),
                "license_limit_runs": sum(
                    row.get("status") == "LICENSE_LIMIT" for row in group
                ),
                "timeout_runs": sum(row.get("status") == "TIMEOUT" for row in group),
                "median_total_time": median(times) if times else "",
                "min_total_time": min(times) if times else "",
                "max_total_time": max(times) if times else "",
            }
        )
    return output


def write_summary(rows: list[dict]) -> None:
    fields = list(rows[0]) if rows else []
    with (REPORT_DIR / "benchmark_summary.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    for experiment in ("sat_encodings", "solver_comparison"):
        experiment_rows = [row for row in rows if row["experiment"] == experiment]
        with (REPORT_DIR / f"{experiment}_summary.csv").open(
            "w", encoding="utf-8", newline=""
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(experiment_rows)


def chart(
    rows: list[dict],
    *,
    title: str,
    output: Path,
    series_keys: list[tuple[str, str]],
) -> None:
    width, height = 1100, 650
    left, right, top, bottom = 100, 40, 75, 100
    plot_width = width - left - right
    plot_height = height - top - bottom
    values = [
        float(row["median_total_time"])
        for row in rows
        if row["median_total_time"] not in ("", None)
    ]
    if not values:
        return

    y_min, y_max = -3.0, math.ceil(math.log10(max(values)))
    ns = sorted({int(row["n"]) for row in rows})
    x_positions = {
        n: left + index * plot_width / max(1, len(ns) - 1)
        for index, n in enumerate(ns)
    }

    def y_position(value: float) -> float:
        log_value = math.log10(max(value, 0.001))
        return top + (y_max - log_value) * plot_height / (y_max - y_min)

    colors = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#ea580c"]
    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="35" text-anchor="middle" font-size="22" font-family="Arial">{html.escape(title)}</text>',
        f'<text x="20" y="{top + plot_height / 2}" transform="rotate(-90 20 {top + plot_height / 2})" text-anchor="middle" font-size="14" font-family="Arial">Median total time (seconds, log scale)</text>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#333"/>',
        f'<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#333"/>',
    ]

    for exponent in range(math.floor(y_min), y_max + 1):
        y = y_position(10**exponent)
        svg.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="#e5e7eb"/>')
        svg.append(f'<text x="{left - 10}" y="{y + 5:.1f}" text-anchor="end" font-size="12" font-family="Arial">10^{exponent}</text>')

    for n, x in x_positions.items():
        svg.append(f'<text x="{x:.1f}" y="{top + plot_height + 25}" text-anchor="middle" font-size="12" font-family="Arial">{n}</text>')

    for index, (series_name, encoding) in enumerate(series_keys):
        points = []
        for row in rows:
            if row["method"] != series_name or row["encoding"] != encoding:
                continue
            if row["median_total_time"] in ("", None):
                continue
            points.append((x_positions[int(row["n"])], y_position(float(row["median_total_time"]))))
        if not points:
            continue
        color = colors[index % len(colors)]
        svg.append(''.join([f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="3"/>']))
        for x, y in points:
            svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>')
        legend_x = left + index * 180
        svg.append(f'<line x1="{legend_x}" y1="{height - 35}" x2="{legend_x + 25}" y2="{height - 35}" stroke="{color}" stroke-width="3"/>')
        svg.append(f'<text x="{legend_x + 32}" y="{height - 30}" font-size="13" font-family="Arial">{html.escape(series_name + ("/" + encoding if encoding else ""))}</text>')

    svg.append('</svg>')
    output.write_text("\n".join(svg), encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    sat_rows = read_rows([
        ROOT / "results/final_sat_encodings_small.csv",
        ROOT / "results/final_sat_encodings_n64.csv",
    ])
    solver_rows = read_rows([
        ROOT / "results/final_solver_comparison_core.csv",
        ROOT / "results/final_solver_comparison_extended.csv",
    ])
    summary = aggregate(sat_rows + solver_rows)
    write_summary(summary)

    chart(
        [row for row in summary if row["experiment"] == "sat_encodings"],
        title="SAT encoding comparison",
        output=REPORT_DIR / "sat_encoding_runtime.svg",
        series_keys=[("sat", encoding) for encoding in ("pairwise", "seqcounter", "bitwise")],
    )
    chart(
        [row for row in summary if row["experiment"] == "solver_comparison"],
        title="Cross-solver comparison",
        output=REPORT_DIR / "solver_runtime.svg",
        series_keys=[
            ("sat", "bitwise"),
            ("cp_sat", ""),
            ("cplex_cp", ""),
            ("cplex_mip", ""),
            ("gurobi_mip", ""),
        ],
    )
    print(f"[DONE] Wrote analysis artifacts to {REPORT_DIR}")


if __name__ == "__main__":
    main()
