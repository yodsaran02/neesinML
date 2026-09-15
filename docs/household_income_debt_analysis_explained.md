# Household Income and Debt Analysis Notebook: A Plain-Language Guide

This document explains **every cell** in [`household_income_debt_analysis.ipynb`](../household_income_debt_analysis.ipynb). It describes what the code does, why each step is needed, what the printed results mean, and what the analysis cannot prove.

The notebook is written partly in Thai because the NSO data uses Thai labels. This guide keeps the original labels in code formatting so that each explanation can be matched directly to the notebook and CSV files.

---

## 1. What the notebook is trying to answer

The notebook explores household income, expenses, and debt in Thailand using province-level data from the **National Statistical Office (NSO)** for B.E. 2566, which is C.E. 2023.

It asks three main questions:

1. Do provinces with higher average monthly household income also tend to have higher average household debt?
2. Which provinces and regions have the highest average income or debt?
3. Which detailed socioeconomic groups have the highest reported average income and debt?

It then adds related NSO tables from the same year to answer questions that the original table cannot answer, such as:

- What are the main sources of household income?
- How many households are indebted?
- What are the purposes and types of debt?
- Do overlapping provincial tables agree with the original table?

### Important meaning of “average”

The main file does **not** contain one record for every household. It contains values already summarized by province and socioeconomic category. Therefore:

- `income_monthly_baht` means reported average total household income per month.
- `debt_average_baht` means reported average household debt.
- The correlation uses **77 provincial averages**, not individual household observations.
- A region's value is usually the simple average of its provinces' reported averages. It is not a household-weighted national or regional average.

---

## 2. Main results at a glance

The notebook's executed outputs report the following:

| Question | Result |
|---|---|
| Province with the highest average debt | Phuket (`ภูเก็ต`), **424,977 baht** |
| Province with the highest monthly income | Pathum Thani (`ปทุมธานี`), **45,729 baht/month** |
| Region with the highest simple mean of provincial debt averages | Bangkok and 3 provinces (`กรุงเทพมหานครและ 3 จังหวัด`) |
| Region with the highest simple mean of provincial income averages | Bangkok and 3 provinces (`กรุงเทพมหานครและ 3 จังหวัด`) |
| Pearson income–debt correlation | **0.488** across 77 provinces |
| Spearman income–debt correlation | **0.389** |
| Mean provincial monthly income | **26,445 baht/month** |
| Mean provincial average debt | **195,125 baht** |
| Highest detailed socioeconomic group for both income and debt | `ผู้จัดการนักวิชาการและผู้ปฏิบัติงานวิชาชีพ` (managers, academics, and professionals) |
| Thailand's monthly household income in the supplementary table | **29,030 baht/month** |
| Largest income component | Income from work, **20,465 baht/month** or about **70.50%** |
| Number of indebted households | **11,472,172 households** |

These are descriptive results. They show patterns in the published data; they do not show that income causes debt or that a province's result applies to every household in that province.

---

## 3. Data used by the notebook

### 3.1 Main input file

The first part of the notebook reads:

```text
data/raw/SFD_SPB0801.csv
```

This is an NSO table containing 3,388 rows:

- 1 year: B.E. 2566
- 77 provinces
- 4 indicators
- multiple socioeconomic categories

The original indicator column has the long name:

```text
mthincome_mthexp_totaldebt_pctexptoincome
```

The notebook renames it to the easier name `indicator`.

### 3.2 Main indicators

| Thai label in the CSV | Name used later | Meaning | Unit |
|---|---|---|---|
| `รายได้ทั้งสิ้นต่อเดือน` | `income_monthly_baht` | Total household income per month | Baht |
| `ค่าใช้จ่ายทั้งสิ้นต่อเดือน` | `expense_monthly_baht` | Total household expenses per month | Baht |
| `หนี้สินเฉลี่ยต่อครัวเรือนทั้งสิ้น` | `debt_average_baht` | Average total debt per household | Baht |
| `ร้อยละของค่าใช้จ่ายต่อรายได้` | `expense_income_pct` | Expenses as a percentage of income | Percent |

The `unit` column confirms whether a value is in `บาท` (baht) or `ร้อยละ` (percent).

### 3.3 Socioeconomic columns

The data has two levels of socioeconomic classification:

- `soc_eco_class1`: a broader category.
- `soc_eco_class2`: a more detailed category.

`รวมทั้งสิ้น` means **total**. The notebook uses the rows where both classification columns equal `รวมทั้งสิ้น` when it wants one overall value per province.

The broad categories in `soc_eco_class1` are approximately:

