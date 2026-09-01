"""Download the complementary NSO tables and keep only B.E. 2566 rows.

The catalog API blocks requests without a browser-like User-Agent, so the
script downloads through urllib and stores local CSV snapshots for the
notebook.  Provincial tables are retained at province level; regional tables
are retained at their original regional/urban-area level.
"""

from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd


TARGET_YEAR = 2566
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = REPOSITORY_ROOT / "data" / "raw"
API_TEMPLATE = "https://catalogapi.nso.go.th/api/index?table={table}&format=csv"

TABLES = {
    "SFD_SPB0802_66.csv": ("SFD_SPB0802_66", "year"),
    "SFD_SPB0806.csv": ("SFD_SPB0806", "year"),
    "SFD_SPB0807.csv": ("SFD_SPB0807", "year"),
    "SES_OS_29_2566.csv": ("SES_OS_29", "Year"),
    "SES_OS_30_2566.csv": ("SES_OS_30", "Year"),
    "SES_OS_31_2566.csv": ("SES_OS_31", "Year"),
    "SES_41_01_2566.csv": ("SES_41_01", "YEAR"),
    "SES_41_02_2566.csv": ("SES_41_02", "YEAR"),
    "SES_41_03_2566.csv": ("SES_41_03", "YEAR"),
    "SES_41_04_2566.csv": ("SES_41_04", "YEAR"),
    "SES_41_05_2566.csv": ("SES_41_05", "YEAR"),
}


def download_csv(table: str) -> pd.DataFrame:
    request = Request(
        API_TEMPLATE.format(table=table),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urlopen(request, timeout=120) as response:
        return pd.read_csv(BytesIO(response.read()))


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename, (table, year_column) in TABLES.items():
        source_df = download_csv(table)
        filtered_df = source_df.loc[source_df[year_column] == TARGET_YEAR].copy()

        if filtered_df.empty:
            raise ValueError(f"No B.E. {TARGET_YEAR} rows found in {table}")

        if set(filtered_df[year_column].unique()) != {TARGET_YEAR}:
            raise ValueError(f"Unexpected years found in filtered {table}")

        output_path = RAW_DATA_DIR / filename
        filtered_df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"{filename}: {len(filtered_df):,} rows, year {TARGET_YEAR}")


if __name__ == "__main__":
    main()
