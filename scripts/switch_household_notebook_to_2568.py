"""Switch the active household debt-analysis notebook to the B.E. 2568 source."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "household_income_debt_analysis.ipynb"


def set_source(cells: dict[str, nbformat.NotebookNode], cell_id: str, source: str) -> None:
    cells[cell_id]["source"] = source


def main() -> None:
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    cells = {cell["id"]: cell for cell in notebook.cells}

    expected_ids = {
        "1f87cb3a", "a56a7966", "c5fb14f5", "8eaa2d10", "974863f7", "a33f4282",
        "79c6405b", "c3077f2e", "ffd36eb1", "0eed0145", "b66ffafb", "4c001193",
        "thailand_debt_heatmap_markdown", "thailand_debt_heatmap_code",
    }
    missing_ids = expected_ids.difference(cells)
    if missing_ids:
        raise ValueError(f"Notebook layout changed; expected cells are missing: {sorted(missing_ids)}")

    set_source(cells, "1f87cb3a", """# การวิเคราะห์ข้อมูลรายได้และหนี้สินครัวเรือน

Notebook นี้เป็นการสำรวจข้อมูลรายได้ ค่าใช้จ่าย และหนี้สินครัวเรือนจากสำนักงานสถิติแห่งชาติ (NSO) ระดับจังหวัด ปี พ.ศ. 2568 เพื่อดูความสัมพันธ์ระหว่างรายได้และหนี้สิน ตรวจสอบคุณภาพข้อมูล และสร้างกราฟพื้นฐาน

**แหล่งข้อมูลที่ใช้ใน notebook นี้มีเพียง 1 แหล่ง:** `data/raw/nso_household_income_debt_province_2568.csv` ซึ่งสกัดจากรายงานการสำรวจภาวะเศรษฐกิจและสังคมของครัวเรือน พ.ศ. 2568 ตาราง ค.1

คำถามหลัก:
- ปริมาณหนี้สินครัวเรือนสัมพันธ์กับรายได้ครัวเรือนหรือไม่ อย่างไร
- จังหวัดและภูมิภาคใดมีรายได้หรือหนี้สินเฉลี่ยสูงที่สุด

## ขอบเขตและข้อควรระวัง
- ข้อมูลเป็นปี พ.ศ. 2568 (ค.ศ. 2025) เพียงปีเดียว จึงเป็นการเปรียบเทียบแบบ cross-sectional ไม่ใช่แนวโน้มตามเวลา
- ค่ารายได้และค่าใช้จ่ายเป็นค่าเฉลี่ยต่อเดือน ส่วนหนี้สินเป็นหนี้สินเฉลี่ยต่อครัวเรือน หน่วยเป็นบาท
- การหาความสัมพันธ์ใช้ค่าเฉลี่ยระดับจังหวัด 77 จังหวัด ไม่ใช่ข้อมูลรายครัวเรือน และไม่ควรตีความเป็นเหตุเป็นผล
- ไฟล์นี้มีจำนวนครัวเรือนระดับจังหวัด จึงใช้ถ่วงน้ำหนักเมื่อสรุปผลระดับภูมิภาค
- รายงาน พ.ศ. 2568 เผยแพร่ข้อมูลระดับจังหวัดเฉพาะยอดรวมของครัวเรือน จึงไม่สามารถจัดอันดับกลุ่มสถานะทางเศรษฐสังคมรายจังหวัดได้ใน notebook รุ่นนี้
- ไฟล์ panel หลายปีใน repository ยังไม่ถูกโหลดใน notebook นี้

