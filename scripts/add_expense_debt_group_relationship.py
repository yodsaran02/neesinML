"""Add expense-versus-debt analysis by socioeconomic group to the SFD-only notebook."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "household_income_debt_analysis.ipynb"
MARKDOWN_ID = "expense_debt_group_relationship_markdown"
CODE_ID = "expense_debt_group_relationship_code"

MARKDOWN_SOURCE = """### ความสัมพันธ์ระหว่างค่าใช้จ่ายและหนี้สิน แยกตามกลุ่มสถานะทางเศรษฐสังคม

ส่วนนี้ใช้เฉพาะข้อมูล `SFD_SPB0801.csv` และคำนวณ Pearson correlation ระหว่างค่าใช้จ่ายเฉลี่ยต่อเดือนกับหนี้สินเฉลี่ยต่อครัวเรือน **ข้าม 77 จังหวัด** ภายในแต่ละกลุ่มสถานะทางเศรษฐสังคมย่อย

ค่า `r` ที่สูงกว่า หมายถึงในกลุ่มนั้นจังหวัดที่มีค่าใช้จ่ายเฉลี่ยสูงกว่ามักมีหนี้สินเฉลี่ยสูงกว่าเช่นกัน ส่วน `R²` คือสัดส่วนความแปรปรวนของหนี้สินที่สัมพันธ์กับเส้นตรงของค่าใช้จ่ายในแบบจำลองตัวแปรเดียว ผลนี้เป็นความสัมพันธ์ของค่าเฉลี่ยระดับจังหวัด ไม่ใช่หลักฐานเชิงเหตุผลหรือวัตถุประสงค์ของหนี้"""

CODE_SOURCE = """relationship_index = ['province', 'soc_eco_class1', 'soc_eco_class2']
is_detail_group = df['soc_eco_class2'] != TOTAL_LABEL
expense_debt_rows = df.loc[is_detail_group].copy()

expense_debt_detail = expense_debt_rows.pivot(
    index=relationship_index,
    columns='indicator',
    values='value',
).reset_index()
expense_debt_detail.columns.name = None
expense_debt_detail.rename(columns={
    'ค่าใช้จ่ายทั้งสิ้นต่อเดือน': 'expense_monthly_baht',
    'หนี้สินเฉลี่ยต่อครัวเรือนทั้งสิ้น': 'debt_average_baht',
}, inplace=True)

correlation_rows = []
grouped_detail = expense_debt_detail.groupby(
    ['soc_eco_class1', 'soc_eco_class2'],
    observed=True,
)
for group_keys, group_data in grouped_detail:
    class_1, class_2 = group_keys
    expenses = group_data['expense_monthly_baht']
    debts = group_data['debt_average_baht']
    pearson_r = expenses.corr(debts)
    correlation_rows.append({
        'soc_eco_class1': class_1,
        'soc_eco_class2': class_2,
        'provinces': len(group_data),
        'mean_expense_baht': expenses.mean(),
        'mean_debt_baht': debts.mean(),
        'pearson_r': pearson_r,
        'r_squared': pearson_r ** 2,
    })

group_correlation = pd.DataFrame(correlation_rows)
group_correlation['group_label'] = (
    group_correlation['soc_eco_class1']
    + ': '
    + group_correlation['soc_eco_class2']
)
group_correlation = group_correlation.sort_values('pearson_r', ascending=False)

required_columns = ['expense_monthly_baht', 'debt_average_baht']
assert len(expense_debt_detail) == 77 * 10
assert expense_debt_detail[required_columns].notna().all().all()
assert len(group_correlation) == 10
assert (group_correlation['provinces'] == 77).all()

print('Expense–debt relationship by detailed socioeconomic group:')
print(group_correlation[
    ['soc_eco_class1', 'soc_eco_class2', 'provinces', 'mean_expense_baht', 'mean_debt_baht', 'pearson_r', 'r_squared']
].round(3).to_string(index=False))