- `ผู้ถือครองทำการเกษตร/เพาะเลี้ยง` — agricultural or aquaculture holders
- `ผู้ประกอบธุรกิจของตนเองที่ไม่ใช่การเกษตร` — non-agricultural self-employed business owners
- `ลูกจ้าง` — employees
- `ผู้ไม่ได้ปฏิบัติงานเชิงเศรษฐกิจ` — people not economically active
- `รวมทั้งสิ้น` — total

The detailed categories in `soc_eco_class2` include land-owning and tenant farmers, fishery/forestry/agricultural-service workers, non-agricultural business owners, managers/academics/professionals, agricultural/forestry/fishery workers, transport/basic workers, clerical/sales/service workers, production/construction/mining workers, economically inactive people, and the total category.

The English descriptions are only for easy reading. The Thai labels in the source remain the authoritative category names.

### 3.4 Other useful columns

| Column | Meaning |
|---|---|
| `year` | Buddhist Era year; 2566 is 2023 in the Gregorian calendar |
| `province` | Thai province name |
| `value` | Numeric value of the selected indicator |
| `attribute` | Optional note supplied by NSO, often explaining a zero from the sample survey |
| `source` | Data provider; here it is the National Statistical Office |
| `year_ce` | Gregorian year created by subtracting 543 from `year` |

---

## 4. How to run the notebook

Run it from the repository root so that the first data path works:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook household_income_debt_analysis.ipynb
```

The notebook also tries `../data/raw/...`, which makes it possible to run from a nearby directory, but running from the repository root is the clearest option.

The supplementary CSV snapshots are already stored in `data/raw/`. To download fresh copies and keep only B.E. 2566 rows, use:

```bash
python3 scripts/fetch_nso_2566_data.py
```

That script downloads from the NSO Catalog API. The notebook itself reads local CSV files; it does not download data during execution.

Dependencies are listed in [`requirements.txt`](../requirements.txt): NumPy, pandas, seaborn, matplotlib, Jupyter/IPython support, and notebook execution libraries.

---

## 5. Complete cell-by-cell explanation

The notebook contains 26 cells, numbered here as cells 0 through 25, matching the order in the `.ipynb` file.

### Cell 0 — Introduction and scope

This is the opening Markdown cell. It states:

- the purpose of the analysis;
- the three main questions;
- the data source;
- the fact that the data is for only one year;
- the meaning of the income, expense, and debt values;
- the fact that the main comparison uses 77 province-level averages;
- the absence of household counts for weighting regional means; and
- the fact that the original file does not directly provide income sources or debt purposes.

The warnings in this cell are important. The notebook is a **cross-sectional exploratory analysis**: it compares different provinces in one year. It is not a time-series analysis and cannot establish cause and effect.

### Cell 1 — Import libraries, configure display, and load the main CSV

This code cell performs the initial setup.

#### Imports

- `Path` finds files in a platform-independent way.
- `numpy` is imported as `np`, although no major NumPy operation is needed later.
- `pandas` is imported as `pd` for table manipulation.
- `seaborn` and `matplotlib.pyplot` create the charts.
- `font_manager` helps find a font that can display Thai text.

#### Plot configuration

```python
try:
    get_ipython().run_line_magic('matplotlib', 'inline')
except NameError:
    matplotlib.use('Agg')