แหล่งข้อมูล: [รายงานการสำรวจภาวะเศรษฐกิจและสังคมของครัวเรือน พ.ศ. 2568 (NSO)](https://www.nso.go.th/nsoweb/storage/survey_detail/2026/20260505141117_96690.pdf), ตาราง ค.1 รายได้ ค่าใช้จ่าย และหนี้สินเฉลี่ยต่อเดือนของครัวเรือน รายจังหวัด""")

    set_source(cells, "a56a7966", """from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
try:
    get_ipython().run_line_magic('matplotlib', 'inline')
except NameError:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

sns.set_theme(style='whitegrid', context='notebook')
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 160)
pd.set_option('display.float_format', lambda value: f'{value:,.2f}')

# Prefer a Thai-capable font when one is available on the machine.
available_fonts = {font.name for font in font_manager.fontManager.ttflist}
for candidate in ['Noto Sans Thai', 'Tahoma', 'Arial Unicode MS', 'Th Sarabun New', 'DejaVu Sans']:
    if candidate in available_fonts:
        plt.rcParams['font.family'] = candidate
        break

data_path_candidates = [
    Path('data/raw/nso_household_income_debt_province_2568.csv'),
    Path('../data/raw/nso_household_income_debt_province_2568.csv'),
]
data_path = next((path for path in data_path_candidates if path.exists()), None)
if data_path is None:
    raise FileNotFoundError(
        'Could not find data/raw/nso_household_income_debt_province_2568.csv. '
        'Run scripts/fetch_nso_2568_province_totals.py first.'
    )

raw_df = pd.read_csv(data_path)
metric_column = 'mthincome_mthexp_totaldebt_pctexptoincome'
df = raw_df.rename(columns={metric_column: 'indicator'}).copy()
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df['year_ce'] = df['year'] - 543

TOTAL_LABEL = 'รวมทั้งสิ้น'
print(f'Loaded: {data_path}')
print(f'Shape: {df.shape[0]:,} rows x {df.shape[1]:,} columns')
print(f'Years (B.E.): {sorted(df["year"].unique().tolist())}')
print(f'Provinces: {df["province"].nunique()}')""")

    set_source(cells, "c5fb14f5", """The missing `attribute` values are expected: the field records the formula for the derived expense-to-income percentage only. The income, expenditure, and debt values are direct provincial totals from NSO Table C.1; all core analysis fields should have no missing values after numeric conversion.""")

    set_source(cells, "8eaa2d10", """## 2. เตรียมชุดข้อมูลระดับจังหวัดและกำหนดภูมิภาค

รายงาน พ.ศ. 2568 ให้ข้อมูลระดับจังหวัดเฉพาะแถว `รวมทั้งสิ้น` จึง pivot ตัวชี้วัดให้อยู่คนละคอลัมน์ และนำจำนวนครัวเรือนที่รายงานมาประกอบเพื่อถ่วงน้ำหนักการสรุประดับภูมิภาค""")

    set_source(cells, "974863f7", """total_scope = df.loc[
    (df['soc_eco_class1'] == TOTAL_LABEL) & (df['soc_eco_class2'] == TOTAL_LABEL)
].copy()

wide = total_scope.pivot(
    index=['year', 'year_ce', 'province'],
    columns='indicator',
    values='value',
).reset_index()
wide.columns.name = None
wide = wide.rename(columns={
    'รายได้ทั้งสิ้นต่อเดือน': 'income_monthly_baht',
    'ค่าใช้จ่ายทั้งสิ้นต่อเดือน': 'expense_monthly_baht',
    'หนี้สินเฉลี่ยต่อครัวเรือนทั้งสิ้น': 'debt_average_baht',
    'ร้อยละของค่าใช้จ่ายต่อรายได้': 'expense_income_pct',
})

province_metadata = total_scope.drop_duplicates('province')[
    ['province', 'total_households', 'average_household_size']
]
wide = wide.merge(province_metadata, on='province', how='left', validate='one_to_one')

REGION_PROVINCES = {
    'กรุงเทพมหานครและ 3 จังหวัด': ['กรุงเทพมหานคร', 'นนทบุรี', 'ปทุมธานี', 'สมุทรปราการ'],
    'ภาคกลาง': [
        'กาญจนบุรี', 'จันทบุรี', 'ฉะเชิงเทรา', 'ชลบุรี', 'ชัยนาท', 'ตราด', 'นครนายก',
        'นครปฐม', 'ประจวบคีรีขันธ์', 'ปราจีนบุรี', 'พระนครศรีอยุธยา', 'เพชรบุรี', 'ระยอง',
        'ราชบุรี', 'ลพบุรี', 'สมุทรสงคราม', 'สมุทรสาคร', 'สระแก้ว', 'สระบุรี', 'สิงห์บุรี',
        'สุพรรณบุรี', 'อ่างทอง',
    ],
    'ภาคเหนือ': [
        'กำแพงเพชร', 'เชียงราย', 'เชียงใหม่', 'ตาก', 'นครสวรรค์', 'น่าน', 'พะเยา',
        'พิจิตร', 'พิษณุโลก', 'เพชรบูรณ์', 'แพร่', 'แม่ฮ่องสอน', 'ลำปาง', 'ลำพูน',
        'สุโขทัย', 'อุตรดิตถ์', 'อุทัยธานี',
    ],
    'ภาคตะวันออกเฉียงเหนือ': [
        'กาฬสินธุ์', 'ขอนแก่น', 'ชัยภูมิ', 'นครพนม', 'นครราชสีมา', 'บึงกาฬ', 'บุรีรัมย์',
        'มหาสารคาม', 'มุกดาหาร', 'ยโสธร', 'ร้อยเอ็ด', 'เลย', 'ศรีสะเกษ', 'สกลนคร',
        'สุรินทร์', 'หนองคาย', 'หนองบัวลำภู', 'อุดรธานี', 'อุบลราชธานี', 'อำนาจเจริญ',
    ],
    'ภาคใต้': [
        'กระบี่', 'ชุมพร', 'ตรัง', 'นครศรีธรรมราช', 'นราธิวาส', 'ปัตตานี', 'พังงา',
        'พัทลุง', 'ภูเก็ต', 'ยะลา', 'ระนอง', 'สงขลา', 'สตูล', 'สุราษฎร์ธานี',
    ],
}

province_to_region = {
    province: region
    for region, provinces in REGION_PROVINCES.items()
    for province in provinces
}
wide['region'] = wide['province'].map(province_to_region)
wide['region'] = pd.Categorical(wide['region'], categories=list(REGION_PROVINCES), ordered=True)

required_metrics = [
    'income_monthly_baht', 'expense_monthly_baht', 'debt_average_baht',
    'expense_income_pct', 'total_households', 'average_household_size',
]
assert len(total_scope) == 77 * 4
assert wide['province'].nunique() == 77
assert wide[required_metrics].notna().all().all()
assert wide['region'].notna().all()
print(f'Total-scope rows: {len(total_scope):,}')
print(f'Province-level rows after pivot: {len(wide):,}')
print(f'Total households represented: {wide["total_households"].sum():,.0f}')
print('Province counts by region:')
print(wide.groupby('region', observed=True)['province'].nunique().to_string())""")

    set_source(cells, "a33f4282", """province_display_cols = ['province', 'region', 'income_monthly_baht', 'debt_average_baht', 'expense_income_pct']
print('Top 10 provinces by average household debt:')
print(wide.nlargest(10, 'debt_average_baht')[province_display_cols].to_string(index=False))
print()
print('Top 10 provinces by monthly total household income:')
print(wide.nlargest(10, 'income_monthly_baht')[province_display_cols].to_string(index=False))

region_rows = []
for region, group in wide.groupby('region', observed=True):
    weights = group['total_households'].to_numpy()
    weighted_income = np.average(group['income_monthly_baht'], weights=weights)
    weighted_expense = np.average(group['expense_monthly_baht'], weights=weights)
    region_rows.append({
        'region': region,
        'provinces': group['province'].nunique(),
        'total_households': weights.sum(),
        'income_monthly_baht': weighted_income,
        'debt_average_baht': np.average(group['debt_average_baht'], weights=weights),
        'expense_income_pct': weighted_expense / weighted_income * 100,
    })

region_summary = (
    pd.DataFrame(region_rows)
    .set_index('region')
    .sort_values('debt_average_baht', ascending=False)
)
print()
print('Regional summary (household-weighted provincial averages):')
print(region_summary.round(2).to_string())

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
debt_region_order = region_summary.sort_values('debt_average_baht').index
income_region_order = region_summary.sort_values('income_monthly_baht').index
region_plot = region_summary.reset_index()
sns.barplot(data=region_plot, x='debt_average_baht', y='region', order=debt_region_order, ax=axes[0], color='#E45756', errorbar=None)
axes[0].set_title('Average household debt by region')
axes[0].set_xlabel('Average debt (baht)')
axes[0].set_ylabel('')
sns.barplot(data=region_plot, x='income_monthly_baht', y='region', order=income_region_order, ax=axes[1], color='#4C78A8', errorbar=None)
axes[1].set_title('Monthly household income by region')
axes[1].set_xlabel('Monthly income (baht)')
axes[1].set_ylabel('')
plt.tight_layout()
plt.show()""")

    set_source(cells, "79c6405b", """## 4. ความสัมพันธ์ระหว่างรายได้กับหนี้สิน

การคำนวณต่อไปนี้เป็นความสัมพันธ์ระหว่างค่าเฉลี่ยระดับจังหวัดในปี พ.ศ. 2568 จึงตอบได้เพียงว่าจังหวัดที่มีรายได้เฉลี่ยสูงกว่ามักมีหนี้สินเฉลี่ยสูงกว่าหรือไม่ ไม่ได้พิสูจน์ว่ารายได้เป็นสาเหตุของหนี้สิน""")

    set_source(cells, "c3077f2e", """relationship_cols = ['income_monthly_baht', 'debt_average_baht']
pearson_r = wide[relationship_cols].corr(method='pearson').iloc[0, 1]
# Ranking first gives the standard Spearman correlation without requiring SciPy.
spearman_r = wide[relationship_cols].rank().corr(method='pearson').iloc[0, 1]
print(f'Pearson correlation (n={len(wide)} provinces): {pearson_r:.3f}')
print(f'Spearman rank correlation: {spearman_r:.3f}')
print(f'Mean monthly income: {wide["income_monthly_baht"].mean():,.0f} baht')
print(f'Mean average debt: {wide["debt_average_baht"].mean():,.0f} baht')

fig, ax = plt.subplots(figsize=(10, 7))
sns.regplot(
    data=wide,
    x='income_monthly_baht',
    y='debt_average_baht',
    ax=ax,
    scatter_kws={'s': 60, 'alpha': 0.75, 'color': '#4C78A8'},
    line_kws={'color': '#E45756', 'linewidth': 2},
)
for _, row in wide.nlargest(3, 'debt_average_baht').iterrows():
    ax.annotate(row['province'], (row['income_monthly_baht'], row['debt_average_baht']), xytext=(5, 5), textcoords='offset points', fontsize=9)
ax.set_title(f'Province-level income and household debt (Pearson r = {pearson_r:.3f})')
ax.set_xlabel('Monthly total household income (baht)')
ax.set_ylabel('Average household debt (baht)')
plt.tight_layout()
plt.show()""")

    set_source(cells, "ffd36eb1", """## 5. ขอบเขตข้อมูลสถานะทางเศรษฐสังคม

รายงาน พ.ศ. 2568 ตาราง ค.1 เผยแพร่รายได้ ค่าใช้จ่าย และหนี้สินในระดับ **ยอดรวมรายจังหวัด** เท่านั้น ไม่มีตารางที่จำแนกสถานะทางเศรษฐสังคมในระดับจังหวัด ดังนั้น notebook รุ่นนี้จึงไม่นำเสนอการจัดอันดับกลุ่มอาชีพหรือสถานะทางเศรษฐสังคม เพื่อหลีกเลี่ยงการนำข้อมูลระดับภูมิภาคหรือระดับประเทศมาแทนข้อมูลรายจังหวัด""")

    set_source(cells, "0eed0145", """detailed_rows = df.loc[df['soc_eco_class2'] != TOTAL_LABEL]
assert detailed_rows.empty
print('Province-level socioeconomic-group rows:', len(detailed_rows))
print('The 2568 source supports total provincial analysis only; socioeconomic-group rankings are omitted.')""")

    set_source(cells, "b66ffafb", """## สรุปผลเบื้องต้น

ผลลัพธ์ในเซลล์ด้านบนตอบคำถามในขอบเขตของชุดข้อมูล `nso_household_income_debt_province_2568.csv` ซึ่งสกัดจากตาราง ค.1 ของรายงาน NSO พ.ศ. 2568 แหล่งเดียวนี้ ควรอ่านร่วมกับข้อจำกัดของข้อมูล: ค่าเป็นค่าเฉลี่ยระดับจังหวัด ไม่ใช่ข้อมูลรายครัวเรือน, การวิเคราะห์ความสัมพันธ์ไม่ใช่หลักฐานเชิงเหตุผล, และข้อมูลจำแนกสถานะทางเศรษฐสังคมรายจังหวัดไม่เผยแพร่ในรายงานรุ่นนี้ แม้ repository จะมี panel หลายปีแยกต่างหาก แต่ notebook นี้ใช้เฉพาะภาพตัดขวางปี 2568""")

    set_source(cells, "4c001193", """highest_debt = wide.loc[wide['debt_average_baht'].idxmax()]
highest_income = wide.loc[wide['income_monthly_baht'].idxmax()]
highest_debt_region = region_summary['debt_average_baht'].idxmax()
highest_income_region = region_summary['income_monthly_baht'].idxmax()

print('Key findings for the total provincial scope:')
print(f'- Highest-debt province: {highest_debt["province"]} ({highest_debt["debt_average_baht"]:,.0f} baht)')
print(f'- Highest-income province: {highest_income["province"]} ({highest_income["income_monthly_baht"]:,.0f} baht/month)')
print(f'- Highest-debt region by household-weighted provincial average: {highest_debt_region}')
print(f'- Highest-income region by household-weighted provincial average: {highest_income_region}')
print(f'- Province-level Pearson correlation: {pearson_r:.3f}')""")

    set_source(cells, "thailand_debt_heatmap_markdown", """## 6. แผนที่ความร้อนหนี้สินเฉลี่ยรายจังหวัด

แผนที่นี้นำหนี้สินเฉลี่ยต่อครัวเรือนของแต่ละจังหวัดในปี พ.ศ. 2568 มาแสดงบนขอบเขตจังหวัดของประเทศไทย โดยใช้สีเขียวแทนจังหวัดที่มีหนี้สินเฉลี่ยต่ำกว่า และสีแดงแทนจังหวัดที่มีหนี้สินเฉลี่ยสูงกว่า สีของแต่ละจังหวัดจึงเปรียบเทียบตามช่วงค่าต่ำสุดถึงสูงสุดของ 77 จังหวัดในข้อมูลนี้

ขอบเขตแผนที่มาจาก [Thailand Canonical Administrative-Names Reference](https://github.com/ReynoldsWJ55/thailand-canonical-admin-names) ซึ่งเผยแพร่ GeoJSON ขอบเขตระดับจังหวัด 77 แห่ง โดยใช้ไฟล์เวอร์ชันที่ระบุไว้ในเซลล์ถัดไป""")

    heatmap_source = cells["thailand_debt_heatmap_code"]["source"]
    cells["thailand_debt_heatmap_code"]["source"] = heatmap_source.replace(
        "'Thailand provincial average household debt, B.E. 2566'",
        "f'Thailand provincial average household debt, B.E. {int(wide[\"year\"].iloc[0])}'",
    )

    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            cell.get("metadata", {}).pop("execution", None)

    nbformat.write(notebook, NOTEBOOK_PATH)
    print(f"Switched: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