strongest_group = group_correlation.iloc[0]
weakest_group = group_correlation.iloc[-1]
print()
print(f'Strongest relationship: {strongest_group["soc_eco_class2"]} (r = {strongest_group["pearson_r"]:.3f}, R² = {strongest_group["r_squared"]:.3f})')
print(f'Weakest relationship: {weakest_group["soc_eco_class2"]} (r = {weakest_group["pearson_r"]:.3f}, R² = {weakest_group["r_squared"]:.3f})')
"""

CODE_SOURCE += """fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(
    data=group_correlation,
    x='pearson_r',
    y='group_label',
    ax=ax,
    color='#4C78A8',
    errorbar=None,
)
ax.axvline(0, color='black', linewidth=1)
ax.set_title('ความสัมพันธ์ระหว่างค่าใช้จ่ายและหนี้สิน แยกตามกลุ่มสถานะทางเศรษฐสังคม')
ax.set_xlabel('Pearson correlation (r)')
ax.set_ylabel('กลุ่มสถานะทางเศรษฐสังคม')
ax.bar_label(ax.containers[0], fmt='{:.3f}', padding=3)
plt.tight_layout()
plt.show()
"""

CODE_SOURCE += """group_order = group_correlation['group_label'].tolist()
fig, axes = plt.subplots(2, 5, figsize=(22, 9), sharex=True, sharey=True)
for ax, group_label in zip(axes.flat, group_order):
    group_row = group_correlation.loc[group_correlation['group_label'] == group_label].iloc[0]
    group_data = expense_debt_detail.loc[
        (expense_debt_detail['soc_eco_class1'] == group_row['soc_eco_class1'])
        & (expense_debt_detail['soc_eco_class2'] == group_row['soc_eco_class2'])
    ]
    sns.regplot(
        data=group_data,
        x='expense_monthly_baht',
        y='debt_average_baht',
        ax=ax,
        ci=None,
        scatter_kws={'s': 24, 'alpha': 0.65, 'color': '#4C78A8'},
        line_kws={'color': '#E45756', 'linewidth': 1.8},
    )
    ax.set_title(textwrap.fill(group_label, width=28), fontsize=9)
    ax.text(
        0.04,
        0.92,
        f'r = {group_row["pearson_r"]:.3f}; R² = {group_row["r_squared"]:.3f}',
        transform=ax.transAxes,
        va='top',
        fontsize=9,
        bbox={'facecolor': 'white', 'alpha': 0.8, 'edgecolor': 'none'},
    )
    ax.set_xlabel('')
    ax.set_ylabel('')

fig.suptitle('ค่าใช้จ่ายเฉลี่ยและหนี้สินเฉลี่ยในแต่ละกลุ่มสถานะทางเศรษฐสังคม', fontsize=15, y=1.02)
fig.supxlabel('ค่าใช้จ่ายเฉลี่ยต่อเดือน (บาท)')
fig.supylabel('หนี้สินเฉลี่ยต่อครัวเรือน (บาท)')
plt.tight_layout()
plt.show()
"""


def main():
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    cell_by_id = {cell["id"]: cell for cell in notebook.cells}

    if MARKDOWN_ID in cell_by_id and CODE_ID in cell_by_id:
        cell_by_id[MARKDOWN_ID]["source"] = MARKDOWN_SOURCE
        cell_by_id[CODE_ID]["source"] = CODE_SOURCE
    else:
        section_index = next(
            (index for index, cell in enumerate(notebook.cells) if cell["id"] == "debt_by_status_code"),
            None,
        )
        if section_index is None:
            raise ValueError("Could not find the debt-by-status section")

        markdown_cell = nbformat.v4.new_markdown_cell(MARKDOWN_SOURCE)
        markdown_cell["id"] = MARKDOWN_ID
        code_cell = nbformat.v4.new_code_cell(CODE_SOURCE)
        code_cell["id"] = CODE_ID
        notebook.cells[section_index + 1:section_index + 1] = [markdown_cell, code_cell]

    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            cell.get("metadata", {}).pop("execution", None)

    nbformat.write(notebook, NOTEBOOK_PATH)
    print(f"Added expense–debt group relationship: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