```

Inside Jupyter, this displays plots below the cell. Outside Jupyter, the `Agg` backend allows plotting without an interactive screen. This makes the code safer to run in a script or automated environment.

The cell also:

- chooses a Thai-capable font when one is installed;
- applies a white-grid Seaborn style;
- increases the maximum displayed columns and line width; and
- formats displayed numbers with commas and two decimal places.

These settings change presentation, not the underlying data.

#### File lookup and transformation

The code checks two possible locations for `SFD_SPB0801.csv`. If neither exists, it raises a helpful `FileNotFoundError`.

Then it:

1. reads the CSV into `raw_df`;
2. renames the long indicator column to `indicator`;
3. copies the result into `df`;
4. converts `value` to numeric with `errors='coerce'`; and
5. creates `year_ce` using `year - 543`.

`errors='coerce'` means that an unparseable value would become `NaN` instead of silently remaining text. The later quality checks show that no values failed conversion.

Finally, it defines:

```python
TOTAL_LABEL = 'รวมทั้งสิ้น'
```

This constant avoids repeating the Thai total label throughout the notebook.

#### Output

```text
Loaded: data/raw/SFD_SPB0801.csv
Shape: 3,388 rows x 10 columns
Years (B.E.): [2566]
Provinces: 77
```

The CSV originally has 9 columns. The added `year_ce` column makes 10 columns in `df`.

### Cell 2 — Section heading

This Markdown cell starts the data-quality section: “Basic data and data-quality checks.” It has no executable code.

### Cell 3 — Basic inspection and quality checks

This cell prints several checks.

#### First five rows

`df.head(5)` shows the first five records so the analyst can see the shape and labels of the data. The first records are for Bangkok and include different socioeconomic categories.

#### Counts by indicator

```python
df['indicator'].value_counts()
```

The output shows 847 rows for each of the four indicators:

| Indicator | Rows |
|---|---:|
| Total monthly income | 847 |
| Total monthly expenses | 847 |
| Average total household debt | 847 |
| Expenses as a percentage of income | 847 |

Equal counts are a useful first sign that the table is structured consistently.

#### Duplicate checks

Two duplicate checks are performed:

- `df.duplicated()` checks whether complete rows repeat.
- `df.duplicated(subset=[...])` checks whether the expected key fields repeat.

Both results are zero. The key is made from year, province, indicator, and the two socioeconomic categories.

#### Missing values

The only substantial missingness is in `attribute`:

- `attribute`: 3,266 missing values
- every core column: 0 missing values

The `attribute` field is optional metadata, not the measurement itself.

#### Units, numeric conversion, notes, and zeros

The output shows:

- units: `บาท` and `ร้อยละ`;
- numeric parsing failures in `value`: 0;
- rows with an NSO attribute note: 122; and
- values equal to zero: 122.

The notes explain that some zero values are zero estimates from the sample survey. A zero should therefore not automatically be treated as a missing value or a coding error.

### Cell 4 — Explanation of missing `attribute` values

This Markdown cell clarifies that missing attributes are expected. NSO only attaches a note to selected observations. The important analysis fields have no missing values after conversion.

### Cell 5 — Inspect data types and make data-type charts

This cell builds `dtype_table` with three pieces of information for every column:

- the pandas data type;
- the number of non-null values; and
- the number of distinct non-null values.

The main results are:

- `year` and `year_ce` are integers;
- text columns are represented as strings;
- `value` is `float64` for all 3,388 rows; and
- `attribute` is present on only 122 rows.

It then maps each item in `value` to its Python type and counts the results. Every value is a Python `float`, confirming that numeric conversion worked.

The two charts show:

1. how many columns have each pandas data type; and
2. how many rows contain each Python type in `value`.

These charts are simple visual versions of the printed type checks.

### Cell 6 — Plot row counts by indicator and unit

This cell creates two bar charts:

1. row counts for each indicator; and
2. row counts for each unit.

The first chart visually confirms the balanced 847-row count for each indicator. The second shows the mixture of baht-valued and percentage-valued observations. It is a quick way to check that the dataset contains both monetary and percentage measures and that the units should not be mixed in one calculation.

### Cell 7 — Section heading for provincial preparation

This Markdown cell begins the preparation step. It explains that the notebook will use the rows where both socioeconomic fields are `รวมทั้งสิ้น`, then pivot the indicators into separate columns.

A **pivot** changes a long table, where the indicator is stored as a value in one column, into a wide table, where each indicator gets its own column.

### Cell 8 — Select total rows, pivot indicators, and assign regions

#### Select the overall provincial scope

```python
total_scope = df.loc[
    (df['soc_eco_class1'] == TOTAL_LABEL)
    & (df['soc_eco_class2'] == TOTAL_LABEL)
].copy()
```

This keeps the overall total for every province and every indicator. It produces:

```text
77 provinces × 4 indicators = 308 rows
```

This removes the detailed socioeconomic breakdown for the province-ranking and correlation analysis.

#### Pivot from long to wide format

The pivot uses year, converted year, and province as the row key. The indicator names become columns. The Thai indicator names are renamed to short English-style names:

- `income_monthly_baht`
- `expense_monthly_baht`
- `debt_average_baht`
- `expense_income_pct`

The result, `wide`, has one row per province, so it has 77 rows.

#### Define regions

The notebook creates `REGION_PROVINCES`, a hard-coded mapping of the 77 provinces into five analysis groups:

| Region label | Provinces |
|---|---:|
| Bangkok and 3 provinces | 4 |
| Central | 22 |
| North | 17 |
| Northeast | 20 |
| South | 14 |

It then reverses that dictionary into `province_to_region` and maps each province to a region. A categorical data type preserves the intended region order in later output and plots.

#### Assertions

The `assert` statements stop execution if an important assumption fails. They check that:

- the total scope has exactly 308 rows;
- there are 77 unique provinces;
- all four required measures are present for every province; and
- every province received a region.

The final printed output confirms the expected counts.

### Cell 9 — Section heading for rankings

This Markdown cell introduces the province and region ranking section.

### Cell 10 — Rank provinces, summarize regions, and plot regional results

#### Province rankings

`nlargest(10, ...)` prints two lists:

- the 10 provinces with the largest average household debt; and
- the 10 provinces with the largest monthly total household income.

The displayed columns are province, region, income, debt, and expense-to-income percentage.

The most important entries are:

**Top debt provinces**

| Rank | Province | Income (baht/month) | Debt (baht) | Expenses/income |
|---:|---|---:|---:|---:|
| 1 | Phuket | 41,865 | 424,977 | 93.02% |
| 2 | Pathum Thani | 45,729 | 362,493 | 78.73% |
| 3 | Amnat Charoen | 28,515 | 337,610 | 79.61% |
| 4 | Ratchaburi | 31,368 | 314,967 | 84.28% |
| 5 | Krabi | 28,360 | 314,717 | 86.52% |
| 6 | Phetchabun | 27,717 | 309,224 | 75.43% |
| 7 | Nakhon Ratchasima | 27,775 | 303,257 | 77.77% |
| 8 | Surin | 22,216 | 290,152 | 82.29% |
| 9 | Mukdahan | 24,925 | 285,176 | 78.03% |
| 10 | Chon Buri | 35,981 | 282,402 | 88.06% |

**Top income provinces**

| Rank | Province | Income (baht/month) | Debt (baht) | Expenses/income |
|---:|---|---:|---:|---:|
| 1 | Pathum Thani | 45,729 | 362,493 | 78.73% |
| 2 | Chanthaburi | 43,857 | 248,280 | 62.30% |
| 3 | Phuket | 41,865 | 424,977 | 93.02% |
| 4 | Bangkok | 40,051 | 161,050 | 81.74% |
| 5 | Nonthaburi | 36,767 | 267,543 | 85.21% |
| 6 | Chon Buri | 35,981 | 282,402 | 88.06% |
| 7 | Phra Nakhon Si Ayutthaya | 33,919 | 231,845 | 78.84% |
| 8 | Saraburi | 33,894 | 254,307 | 80.29% |
| 9 | Surat Thani | 33,523 | 225,020 | 78.61% |
| 10 | Nakhon Si Thammarat | 33,414 | 268,956 | 69.04% |

The ranking is based on the published provincial averages. It is not a ranking of total provincial debt, because the notebook does not have the number of households needed to calculate that.

#### Regional summary

The `groupby('region')` operation calculates, for each region:

- the number of provinces;
- the arithmetic mean of provincial monthly income averages;
- the arithmetic mean of provincial debt averages; and
- the arithmetic mean of provincial expense-to-income percentages.

The output is:

| Region | Provinces | Mean income (baht/month) | Mean debt (baht) | Mean expenses/income |
|---|---:|---:|---:|---:|
| Bangkok and 3 provinces | 4 | 38,702.50 | 250,762.00 | 82.62% |
| Northeast | 20 | 22,889.55 | 208,481.00 | 83.56% |
| South | 14 | 27,514.00 | 200,481.21 | 83.21% |
| North | 17 | 23,155.29 | 190,497.12 | 79.44% |
| Central | 22 | 29,309.82 | 173,033.45 | 80.40% |

Although the code calls this a “regional summary,” it is specifically a **simple mean of provincial averages**. A region with many households does not automatically receive more weight than a region with fewer households.

#### Regional charts

The final part of the cell draws two horizontal bar charts:

- average household debt by region; and
- monthly household income by region.

The data is sorted separately for each chart so that the bars are easy to compare.

### Cell 11 — Explanation before calculating correlation

This Markdown cell gives the central statistical warning: the correlation is between province-level averages in one year. It can answer whether higher-income provinces tend to have higher debt averages, but it cannot prove that income causes debt.

### Cell 12 — Calculate correlations and draw the income–debt plot

The cell selects two columns from `wide`:

```python
relationship_cols = ['income_monthly_baht', 'debt_average_baht']
```

It calculates two different types of correlation.

#### Pearson correlation

Pearson's `r` measures the strength and direction of a roughly linear relationship. The result is:

```text
Pearson correlation (n=77 provinces): 0.488
```

This is a positive, moderate association in this dataset: provinces with higher reported income often also have higher reported debt, but the relationship is far from perfect.

#### Spearman correlation

Spearman correlation compares the ranks rather than the raw distances between values. It is useful when the relationship is monotonic but not necessarily linear, or when extreme values may affect Pearson's result.

```text
Spearman rank correlation: 0.389
```

The lower value indicates that the income and debt rankings are not identical.

#### Overall means

The cell also prints unweighted means across the 77 provinces:

- mean monthly income: 26,445 baht;
- mean average debt: 195,125 baht.

These are not the same as a national household-weighted average.

#### Scatter plot and regression line

`seaborn.regplot` creates:

- one point per province;
- income on the horizontal axis;
- debt on the vertical axis; and
- a fitted straight regression line.

The three provinces with the largest debt values are annotated. The line is a visual summary of association, not a causal model or a prediction guarantee.

### Cell 13 — Section heading for socioeconomic groups

This Markdown cell introduces the detailed socioeconomic comparison. It explicitly warns that the results are averages for categories, not the categories' share of national income or debt.

### Cell 14 — Compare detailed socioeconomic groups

#### Create a detailed wide table

The code removes rows where `soc_eco_class2` is the total label, because this section is intended to compare detailed groups.

It then uses `pivot_table` with the key:

```text
province, soc_eco_class1, soc_eco_class2
```

The indicator names become columns. `aggfunc='first'` tells pandas to take the first value if duplicate combinations occur. The earlier duplicate checks found no duplicate key rows in the original table.

Only the income and debt columns are renamed because those are the two measures needed here.

#### Average each group across provinces

The next `groupby` averages the income and debt values for each pair of socioeconomic labels. In other words, it asks:

> Among the provinces where this category is reported, what is the average published income and debt value for the category?

It does not use household counts as weights.

The code builds `category_label` by joining the broad and detailed labels. `textwrap.fill` wraps long Thai labels so they fit on the chart.

#### Top five output

For average monthly income, the top five groups are:

| Rank | Broad group | Detailed group | Income (baht/month) | Debt (baht) |
|---:|---|---|---:|---:|
| 1 | Employees | Managers, academics, and professionals | 48,292.91 | 558,901.04 |
| 2 | Non-agricultural self-employed | Non-agricultural self-employed | 33,298.61 | 264,960.21 |
| 3 | Agricultural/aquaculture holders | Mostly landowners | 27,264.10 | 187,962.10 |
| 4 | Employees | Clerical, sales, and service workers | 25,684.36 | 180,260.87 |
| 5 | Agricultural/aquaculture holders | Mostly tenants or free users | 24,063.81 | 239,350.51 |

For average debt, the same five groups appear, ordered slightly differently:

| Rank | Broad group | Detailed group | Income (baht/month) | Debt (baht) |
|---:|---|---|---:|---:|
| 1 | Employees | Managers, academics, and professionals | 48,292.91 | 558,901.04 |
| 2 | Non-agricultural self-employed | Non-agricultural self-employed | 33,298.61 | 264,960.21 |
| 3 | Agricultural/aquaculture holders | Mostly tenants or free users | 24,063.81 | 239,350.51 |
| 4 | Agricultural/aquaculture holders | Mostly landowners | 27,264.10 | 187,962.10 |
| 5 | Employees | Clerical, sales, and service workers | 25,684.36 | 180,260.87 |

The parent and child labels come directly from the NSO classification. They should not be rearranged based only on how the labels sound in English.

#### Charts

Two horizontal bar charts show the top five groups:

- top groups by average monthly income; and
- top groups by average household debt.

### Cell 15 — Written summary and limitations

This Markdown cell summarizes what the first five sections can answer and repeats the major limitations:

- there are no individual household income or debt records;
- there are no household counts for weighting in the main CSV;
- there is only one year; and
- the main file does not identify income sources or debt purposes.

It points toward the supplementary survey tables for those additional questions.

### Cell 16 — Print a compact list of key findings

This cell finds the maximum row or label in each prepared summary:

- `idxmax()` finds the province with the largest income or debt;
- another `idxmax()` finds the region with the largest mean provincial value; and
- the same operation finds the detailed group with the largest average income or debt.

It prints:

```text
Highest-debt province: ภูเก็ต (424,977 baht)
Highest-income province: ปทุมธานี (45,729 baht/month)
Highest-debt region: กรุงเทพมหานครและ 3 จังหวัด
Highest-income region: กรุงเทพมหานครและ 3 จังหวัด
Highest-income detailed group: ผู้จัดการนักวิชาการและผู้ปฏิบัติงานวิชาชีพ
Highest-debt detailed group: ผู้จัดการนักวิชาการและผู้ปฏิบัติงานวิชาชีพ
Province-level Pearson correlation: 0.488
```

This is a convenient text summary of results already calculated in earlier cells; it does not introduce a new analysis.

### Cell 17 — Introduce supplementary NSO tables

This Markdown cell lists the additional local snapshots. The important distinction is geographic level:

- the three `SFD` provincial tables can be compared using province and socioeconomic keys;
- the `SES` tables are regional or administrative-area tables and should not be merged directly into the provincial table.

All supplementary files kept in the repository are filtered to B.E. 2566 so that they match the main analysis year.

### Cell 18 — Load and inventory the supplementary data

#### Locate the supplementary directory

The code tries `data/raw` and `../data/raw`, then raises an error if neither directory exists.

#### Map logical names to filenames

The `supplementary_files` dictionary gives short names to the CSV files. This makes later code easier to read. For example:

```python
'income_source_province': 'SFD_SPB0802_66.csv'
```

A dictionary comprehension reads every file into `supplementary_data`, so each named item is a pandas DataFrame.

#### Handle inconsistent year-column capitalization

The NSO tables do not all use the same capitalization for their year field. The helper function:

```python
def year_column(frame):
    return next(column for column in ['year', 'Year', 'YEAR'] if column in frame.columns)
