"""Append the 2566 complementary-data analysis cells to the notebook."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "household_income_debt_analysis.ipynb"
MARKER = "## 6. ตรวจสอบชุดข้อมูลเสริมจาก NSO ในปีเดียวกัน"


def md(source):
    return nbformat.v4.new_markdown_cell(source)


def code(source):
    return nbformat.v4.new_code_cell(source)


def cells():
    return [
        md(
            """## 6. ตรวจสอบชุดข้อมูลเสริมจาก NSO ในปีเดียวกัน

ชุดข้อมูลเสริมต่อไปนี้ดาวน์โหลดจาก NSO Catalog API และเก็บเฉพาะปี พ.ศ. 2566 เพื่อให้ตรงกับ SFD_SPB0801 เดิม:

- SFD_SPB0802_66: รายได้จำแนกตามแหล่งที่มา ระดับจังหวัด
- SFD_SPB0806 และ SFD_SPB0807: หนี้สินเฉลี่ยระดับจังหวัด ทั้งครัวเรือนและเฉพาะครัวเรือนที่เป็นหนี้
- SES_OS_29 ถึง SES_OS_31: จำนวนครัวเรือนที่เป็นหนี้ แหล่งเงินกู้ และประเภทหนี้ ระดับภูมิภาค/เขตการปกครอง
- SES_41_01 ถึง SES_41_05: รายได้ การกระจายรายได้ และ quintile ระดับภูมิภาค/สถานะทางเศรษฐสังคม

สามไฟล์ SFD เป็นระดับจังหวัดและใช้ตรวจสอบร่วมกับฐานเดิมได้ ส่วนไฟล์ SES เป็นระดับภูมิภาคหรือเขตการปกครอง จึงใช้เปรียบเทียบแยกชุด ไม่ควร merge กับจังหวัดโดยตรง."""
        ),
        code(
            """supplementary_dir_candidates = [Path('data/raw'), Path('../data/raw')]
supplementary_dir = next((path for path in supplementary_dir_candidates if path.exists()), None)
if supplementary_dir is None:
    raise FileNotFoundError('Could not find supplementary CSV snapshots in data/raw.')

supplementary_files = {
    'income_source_province': 'SFD_SPB0802_66.csv',
    'debt_all_households_province': 'SFD_SPB0806.csv',
    'debt_indebted_households_province': 'SFD_SPB0807.csv',
    'indebted_count_region': 'SES_OS_29_2566.csv',
    'indebted_source_purpose_region': 'SES_OS_30_2566.csv',
    'indebted_type_region': 'SES_OS_31_2566.csv',
    'income_source_region': 'SES_41_01_2566.csv',
    'income_socioeconomic': 'SES_41_02_2566.csv',
    'income_distribution_region': 'SES_41_03_2566.csv',
    'income_distribution_socioeconomic': 'SES_41_04_2566.csv',
    'income_quintile_region': 'SES_41_05_2566.csv',
}
supplementary_data = {
    name: pd.read_csv(supplementary_dir / filename)
    for name, filename in supplementary_files.items()
}


def year_column(frame):
    return next(column for column in ['year', 'Year', 'YEAR'] if column in frame.columns)


inventory_rows = []
for name, frame in supplementary_data.items():
    year_col = year_column(frame)
    geography = 'province' if 'province' in frame.columns else 'region/area'
    inventory_rows.append({
        'dataset': name,
        'file': supplementary_files[name],
        'rows': len(frame),
        'columns': len(frame.columns),
        'years': sorted(frame[year_col].dropna().unique().tolist()),
        'geography': geography,
        'duplicate_rows': int(frame.duplicated().sum()),
    })

inventory = pd.DataFrame(inventory_rows)
print('Supplementary-data inventory:')
print(inventory.to_string(index=False))
print()
print('Sample rows from the principal new tables:')
for name in [
    'income_source_province',
    'debt_all_households_province',
    'debt_indebted_households_province',
    'indebted_source_purpose_region',
    'income_source_region',
]:
    print(f'\\n{name}:')
    print(supplementary_data[name].head(2).to_string(index=False))

for frame in supplementary_data.values():
    assert set(frame[year_column(frame)].dropna().unique()) == {2566}

province_set = set(df['province'])
for name in [
    'income_source_province',
    'debt_all_households_province',
    'debt_indebted_households_province',
]:
    assert set(supplementary_data[name]['province']) == province_set

print('All stored supplementary snapshots contain only B.E. 2566 rows.')
print('All three provincial snapshots contain the same 77 provinces as SFD_SPB0801.')"""
        ),
        code(
            """# Cross-check overlapping indicators against the original SFD_SPB0801 snapshot.
comparison_key = ['province', 'soc_eco_class1', 'soc_eco_class2']

