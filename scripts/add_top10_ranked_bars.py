"""Add readable top-10 provincial debt and income bar charts to the notebook."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "household_income_debt_analysis.ipynb"
MARKDOWN_ID = "top10_ranked_bars_markdown"
CODE_ID = "top10_ranked_bars_code"

MARKDOWN_SOURCE = """### จังหวัด 10 อันดับแรก: หนี้สินและรายได้

กราฟแท่งนี้เรียงลำดับจากมากไปน้อย เพื่อเปรียบเทียบจังหวัดที่มีหนี้สินเฉลี่ยต่อครัวเรือนสูงสุด 10 อันดับ และจังหวัดที่มีรายได้เฉลี่ยต่อเดือนสูงสุด 10 อันดับ ข้อมูลทั้งสองกราฟเป็นค่าเฉลี่ยระดับจังหวัด ปี พ.ศ. 2566"""

CODE_SOURCE = """top_debt_chart = wide.nlargest(10, 'debt_average_baht').copy()
top_income_chart = wide.nlargest(10, 'income_monthly_baht').copy()

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

sns.barplot(
    data=top_debt_chart,
    x='debt_average_baht',
    y='province',
    order=top_debt_chart['province'],
    ax=axes[0],
    color='#E45756',
    errorbar=None,
)
axes[0].set_title('10 จังหวัดที่มีหนี้สินเฉลี่ยสูงสุด')
axes[0].set_xlabel('หนี้สินเฉลี่ยต่อครัวเรือน (บาท)')
axes[0].set_ylabel('จังหวัด')
axes[0].bar_label(axes[0].containers[0], fmt='{:,.0f}', padding=3)

sns.barplot(
    data=top_income_chart,
    x='income_monthly_baht',
    y='province',
    order=top_income_chart['province'],
    ax=axes[1],
    color='#4C78A8',
    errorbar=None,
)
axes[1].set_title('10 จังหวัดที่มีรายได้เฉลี่ยต่อเดือนสูงสุด')
axes[1].set_xlabel('รายได้เฉลี่ยต่อเดือน (บาท)')
axes[1].set_ylabel('จังหวัด')
axes[1].bar_label(axes[1].containers[0], fmt='{:,.0f}', padding=3)

plt.tight_layout()
plt.show()"""


def main():
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    cell_by_id = {cell["id"]: cell for cell in notebook.cells}

    if MARKDOWN_ID in cell_by_id and CODE_ID in cell_by_id:
        cell_by_id[MARKDOWN_ID]["source"] = MARKDOWN_SOURCE
        cell_by_id[CODE_ID]["source"] = CODE_SOURCE
    else:
        summary_index = next(
            (index for index, cell in enumerate(notebook.cells) if cell["id"] == "a33f4282"),
            None,
        )
        if summary_index is None:
            raise ValueError("Could not find the regional-summary cell")

        markdown_cell = nbformat.v4.new_markdown_cell(MARKDOWN_SOURCE)
        markdown_cell["id"] = MARKDOWN_ID
        code_cell = nbformat.v4.new_code_cell(CODE_SOURCE)
        code_cell["id"] = CODE_ID
        notebook.cells[summary_index + 1:summary_index + 1] = [markdown_cell, code_cell]

    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            cell.get("metadata", {}).pop("execution", None)

    nbformat.write(notebook, NOTEBOOK_PATH)
    print(f"Added ranked bar charts: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