```

finds whichever spelling is present.

#### Build the inventory

For every supplementary table, the code records:

- its logical dataset name;
- its filename;
- number of rows and columns;
- the distinct years present;
- whether it is province-level or region/area-level; and
- the number of duplicate complete rows.

The inventory output is:

| Dataset | Rows | Columns | Level | Duplicate rows |
|---|---:|---:|---|---:|
| `SFD_SPB0802_66` | 7,700 | 11 | Province | 0 |
| `SFD_SPB0806` | 7,700 | 11 | Province | 0 |
| `SFD_SPB0807` | 7,700 | 11 | Province | 0 |
| `SES_OS_29_2566` | 18 | 6 | Region/area | 0 |
| `SES_OS_30_2566` | 234 | 8 | Region/area | 0 |
| `SES_OS_31_2566` | 72 | 7 | Region/area | 0 |
| `SES_41_01_2566` | 18 | 15 | Region/area | 0 |
| `SES_41_02_2566` | 11 | 13 | Region/area | 0 |
| `SES_41_03_2566` | 6 | 26 | Region/area | 0 |
| `SES_41_04_2566` | 11 | 26 | Region/area | 0 |
| `SES_41_05_2566` | 6 | 16 | Region/area | 0 |

The cell prints two sample rows from five important tables so the analyst can inspect their schemas and labels.

#### Assertions in this cell

The first loop asserts that every stored supplementary table contains exactly year 2566. The second check asserts that all three provincial supplementary tables contain exactly the same 77 province names as the base table.

The output confirms:

```text
All stored supplementary snapshots contain only B.E. 2566 rows.
All three provincial snapshots contain the same 77 provinces as SFD_SPB0801.
```

The other `SES_41_*` tables are loaded and checked for year/geography consistency, but they are not all used in later calculations.

### Cell 19 — Cross-check overlapping provincial indicators

This code tests whether the original `SFD_SPB0801` values agree with related provincial snapshots.

#### Build a common comparison key

```python
comparison_key = ['province', 'soc_eco_class1', 'soc_eco_class2']
```

The year is not included because every stored snapshot is already restricted to B.E. 2566.

#### Compare income

From the base table, the code selects:

- the total monthly income indicator; and
- rows whose broad socioeconomic class is not the overall total.

From `SFD_SPB0802_66`, it selects rows where `source_income3` equals total monthly income. Both sides are renamed to `current_value` and `source_value`, then combined with an outer merge.

An **outer merge** keeps every key from either table. This means missing keys would be visible instead of being silently discarded. The `_merge` column records whether a key appeared on the left, right, or both sides.

The absolute difference is calculated as:

```text
absolute difference = |current value − source value|
```

Results:

- 770 overlapping income keys;
- 0 unmatched keys;
- 769 exact matches; and
- 1 mismatch.

The mismatch is:

| Province | Detailed group | Base value | Supplementary value | Difference |
|---|---|---:|---:|---:|
| Samut Sakhon (`สมุทรสาคร`) | Mostly tenant/free agricultural category | 600 | -600 | 1,200 |

The notebook keeps both published values and reports the discrepancy. It does not silently choose one or overwrite the source data.

#### Compare debt

The same approach compares:

- the base indicator `หนี้สินเฉลี่ยต่อครัวเรือนทั้งสิ้น`; and
- rows in `SFD_SPB0806` where `purpose_source_bor` is `จำนวนหนี้สินเฉลี่ยต่อครัวเรือน`.

Results:

- 770 overlapping debt keys;
- 0 unmatched keys;
- 770 exact matches; and
- 0 debt mismatches.

The `assert` statements enforce the expected 770-key structure and require no debt mismatch. The income mismatch is intentionally reported rather than treated as a failure.

#### Check negative income-source values

The code counts negative values in the entire provincial income-source table and finds 36. Negative values can be meaningful for fields that represent **net** agricultural or business profit. They are retained for review instead of automatically being changed to zero or removed.

This is a data interpretation warning: a negative net-income component is not necessarily a corrupt CSV value.

### Cell 20 — Heading for income sources

This Markdown cell explains that `SES_41_01` contains regional and administrative-area income data. The notebook chooses the Thailand-wide row so it does not calculate a second average across overlapping regional categories.

### Cell 21 — Break down Thailand's household income

#### Select the national row

The code copies `SES_41_01` and selects the row where:

- `REGION == 'ทั่วราชอาณาจักร'` — whole kingdom / Thailand total; and
- `AREA == 'เขตการปกครอง'` — the administrative-area total used by this table.

`.iloc[0]` takes the first matching row.

#### Select income components

The dictionary maps readable Thai descriptions to source columns:

| Description | Source column |
|---|---|
| Income from work | `FROM_WORK` |
| Current transfers/support | `CURRENT_TRANSFER` |
| Property income | `PROPERTY_INCOME` |
| Non-money income | `NONMONEY_INCOME` |
| Irregular monetary income | `NONCUR_M_INCOME` |

The resulting series is sorted from largest to smallest. Each component's share is calculated as:

```text
component share (%) = component amount / MONTHLY_INCOME × 100
```

The output is:

| Component | Baht/month | Share of monthly income |
|---|---:|---:|
| Income from work | 20,465 | 70.50% |
| Non-money income | 4,205 | 14.49% |
| Current transfers/support | 3,794 | 13.07% |
| Irregular monetary income | 325 | 1.12% |
| Property income | 242 | 0.83% |
| **Total monthly income field** | **29,030** | — |

The component amounts add to 29,031 while the published total is 29,030. The one-baht difference is consistent with rounding in component values. The notebook reports the source values rather than forcing them to reconcile.

The bar chart displays the same five components, with baht per month on the horizontal axis.

### Cell 22 — Heading for indebted households and debt purpose

This Markdown cell explains that `SES_OS_29` through `SES_OS_31` count **households**, not baht of debt. They can describe how many households report a kind of debt or purpose, but they do not measure the size of those debts.

### Cell 23 — Analyze indebted-household counts, sources, purposes, and types

#### Copy the three debt-count tables

The code makes working copies of:

- `SES_OS_29_2566`: number of indebted households;
- `SES_OS_30_2566`: indebted households by loan source and purpose; and
- `SES_OS_31_2566`: indebted households by debt type.

It strips leading and trailing whitespace from the text columns. This matters because some CSV labels contain spaces around values such as `หนี้ในระบบ` and `รวม`.

#### Total number of indebted households

The code selects the Thailand-wide, all-area total from `SES_OS_29_2566`:

```text
11,472,172 households
```

#### Purpose by loan source

For `SES_OS_30_2566`, it selects the Thailand-wide, all-area rows and removes subtotal rows where either source or purpose equals `รวม`.

The detailed output is:

| Loan source | Purpose | Households |
|---|---|---:|
| Formal debt (`หนี้ในระบบ`) | Household consumption and other expenses | 7,728,981 |
| Formal debt | Agriculture | 2,786,637 |
| Formal debt | Buying/financing a house and/or land | 1,638,465 |
| Formal debt | Business | 933,037 |
| Informal debt (`หนี้นอกระบบ`) | Household consumption and other expenses | 613,890 |
| Formal debt | Education | 417,894 |
| Informal debt | Business | 131,782 |
| Informal debt | Agriculture | 69,740 |
| Formal debt | Other | 53,400 |
| Informal debt | Buying/financing a house and/or land | 30,994 |
| Informal debt | Education | 19,162 |
| Informal debt | Other | 12,419 |

The code groups by `Source_loan` and uses `idxmax()` to find the largest purpose within each source. Household consumption is the largest purpose for both:

- formal debt: 7,728,981 households;
- informal debt: 613,890 households.

These purpose values should **not** automatically be added together to estimate a unique total number of households. One household may have more than one purpose and may have both formal and informal debt.

#### Debt type

The code selects Thailand-wide, all-area rows from `SES_OS_31_2566` and removes the overall total row. The output is:

| Debt type | Households |
|---|---:|
| Formal debt only | 10,613,594 |
| Informal debt only | 548,804 |
| Both formal and informal debt | 309,774 |

These three categories sum to 11,472,172, matching the total number of indebted households in the output.

#### Charts

The first chart is a grouped bar chart of indebted households by purpose and loan source. The second is a bar chart of indebted households by debt type. Both charts show **counts of households**, not debt balances.

### Cell 24 — Final scope and comparability note

This Markdown cell summarizes the final data boundary:

- all stored tables are B.E. 2566 snapshots;
- provincial supplementary tables contain the same 77 provinces as the base table;
- regional/administrative-area tables are kept separate from province-level joins; and
- one income value differs between two published snapshots.

It states the important reproducibility principle: preserve and report source differences instead of silently correcting them.

### Cell 25 — Final automated checks

The last code cell prints a compact audit:

- base-table year: `[2566]`;
- supplementary years: `[2566]`;
- current province count: `77`;
- province counts in the three provincial supplementary tables: `[77, 77, 77]`; and
- regional supplementary tables are kept as separate B.E. 2566 snapshots.

This cell is a final confirmation of year alignment and geographic coverage. It does not recalculate the earlier rankings.

---

## 6. How to interpret the findings correctly

### The positive income–debt relationship

A Pearson correlation of 0.488 means that the provincial averages move together to some degree: higher-income provinces tend to have higher average debt. It does **not** mean:

- an extra baht of income causes a particular amount of debt;
- every household in a high-income province has high debt;
- debt causes income; or
- the relationship would be the same in another year.

Many factors could affect both measures, including housing costs, land prices, urbanization, business structure, employment, tourism, and access to credit. The notebook does not model those factors.

### The highest province is not necessarily “the most indebted population”

Phuket has the highest **average debt per household** in the base table. Without the number of households and a total debt measure, the notebook cannot say that Phuket has the largest total amount of household debt in Thailand.

Similarly, Pathum Thani has the highest reported average monthly household income; this is not a statement about every household or total provincial income.

### Regional means are unweighted

The Bangkok-and-3-provinces group has the highest simple mean in both income and debt. Its result is the average of four provincial averages. A household-weighted calculation could produce a different ranking, but the required household counts are not available in the main CSV.

### Socioeconomic-group results are category averages

The managers/academics/professionals group has the highest average income and debt among the detailed categories used. This does not tell us:

- how many households belong to that group;
- its share of national income or debt;
- the total debt held by the group; or
- why the group has that debt.

### Supplementary debt-purpose results are counts

The supplementary debt-purpose tables identify how many indebted households report each source/purpose combination. They do not provide:

- the baht value of the debt;
- the interest rate;
- the number of loans; or
- a causal explanation for borrowing.

---

## 7. Limitations and possible extensions

The notebook is useful for exploration and quality checking, but it has clear boundaries:

1. **One year only.** It cannot identify trends or changes over time.
2. **Aggregated data.** It has province/category averages, not household-level observations.
3. **No weights in the main file.** Regional means are unweighted means of provincial averages.
4. **No causal analysis.** Correlation and a regression line describe association only.
5. **No uncertainty estimates.** The notebook does not calculate survey standard errors or confidence intervals.
6. **Different measures are kept distinct.** Average debt, number of indebted households, and debt-purpose counts are not interchangeable.
7. **Source categories may overlap.** Purpose counts and formal/informal source counts should not be assumed to be mutually exclusive household counts.
8. **Some source values can be negative.** Net agricultural or business income components need domain-aware interpretation.
9. **One published discrepancy remains.** The Samut Sakhon category is `600` in `SFD_SPB0801` and `-600` in `SFD_SPB0802_66`; both are preserved.
10. **Several supplementary tables are only inventoried.** `SES_41_02` through `SES_41_05` are loaded and year-checked, but the current notebook does not yet analyze their socioeconomic, distribution, or quintile columns.

Useful future extensions would include multiple years, household-count weights, confidence intervals, a direct analysis of the unused income-distribution/quintile tables, and models that include economic and demographic controls.

---

## 8. Data provenance

The project README contains the full source list. The principal sources referenced by the notebook are:

- [data.go.th dataset 0705_08_0031](https://data.go.th/dataset/0705_08_0031)
- [NSO `SFD_SPB0801` CSV](https://catalogapi.nso.go.th/api/index?table=SFD_SPB0801&format=csv)
- [NSO Income and Income Distribution 2023, Table 3](https://www.nso.go.th/public/e-book/Analytical-Reports/Income-2566/47/)
- [NSO Income and Income Distribution 2023, Table 16](https://www.nso.go.th/public/e-book/Analytical-Reports/Income-2566/94/)

The supplementary files are downloaded from the NSO Catalog API using URLs of this form:

```text
https://catalogapi.nso.go.th/api/index?table=<TABLE_NAME>&format=csv
```

The local snapshots and the download/filtering logic are documented in [`scripts/fetch_nso_2566_data.py`](../scripts/fetch_nso_2566_data.py).
