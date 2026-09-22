"""Add an SFD_SPB0801-only debt-by-economic-status section to the old notebook."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "household_income_debt_analysis.ipynb"
MARKDOWN_ID = "debt_by_status_markdown"
CODE_ID = "debt_by_status_code"

MARKDOWN_SOURCE = """### กลุ่มครัวเรือนที่มีหนี้สินเฉลี่ยสูง

`SFD_SPB0801.csv` ไม่ระบุแหล่งเงินกู้หรือวัตถุประสงค์ของหนี้ ส่วนนี้จึงตอบได้เพียงว่า **กลุ่มสถานะทางเศรษฐสังคมใดมีหนี้สินเฉลี่ยสูงกว่า** โดยคำนวณค่าเฉลี่ยอย่างไม่ถ่วงน้ำหนักจากกลุ่มย่อยในแต่ละจังหวัด ไม่ควรตีความว่าเป็นแหล่งกำเนิดของหนี้"""

CODE_SOURCE = """debt_by_main_group = class_summary.groupby(
    'soc_eco_class1',
    observed=True,
)['debt_average_baht'].mean()
debt_by_main_group = debt_by_main_group.reset_index()
debt_by_main_group = debt_by_main_group.sort_values(
    'debt_average_baht',
    ascending=False,
)

print('Average debt by main socioeconomic group:')
print(debt_by_main_group.round(2).to_string(index=False))

fig, ax = plt.subplots(figsize=(11, 6))
sns.barplot(
    data=debt_by_main_group,
    x='debt_average_baht',
    y='soc_eco_class1',
    ax=ax,
    color='#E45756',
    errorbar=None,
)
ax.set_title('หนี้สินเฉลี่ยตามกลุ่มสถานะทางเศรษฐสังคม')
ax.set_xlabel('หนี้สินเฉลี่ยต่อครัวเรือน (บาท)')
ax.set_ylabel('กลุ่มสถานะทางเศรษฐสังคม')
ax.bar_label(ax.containers[0], fmt='{:,.0f}', padding=3)
plt.tight_layout()
plt.show()"""


def main():
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    cell_by_id = {cell["id"]: cell for cell in notebook.cells}

    if MARKDOWN_ID in cell_by_id and CODE_ID in cell_by_id:
        cell_by_id[MARKDOWN_ID]["source"] = MARKDOWN_SOURCE
        cell_by_id[CODE_ID]["source"] = CODE_SOURCE
    else:
        detail_cell_index = next(
            (index for index, cell in enumerate(notebook.cells) if cell["id"] == "0eed0145"),
            None,
        )
        if detail_cell_index is None:
            raise ValueError("Could not find the socioeconomic-detail cell")

        markdown_cell = nbformat.v4.new_markdown_cell(MARKDOWN_SOURCE)
        markdown_cell["id"] = MARKDOWN_ID
        code_cell = nbformat.v4.new_code_cell(CODE_SOURCE)
        code_cell["id"] = CODE_ID
        notebook.cells[detail_cell_index + 1:detail_cell_index + 1] = [markdown_cell, code_cell]

    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            cell.get("metadata", {}).pop("execution", None)

    nbformat.write(notebook, NOTEBOOK_PATH)
    print(f"Added debt-by-status section: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
