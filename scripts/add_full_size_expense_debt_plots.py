"""Add one full-size expense-versus-debt plot for each socioeconomic group."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "household_income_debt_analysis.ipynb"
MARKDOWN_ID = "expense_debt_full_size_markdown"
CODE_ID = "expense_debt_full_size_code"

MARKDOWN_SOURCE = """#### กราฟเต็มขนาดแยกตามกลุ่ม

กราฟต่อไปนี้แสดงค่าใช้จ่ายเฉลี่ยต่อเดือนและหนี้สินเฉลี่ยต่อครัวเรือนของ 77 จังหวัด แยกหนึ่งกราฟต่อหนึ่งกลุ่มสถานะทางเศรษฐสังคม เส้นสีแดงเป็นเส้นแนวโน้มเชิงเส้น และไม่มีแถบความเชื่อมั่น"""

CODE_SOURCE = """for _, group_row in group_correlation.iterrows():
    group_data = expense_debt_detail.loc[
        (expense_debt_detail['soc_eco_class1'] == group_row['soc_eco_class1'])
        & (expense_debt_detail['soc_eco_class2'] == group_row['soc_eco_class2'])
    ]

    fig, ax = plt.subplots(figsize=(11, 7))
    sns.regplot(
        data=group_data,
        x='expense_monthly_baht',
        y='debt_average_baht',
        ax=ax,
        ci=None,
        scatter_kws={'s': 60, 'alpha': 0.75, 'color': '#4C78A8'},
        line_kws={'color': '#E45756', 'linewidth': 2},
    )
    title = textwrap.fill(group_row['group_label'], width=58)
    ax.set_title(f'{title} — ค่าใช้จ่ายเฉลี่ยและหนี้สินเฉลี่ยรายจังหวัด')
    ax.set_xlabel('ค่าใช้จ่ายเฉลี่ยต่อเดือน (บาท)')
    ax.set_ylabel('หนี้สินเฉลี่ยต่อครัวเรือน (บาท)')
    ax.text(
        0.04,
        0.95,
        f'Pearson r = {group_row["pearson_r"]:.3f} | R² = {group_row["r_squared"]:.3f} | n = {group_row["provinces"]} จังหวัด',
        transform=ax.transAxes,
        va='top',
        fontsize=11,
        bbox={'facecolor': 'white', 'alpha': 0.85, 'edgecolor': '#999999'},
    )
    plt.tight_layout()
    plt.show()"""


def main():
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    cell_by_id = {cell["id"]: cell for cell in notebook.cells}

    if MARKDOWN_ID in cell_by_id and CODE_ID in cell_by_id:
        cell_by_id[MARKDOWN_ID]["source"] = MARKDOWN_SOURCE
        cell_by_id[CODE_ID]["source"] = CODE_SOURCE
    else:
        relationship_index = next(
            (index for index, cell in enumerate(notebook.cells) if cell["id"] == "expense_debt_group_relationship_code"),
            None,
        )
        if relationship_index is None:
            raise ValueError("Could not find the expense–debt relationship section")

        markdown_cell = nbformat.v4.new_markdown_cell(MARKDOWN_SOURCE)
        markdown_cell["id"] = MARKDOWN_ID
        code_cell = nbformat.v4.new_code_cell(CODE_SOURCE)
        code_cell["id"] = CODE_ID
        notebook.cells[relationship_index + 1:relationship_index + 1] = [markdown_cell, code_cell]

    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            cell.get("metadata", {}).pop("execution", None)

    nbformat.write(notebook, NOTEBOOK_PATH)
    print(f"Added full-size expense–debt plots: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