current_income = (
    df.loc[
        (df['indicator'] == 'รายได้ทั้งสิ้นต่อเดือน')
        & (df['soc_eco_class1'] != TOTAL_LABEL),
        comparison_key + ['value'],
    ]
    .rename(columns={'value': 'current_value'})
)
source_income_total = (
    supplementary_data['income_source_province']
    .loc[
        supplementary_data['income_source_province']['source_income3'] == 'รายได้ทั้งสิ้นต่อเดือน',
        comparison_key + ['value'],
    ]
    .rename(columns={'value': 'source_value'})
)
income_comparison = current_income.merge(source_income_total, on=comparison_key, how='outer', indicator=True)
income_comparison['absolute_difference'] = (
    income_comparison['current_value'] - income_comparison['source_value']
).abs()
income_mismatches = income_comparison.loc[income_comparison['absolute_difference'] > 0]

current_debt = (
    df.loc[
        (df['indicator'] == 'หนี้สินเฉลี่ยต่อครัวเรือนทั้งสิ้น')
        & (df['soc_eco_class1'] != TOTAL_LABEL),
        comparison_key + ['value'],
    ]
    .rename(columns={'value': 'current_value'})
)
source_debt_total = (
    supplementary_data['debt_all_households_province']
    .loc[
        supplementary_data['debt_all_households_province']['purpose_source_bor']
        == 'จำนวนหนี้สินเฉลี่ยต่อครัวเรือน',
        comparison_key + ['value'],
    ]
    .rename(columns={'value': 'source_value'})
)
debt_comparison = current_debt.merge(source_debt_total, on=comparison_key, how='outer', indicator=True)
debt_comparison['absolute_difference'] = (
    debt_comparison['current_value'] - debt_comparison['source_value']
).abs()
debt_mismatches = debt_comparison.loc[debt_comparison['absolute_difference'] > 0]

print(f'Income overlapping keys: {len(income_comparison):,}; unmatched: {(income_comparison["_merge"] != "both").sum()}')
print(f'Income exact matches: {len(income_comparison) - len(income_mismatches):,}; mismatches: {len(income_mismatches):,}')
if not income_mismatches.empty:
    print('Income mismatch(es) retained as published by each source snapshot:')
    print(income_mismatches.to_string(index=False))
print(f'Debt overlapping keys: {len(debt_comparison):,}; unmatched: {(debt_comparison["_merge"] != "both").sum()}')
print(f'Debt exact matches: {len(debt_comparison) - len(debt_mismatches):,}; mismatches: {len(debt_mismatches):,}')
assert len(income_comparison) == 770
assert len(debt_comparison) == 770
assert len(debt_mismatches) == 0

negative_income_rows = supplementary_data['income_source_province'].loc[
    supplementary_data['income_source_province']['value'] < 0
]
print(f'Negative values in provincial income-source table: {len(negative_income_rows):,}')
print('Negative values are retained because some source fields represent net agricultural/business profit; inspect before treating them as errors.')"""
        ),
        md(
            """### แหล่งที่มาของรายได้ในปี 2566

ตาราง SES_41_01 มีรายได้ระดับภูมิภาคและระดับเขตการปกครอง โดยใช้แถวประเทศไทยรวมเพื่อดูองค์ประกอบรายได้โดยไม่เฉลี่ยซ้ำข้ามกลุ่มเศรษฐสังคม."""
        ),
        code(
            """income_region = supplementary_data['income_source_region'].copy()
national_income = income_region.loc[
    (income_region['REGION'] == 'ทั่วราชอาณาจักร')
    & (income_region['AREA'] == 'เขตการปกครอง')
].iloc[0]

income_component_labels = {
    'รายได้จากการทำงาน': 'FROM_WORK',
    'เงินโอน/เงินช่วยเหลือ': 'CURRENT_TRANSFER',
    'รายได้จากทรัพย์สิน': 'PROPERTY_INCOME',
    'รายได้ไม่เป็นตัวเงิน': 'NONMONEY_INCOME',
    'รายได้ไม่ประจำที่เป็นตัวเงิน': 'NONCUR_M_INCOME',
}
income_components = pd.Series(
    {label: float(national_income[column]) for label, column in income_component_labels.items()},
    name='baht_per_month',
).sort_values(ascending=False)
income_components_table = income_components.to_frame()
income_components_table['share_of_monthly_income_pct'] = (
    income_components / float(national_income['MONTHLY_INCOME']) * 100
)
print(f"Thailand monthly household income: {national_income['MONTHLY_INCOME']:,.0f} baht")
print('Income components:')
print(income_components_table.round(2).to_string())
print(f"Largest component: {income_components.index[0]} ({income_components.iloc[0]:,.0f} baht/month)")

fig, ax = plt.subplots(figsize=(10, 5))
income_plot = income_components.rename_axis('component').reset_index()
sns.barplot(data=income_plot, x='baht_per_month', y='component', ax=ax, color='#4C78A8', errorbar=None)
ax.set_title('Thailand household income components, B.E. 2566')
ax.set_xlabel('Baht per month')
ax.set_ylabel('Income component')
plt.tight_layout()
plt.show()"""
        ),
        md(
            """### จำนวนครัวเรือนที่เป็นหนี้ แหล่งเงินกู้ และวัตถุประสงค์

