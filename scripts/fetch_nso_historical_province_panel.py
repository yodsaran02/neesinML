"""Download and extract NSO's 2558–2566 provincial income/debt panel.

The NSO B.E. 2566 provincial report includes five survey waves in its
appendix: B.E. 2558, 2560, 2562, 2564, and 2566.  This script preserves the
nine official HTML appendix pages as raw inputs, extracts the provincial
values, and verifies that its 2566 income, expenditure, and debt values match
the repository's SFD_SPB0801 CSV before writing a panel CSV.
"""

from __future__ import annotations

import argparse
import re
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = ROOT / "data" / "raw"
SOURCE_DIR = RAW_DATA_DIR / "nso_income_2566_appendix_pages"
PANEL_PATH = RAW_DATA_DIR / "household_income_debt_province_panel_2558_2566.csv"
REPORT_URL = "https://www.nso.go.th/public/e-book/Analytical-Reports/Income-2566"
YEARS_BE = [2558, 2560, 2562, 2564, 2566]

# Each table spans three HTML pages in the e-book.
TABLE_PAGES = {
    "income_monthly_baht": [131, 132, 133],  # Appendix Table ผ 1
    "expense_monthly_baht": [137, 138, 139],  # Appendix Table ผ 3
    "debt_all_households": [146, 147, 148],  # Appendix Table ผ 6
}
NUMBER_PATTERN = re.compile(r"-?\d[\d,]*(?:\.\d+)?")


class PageTextExtractor(HTMLParser):
    """Collect visible text from an NSO FlippingBook page."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        text = " ".join(unescape(" ".join(self.parts)).split())
        # The HTML conversion occasionally duplicates the vowel after sara am,
        # e.g. "กำ าแพงเพชร" instead of "กำแพงเพชร".
        return text.replace("ำ า", "ำ")


def download_page(page: int, refresh: bool) -> str:
    """Return normalized page text and retain its official HTML source."""
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    page_path = SOURCE_DIR / f"page_{page}.html"

    if refresh or not page_path.exists():
        request = Request(
            f"{REPORT_URL}/{page}/",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urlopen(request, timeout=120) as response:
            page_path.write_bytes(response.read())

    parser = PageTextExtractor()
    parser.feed(page_path.read_text(encoding="utf-8-sig"))
    return parser.text()


def parse_number(token: str) -> float:
    return float(token.replace(",", ""))


def province_values(text: str, province: str, count: int) -> list[float]:
    """Extract the first `count` numbers immediately following a province row."""
    for match in re.finditer(re.escape(province), text):
        suffix = text[match.end():]
        if not re.match(r"\s+" + NUMBER_PATTERN.pattern, suffix):
            continue
        values = [parse_number(token) for token in NUMBER_PATTERN.findall(suffix[:400])]
        if len(values) >= count:
            return values[:count]
    raise ValueError(f"Could not extract {count} values for {province}")


def extract_table(table_name: str, provinces: list[str], refresh: bool) -> dict[str, list[float]]:
    page_text = " ".join(download_page(page, refresh) for page in TABLE_PAGES[table_name])
    value_count = 10 if table_name == "debt_all_households" else 9
    extracted = {
        province: province_values(page_text, province, value_count)
        for province in provinces
    }
    if len(extracted) != 77:
        raise ValueError(f"Expected 77 provinces in {table_name}; found {len(extracted)}")
    return extracted


def current_2566_totals() -> pd.DataFrame:
    """Return the current notebook's total-scope provincial values for checking."""
    current = pd.read_csv(RAW_DATA_DIR / "SFD_SPB0801.csv")
    current = current.rename(columns={"mthincome_mthexp_totaldebt_pctexptoincome": "indicator"})
    current["value"] = pd.to_numeric(current["value"], errors="raise")
    total = current.loc[
        (current["soc_eco_class1"] == "รวมทั้งสิ้น")
        & (current["soc_eco_class2"] == "รวมทั้งสิ้น")
    ]
    result = total.pivot(index="province", columns="indicator", values="value").reset_index()
    return result.rename(columns={
        "รายได้ทั้งสิ้นต่อเดือน": "income_monthly_baht",
        "ค่าใช้จ่ายทั้งสิ้นต่อเดือน": "expense_monthly_baht",
        "หนี้สินเฉลี่ยต่อครัวเรือนทั้งสิ้น": "debt_average_baht",
        "ร้อยละของค่าใช้จ่ายต่อรายได้": "expense_income_pct_source",
    })


