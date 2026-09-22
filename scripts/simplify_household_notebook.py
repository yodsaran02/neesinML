"""Replace compact notebook expressions with easier-to-read equivalents."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "household_income_debt_analysis.ipynb"


def replace_source(cells, cell_id, old_text, new_text):
    """Replace one known block and stop if the notebook no longer matches."""
    source = cells[cell_id]["source"]
    if old_text not in source:
        raise ValueError(f"Expected code was not found in cell {cell_id}")
    cells[cell_id]["source"] = source.replace(old_text, new_text)


def main():
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    cells = {cell["id"]: cell for cell in notebook.cells}
    expected_ids = {"a56a7966", "e0345dbe", "974863f7", "a33f4282", "c3077f2e", "0eed0145"}
    missing_ids = expected_ids.difference(cells)
    if missing_ids:
        raise ValueError(f"Notebook layout changed; expected cells are missing: {sorted(missing_ids)}")

    replace_source(
        cells,
        "a56a7966",
        "from pathlib import Path\n\nimport numpy as np",
        "from pathlib import Path\nimport textwrap\n\nimport numpy as np",
    )
    replace_source(
        cells,
        "a56a7966",
        "sns.set_theme(style='whitegrid', context='notebook')\n"
        "pd.set_option('display.max_columns', 30)\n"
        "pd.set_option('display.width', 160)\n"
        "pd.set_option('display.float_format', lambda value: f'{value:,.2f}')",
        "def format_number(value):\n"
        "    return f'{value:,.2f}'\n\n\n"
        "sns.set_theme(style='whitegrid', context='notebook')\n"
        "pd.set_option('display.max_columns', 30)\n"
        "pd.set_option('display.width', 160)\n"
        "pd.set_option('display.float_format', format_number)",
    )
    replace_source(
        cells,
        "a56a7966",
        "data_path = next((path for path in data_path_candidates if path.exists()), None)\n"
        "if data_path is None:\n"
        "    raise FileNotFoundError('Could not find data/raw/SFD_SPB0801.csv. Run this notebook from the repository root.')\n\n"
        "raw_df = pd.read_csv(data_path)\n"
        "metric_column = 'mthincome_mthexp_totaldebt_pctexptoincome'\n"
        "df = raw_df.rename(columns={metric_column: 'indicator'}).copy()",
        "data_path = None\n"
        "for candidate_path in data_path_candidates:\n"
        "    if candidate_path.exists():\n"
        "        data_path = candidate_path\n"
        "        break\n\n"
        "if data_path is None:\n"
        "    raise FileNotFoundError('Could not find data/raw/SFD_SPB0801.csv. Run this notebook from the repository root.')\n\n"
        "raw_df = pd.read_csv(data_path)\n"
        "metric_column = 'mthincome_mthexp_totaldebt_pctexptoincome'\n"
        "df = raw_df.copy()\n"
        "df.rename(columns={metric_column: 'indicator'}, inplace=True)",
    )

    replace_source(
        cells,
        "e0345dbe",
        "dtype_table = pd.DataFrame({",
        "def get_type_name(value):\n"
        "    return type(value).__name__\n\n\n"
        "dtype_table = pd.DataFrame({",
    )
    replace_source(
        cells,
        "e0345dbe",
        "value_python_types = df['value'].map(type).map(lambda value_type: value_type.__name__).value_counts()",
        "value_type_names = df['value'].apply(get_type_name)\n"
        "value_python_types = value_type_names.value_counts()",
    )

    replace_source(
        cells,
        "974863f7",
        "province_to_region = {\n"
        "    province: region\n"
        "    for region, provinces in REGION_PROVINCES.items()\n"
        "    for province in provinces\n"
        "}",
        "province_to_region = {}\n"
        "for region, provinces in REGION_PROVINCES.items():\n"
        "    for province in provinces:\n"
        "        province_to_region[province] = region",
    )

    replace_source(
        cells,
        "a33f4282",
        "region_summary = (\n"
        "    wide.groupby('region', observed=True)\n"
        "    .agg(\n"
        "        provinces=('province', 'nunique'),\n"
        "        income_monthly_baht=('income_monthly_baht', 'mean'),\n"
        "        debt_average_baht=('debt_average_baht', 'mean'),\n"
        "        expense_income_pct=('expense_income_pct', 'mean'),\n"
        "    )\n"
        "    .sort_values('debt_average_baht', ascending=False)\n"
        ")",
        "region_groups = wide.groupby('region', observed=True)\n"
        "region_summary = region_groups.agg(\n"
        "    provinces=('province', 'nunique'),\n"
        "    income_monthly_baht=('income_monthly_baht', 'mean'),\n"
        "    debt_average_baht=('debt_average_baht', 'mean'),\n"
        "    expense_income_pct=('expense_income_pct', 'mean'),\n"
        ")\n"
        "region_summary = region_summary.sort_values('debt_average_baht', ascending=False)",
    )
    replace_source(
        cells,
        "a33f4282",
        "debt_region_order = region_summary.sort_values('debt_average_baht').index\n"
        "income_region_order = region_summary.sort_values('income_monthly_baht').index",
        "debt_region_order = region_summary['debt_average_baht'].sort_values().index\n"
        "income_region_order = region_summary['income_monthly_baht'].sort_values().index",
    )

    replace_source(
        cells,
        "c3077f2e",
        "relationship_cols = ['income_monthly_baht', 'debt_average_baht']\n"
        "pearson_r = wide[relationship_cols].corr(method='pearson').iloc[0, 1]\n"
        "spearman_r = wide[relationship_cols].rank().corr(method='pearson').iloc[0, 1]",
        "income = wide['income_monthly_baht']\n"
        "debt = wide['debt_average_baht']\n\n"
        "pearson_r = income.corr(debt)\n"
        "income_ranks = income.rank()\n"
        "debt_ranks = debt.rank()\n"
        "spearman_r = income_ranks.corr(debt_ranks)",
    )
    replace_source(
        cells,
        "c3077f2e",
        "print(f'Mean monthly income: {wide[\"income_monthly_baht\"].mean():,.0f} baht')\n"
        "print(f'Mean average debt: {wide[\"debt_average_baht\"].mean():,.0f} baht')",
        "print(f'Mean monthly income: {income.mean():,.0f} baht')\n"
        "print(f'Mean average debt: {debt.mean():,.0f} baht')",
    )

    replace_source(
        cells,
        "0eed0145",
        "class_summary['category_label'] = class_summary['soc_eco_class1'] + ': ' + class_summary['soc_eco_class2']\n"
        "class_summary['category_label'] = class_summary['category_label'].map(lambda label: __import__('textwrap').fill(str(label), width=38))",
        "class_summary['category_label'] = class_summary['soc_eco_class1'] + ': ' + class_summary['soc_eco_class2']\n"
        "class_summary['category_label'] = class_summary['category_label'].apply(textwrap.fill, width=38)",
    )

    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            cell.get("metadata", {}).pop("execution", None)

    nbformat.write(notebook, NOTEBOOK_PATH)
    print(f"Simplified: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