SES_OS_29 ถึง SES_OS_31 เป็นจำนวนครัวเรือน ไม่ใช่ยอดหนี้ จึงใช้ตอบว่าหนี้กระจุกตัวที่วัตถุประสงค์หรือประเภทใด โดยเลือกข้อมูลประเทศไทยรวม."""
        ),
        code(
            """debt_count_region = supplementary_data['indebted_count_region'].copy()
debt_source_purpose_region = supplementary_data['indebted_source_purpose_region'].copy()
debt_type_region = supplementary_data['indebted_type_region'].copy()

for frame, columns in [
    (debt_count_region, ['Region', 'Area']),
    (debt_source_purpose_region, ['Region', 'Area', 'Source_loan', 'Purpose_borrow']),
    (debt_type_region, ['Region', 'Area', 'Type_debt']),
]:
    for column in columns:
        frame[column] = frame[column].astype(str).str.strip()

national_indebted_count = debt_count_region.loc[
    (debt_count_region['Region'] == 'ทั่วราชอาณาจักร')
    & (debt_count_region['Area'] == 'รวม'),
    'value',
].iloc[0]

purpose_by_source = debt_source_purpose_region.loc[
    (debt_source_purpose_region['Region'] == 'ทั่วราชอาณาจักร')
    & (debt_source_purpose_region['Area'] == 'รวม')
    & (debt_source_purpose_region['Source_loan'] != 'รวม')
    & (debt_source_purpose_region['Purpose_borrow'] != 'รวม'),
    ['Source_loan', 'Purpose_borrow', 'value'],
].sort_values('value', ascending=False)

type_national = debt_type_region.loc[
    (debt_type_region['Region'] == 'ทั่วราชอาณาจักร')
    & (debt_type_region['Area'] == 'รวม')
    & (debt_type_region['Type_debt'] != 'รวม'),
    ['Type_debt', 'value'],
].sort_values('value', ascending=False)

print(f'Indebted households in Thailand: {national_indebted_count:,.0f} households')
print('Indebted households by loan source and borrowing purpose:')
print(purpose_by_source.to_string(index=False))
print()
print('Indebted households by debt type:')
print(type_national.to_string(index=False))
largest_purpose_by_source = (
    purpose_by_source.loc[purpose_by_source.groupby('Source_loan')['value'].idxmax()]
    .sort_values('value', ascending=False)
)
print('Largest purpose within each loan source:')
print(largest_purpose_by_source.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(18, 6))
sns.barplot(data=purpose_by_source, x='value', y='Purpose_borrow', hue='Source_loan', ax=axes[0], errorbar=None)
axes[0].set_title('Indebted households by source and purpose')
axes[0].set_xlabel('Households')
axes[0].set_ylabel('Borrowing purpose')
sns.move_legend(axes[0], 'lower right', title='Loan source')
sns.barplot(data=type_national, x='value', y='Type_debt', ax=axes[1], color='#F58518', errorbar=None)
axes[1].set_title('Indebted households by debt type')
axes[1].set_xlabel('Households')
axes[1].set_ylabel('Debt type')
plt.tight_layout()
plt.show()"""
        ),
        md(
            """## 7. สรุปการตรวจสอบช่วงเวลาและขอบเขตข้อมูล

ชุดข้อมูลใหม่ทุกไฟล์ใน repository เป็น snapshot ปี พ.ศ. 2566 เช่นเดียวกับ SFD_SPB0801 เดิม แต่มีสองระดับพื้นที่:

- ระดับจังหวัด: รายได้จำแนกแหล่งที่มา และหนี้สินเฉลี่ย
- ระดับภูมิภาค/เขตการปกครอง: จำนวนครัวเรือนที่เป็นหนี้และองค์ประกอบรายได้

การตรวจสอบพบความแตกต่างของค่ารายได้ 1 คีย์จาก 770 คีย์ที่ทับซ้อนกันระหว่าง snapshot เดิมกับ SFD_SPB0802_66 จึงแสดงและเก็บค่าตามแหล่งข้อมูล ไม่ปรับแก้เงียบ ๆ."""
        ),
        code(
            """print('Final comparability checks:')
print('- Current base year:', sorted(df['year'].unique().tolist()))
print('- Supplementary years:', sorted(inventory['years'].explode().unique().tolist()))
print('- Current provinces:', df['province'].nunique())
print('- Provincial supplementary tables:', [
    supplementary_data[name]['province'].nunique()
    for name in ['income_source_province', 'debt_all_households_province', 'debt_indebted_households_province']
])
print('- Regional supplementary tables are kept as separate 2566 snapshots.')"""
        ),
    ]


def main():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    marker_indices = [index for index, cell in enumerate(notebook.cells) if MARKER in cell.source]
    if marker_indices:
        notebook.cells = notebook.cells[: marker_indices[0]]
    notebook.cells.extend(cells())
    nbformat.write(notebook, NOTEBOOK)
    print(f"Updated {NOTEBOOK} with {len(cells())} cells.")


if __name__ == "__main__":
    main()
