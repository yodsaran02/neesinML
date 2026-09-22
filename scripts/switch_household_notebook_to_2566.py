"""Restore the active household debt-analysis notebook to its B.E. 2566 source."""

from pathlib import Path
import subprocess

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "household_income_debt_analysis.ipynb"
NOTEBOOK_AT_2566 = "HEAD:household_income_debt_analysis.ipynb"

# These are the cells changed when the active source was switched to B.E. 2568.
RESTORE_CELL_IDS = {
    "1f87cb3a", "a56a7966", "c5fb14f5", "8eaa2d10", "974863f7", "a33f4282",
    "79c6405b", "c3077f2e", "ffd36eb1", "0eed0145", "b66ffafb", "4c001193",
    "thailand_debt_heatmap_markdown", "thailand_debt_heatmap_code",
}


def main() -> None:
    current = nbformat.read(NOTEBOOK_PATH, as_version=4)
    baseline_text = subprocess.check_output(
        ["git", "show", NOTEBOOK_AT_2566], cwd=ROOT, text=True
    )
    baseline = nbformat.reads(baseline_text, as_version=4)

    current_cells = {cell["id"]: cell for cell in current.cells}
    baseline_cells = {cell["id"]: cell for cell in baseline.cells}
    missing = RESTORE_CELL_IDS.difference(current_cells) | RESTORE_CELL_IDS.difference(baseline_cells)
    if missing:
        raise ValueError(f"Notebook layout changed; expected cells are missing: {sorted(missing)}")

    for cell_id in RESTORE_CELL_IDS:
        current_cells[cell_id]["source"] = baseline_cells[cell_id]["source"]

    # Avoid the optional SciPy dependency used by pandas for method='spearman'.
    correlation_cell = current_cells["c3077f2e"]
    correlation_cell["source"] = correlation_cell["source"].replace(
        "spearman_r = wide[relationship_cols].corr(method='spearman').iloc[0, 1]",
        "spearman_r = wide[relationship_cols].rank().corr(method='pearson').iloc[0, 1]",
    )

    for cell in current.cells:
        if cell.cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            cell.get("metadata", {}).pop("execution", None)

    nbformat.write(current, NOTEBOOK_PATH)
    print(f"Restored B.E. 2566 source: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
