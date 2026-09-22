"""Extract B.E. 2568 province-total income, expenditure, and debt from NSO.

The 2025 Household Socio-Economic Survey full report publishes Table C.1 with
one row per Thai province.  It does not publish province-by-socioeconomic-class
figures, so this extractor emits only total provincial metrics compatible with
the corresponding scope of the debt-analysis notebook.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = ROOT / "data" / "raw"
REPORT_URL = "https://www.nso.go.th/nsoweb/storage/survey_detail/2026/20260505141117_96690.pdf"
REPORT_PATH = RAW_DATA_DIR / "nso_household_socioeconomic_survey_2568_full_report.pdf"
OUTPUT_PATH = RAW_DATA_DIR / "nso_household_income_debt_province_2568.csv"
TABLE_C1_PAGE_INDEXES = range(188, 192)  # PDF pages 165–168, zero-indexed.
YEAR_BE = 2568
TOTAL_LABEL = "รวมทั้งสิ้น"
NUMBER_PATTERN = re.compile(r"\d[\d,]*(?:\.\d+)?")


def download_report(refresh: bool) -> None:
    """Download the official report once, preserving the raw PDF locally."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if REPORT_PATH.exists() and not refresh:
        return

    request = Request(REPORT_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=120) as response:
        REPORT_PATH.write_bytes(response.read())


def normalize_thai(text: str) -> str:
    """Repair spacing artifacts introduced by PDF text extraction."""
    return (
        text.replace("ก า", "กำ")
        .replace("ล า", "ลำ")
        .replace("อ า", "อำ")
    )


def province_names() -> list[str]:
    """Use the existing NSO province spelling as the canonical join key."""
    source = pd.read_csv(RAW_DATA_DIR / "SFD_SPB0801.csv")
    return sorted(source["province"].unique().tolist())


def values_for_province(table_text: str, province: str) -> list[float]:
    """Read household count, size, income, expenditure, and debt from one row."""
    for line in table_text.splitlines():
        line = normalize_thai(line).strip()
        if not line.startswith(province):
            continue

        suffix = line[len(province):]
        if not re.match(r"\s+" + NUMBER_PATTERN.pattern, suffix):
            continue
        values = [float(token.replace(",", "")) for token in NUMBER_PATTERN.findall(suffix)]
        if len(values) >= 5:
            return values[:5]

    raise ValueError(f"Could not extract Table C.1 values for {province}")


def build_extract() -> pd.DataFrame:
    reader = PdfReader(REPORT_PATH)
    table_text = "\n".join(
        reader.pages[page_index].extract_text() or ""
        for page_index in TABLE_C1_PAGE_INDEXES
    )
    if "Table C.1 Average Monthly Income Expenditure and Debt per Household and Province" not in table_text:
        raise ValueError("Could not locate Table C.1 in the downloaded report")

    records = []
    for province in province_names():
        households, household_size, income, expense, debt = values_for_province(table_text, province)
        records.append({
            "province": province,
            "total_households": households,
            "average_household_size": household_size,
            "income_monthly_baht": income,
            "expense_monthly_baht": expense,
            "debt_average_baht": debt,
        })

    totals = pd.DataFrame(records)
    if len(totals) != 77 or totals["province"].nunique() != 77:
        raise ValueError("Table C.1 extraction must contain exactly 77 distinct provinces")
    if totals.isna().any().any():
        raise ValueError("Missing values found in Table C.1 extraction")

    source_label = "สำนักงานสถิติแห่งชาติ (การสำรวจภาวะเศรษฐกิจและสังคมของครัวเรือน พ.ศ. 2568, ตาราง ค.1)"
    rows = []
    for record in totals.to_dict("records"):
        metrics = [
            ("รายได้ทั้งสิ้นต่อเดือน", record["income_monthly_baht"], "บาท", None),
            ("ค่าใช้จ่ายทั้งสิ้นต่อเดือน", record["expense_monthly_baht"], "บาท", None),
            ("หนี้สินเฉลี่ยต่อครัวเรือนทั้งสิ้น", record["debt_average_baht"], "บาท", None),
            (
                "ร้อยละของค่าใช้จ่ายต่อรายได้",
                record["expense_monthly_baht"] / record["income_monthly_baht"] * 100,
                "ร้อยละ",
                "คำนวณจากค่าใช้จ่ายทั้งสิ้นต่อเดือนหารด้วยรายได้ทั้งสิ้นต่อเดือน × 100",
            ),
        ]
        for indicator, value, unit, attribute in metrics:
            rows.append({
                "year": YEAR_BE,
                "province": record["province"],
                "mthincome_mthexp_totaldebt_pctexptoincome": indicator,
                "soc_eco_class1": TOTAL_LABEL,
                "soc_eco_class2": TOTAL_LABEL,
                "value": value,
                "unit": unit,
                "attribute": attribute,
                "source": source_label,
                "total_households": record["total_households"],
                "average_household_size": record["average_household_size"],
            })

    return pd.DataFrame(rows).sort_values(["province", "mthincome_mthexp_totaldebt_pctexptoincome"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-download the official PDF even when a local copy exists.",
    )
    args = parser.parse_args()

    download_report(refresh=args.refresh)
    extract = build_extract()
    extract.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print(f"Raw official report: {REPORT_PATH}")
    print(f"Province-total extract: {OUTPUT_PATH}")
    print(f"Shape: {extract.shape[0]:,} rows x {extract.shape[1]:,} columns")
    print(f"Years (B.E.): {sorted(extract['year'].unique().tolist())}")
    print(f"Provinces: {extract['province'].nunique()}")
    print("All rows represent the provincial total; socioeconomic-group detail is not available at province level.")


if __name__ == "__main__":
    main()