def build_panel(refresh: bool) -> pd.DataFrame:
    current = current_2566_totals()
    provinces = current["province"].tolist()

    income = extract_table("income_monthly_baht", provinces, refresh)
    expense = extract_table("expense_monthly_baht", provinces, refresh)
    debt = extract_table("debt_all_households", provinces, refresh)

    rows = []
    for province in provinces:
        for index, year_be in enumerate(YEARS_BE):
            rows.append({
                "year_be": year_be,
                "year_ce": year_be - 543,
                "province": province,
                "income_monthly_baht": income[province][index],
                "expense_monthly_baht": expense[province][index],
                "pct_households_with_debt": debt[province][index],
                "debt_average_baht": debt[province][index + 5],
            })

    panel = pd.DataFrame(rows)
    panel["expense_income_pct"] = (
        panel["expense_monthly_baht"] / panel["income_monthly_baht"] * 100
    )

    if len(panel) != 77 * len(YEARS_BE):
        raise ValueError(f"Expected 385 province-year rows; found {len(panel)}")
    if panel.duplicated(["year_be", "province"]).any():
        raise ValueError("Duplicate province-year rows found")
    if panel.isna().any().any():
        raise ValueError("Missing values found in extracted panel")

    check = panel.loc[panel["year_be"] == 2566].merge(
        current,
        on="province",
        suffixes=("_report", "_csv"),
        validate="one_to_one",
    )
    comparison_summary = {}
    for metric in ["income_monthly_baht", "expense_monthly_baht", "debt_average_baht"]:
        absolute_difference = (
            check[f"{metric}_report"] - check[f"{metric}_csv"]
        ).abs()
        comparison_summary[metric] = {
            "different_provinces": int((absolute_difference > 0).sum()),
            "max_absolute_difference_baht": float(absolute_difference.max()),
        }
        if (absolute_difference > 1).any():
            differences = check.loc[
                absolute_difference > 1,
                ["province", f"{metric}_report", f"{metric}_csv"],
            ]
            raise ValueError(
                f"2566 {metric} differs from SFD_SPB0801 by more than one baht:\n{differences}"
            )

    ratio_difference = (check["expense_income_pct"] - check["expense_income_pct_source"]).abs()
    comparison_summary["expense_income_pct"] = {
        "different_provinces": int((ratio_difference > 0.01).sum()),
        "max_absolute_difference_percentage_points": float(ratio_difference.max()),
    }
    if (ratio_difference > 0.01).any():
        raise ValueError("Derived 2566 expense-to-income percentages differ from SFD_SPB0801 by over 0.01 points")

    panel.attrs["comparison_summary"] = comparison_summary
    return panel.sort_values(["year_be", "province"]).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-download the nine source HTML pages even if they are already stored.",
    )
    args = parser.parse_args()

    panel = build_panel(refresh=args.refresh)
    panel.to_csv(PANEL_PATH, index=False, encoding="utf-8-sig")

    print(f"Raw official pages: {SOURCE_DIR}")
    print(f"Panel: {PANEL_PATH}")
    print(f"Shape: {panel.shape[0]:,} rows x {panel.shape[1]:,} columns")
    print(f"Years (B.E.): {sorted(panel['year_be'].unique().tolist())}")
    print(f"Provinces: {panel['province'].nunique()}")
    print("2566 validation against SFD_SPB0801 (report values may be rounded to whole baht):")
    for metric, result in panel.attrs["comparison_summary"].items():
        print(f"- {metric}: {result}")


if __name__ == "__main__":
    main()
