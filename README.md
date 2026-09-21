# Household Income and Debt Analysis

การสำรวจข้อมูลรายได้และหนี้สินครัวเรือนระดับจังหวัดของประเทศไทยจากสำนักงานสถิติแห่งชาติ (NSO) ปี พ.ศ. 2566 (ค.ศ. 2023)

## Contents

- `household_income_debt_analysis.ipynb` — notebook ตรวจสอบคุณภาพข้อมูลและวิเคราะห์เชิงสำรวจ โดยใช้ CSV แหล่งเดียวในขณะนี้
- `household_debt_model.ipynb` — notebook โมเดล Ridge สำหรับประมาณหนี้สินเฉลี่ยระดับจังหวัดด้วย 5-fold cross-validation
- `docs/household_income_debt_analysis_results.md` — ผลการวิเคราะห์ฉบับแยกจาก notebook
- `data/raw/SFD_SPB0801.csv` — แหล่งข้อมูลที่ notebook ใช้งานอยู่
- `data/raw/` — ตารางเสริมที่เก็บไว้สำหรับการวิเคราะห์ในอนาคต แต่ยังไม่ถูกโหลดโดย notebook รุ่นนี้
- `backups/household_income_debt_analysis_before_single_source.ipynb` — สำเนา notebook รุ่นเดิมก่อนลดเหลือแหล่งข้อมูลเดียว
- `scripts/fetch_nso_2566_data.py` — ดาวน์โหลดทรัพยากร NSO และกรองให้เหลือปี พ.ศ. 2566
- `scripts/extend_household_notebook.py` — สคริปต์เสริมสำหรับเพิ่มการวิเคราะห์ชุดข้อมูลอื่นเมื่อขยายขอบเขตในอนาคต
- `requirements.txt` — dependencies สำหรับ environment และการรัน notebook

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook household_income_debt_analysis.ipynb
```

## Current findings (single source)

ผลลัพธ์ฉบับเต็มอยู่ใน [`docs/household_income_debt_analysis_results.md`](docs/household_income_debt_analysis_results.md)

จากแถว `รวมทั้งสิ้น` ระดับจังหวัดใน `SFD_SPB0801.csv`:

- มีข้อมูล 3,388 แถว ครอบคลุม 77 จังหวัด 4 ตัวชี้วัด และไม่พบแถวซ้ำ
- Pearson correlation ระหว่างรายได้รวมต่อเดือนกับหนี้สินเฉลี่ยระดับจังหวัดเท่ากับประมาณ `0.488` (Spearman `0.389`) ซึ่งเป็นความสัมพันธ์เชิงบวกระดับปานกลางในข้อมูลแบบ cross-sectional ไม่ใช่หลักฐานเชิงเหตุผล
- จังหวัดที่มีหนี้สินเฉลี่ยสูงสุดคือภูเก็ต (`424,977` บาท)
- จังหวัดที่มีรายได้รวมเฉลี่ยต่อเดือนสูงสุดคือปทุมธานี (`45,729` บาท/เดือน)
- หากสรุปเป็นค่าเฉลี่ยแบบไม่ถ่วงน้ำหนักของค่าเฉลี่ยจังหวัด กลุ่ม “กรุงเทพมหานครและ 3 จังหวัด” สูงสุดทั้งด้านรายได้และหนี้สิน
- ในหมวดหมู่สถานะทางเศรษฐสังคมย่อย กลุ่มผู้จัดการ นักวิชาการ และผู้ปฏิบัติงานวิชาชีพมีค่าเฉลี่ยรายได้และหนี้สินสูงสุด แต่ข้อมูลนี้ไม่ได้วัดสัดส่วนหรือยอดรวมของรายได้/หนี้สิน และไม่ได้บอกวัตถุประสงค์ของหนี้

## Current data boundary

The active notebook intentionally reads only `data/raw/SFD_SPB0801.csv`. The supplementary snapshots remain available in `data/raw/` but are not part of the current result. The old extended notebook is preserved in `backups/` before this change.

## Time-period and data-quality note

The active analysis contains B.E. 2566 data only. It uses province/category averages rather than household-level observations, and keeps the source values as published. See the separate [results report](docs/household_income_debt_analysis_results.md) for the quality checks and interpretation limits.

## Sources

- [data.go.th dataset 0705_08_0031](https://data.go.th/dataset/0705_08_0031)
- [NSO CSV resource: SFD_SPB0801](https://catalogapi.nso.go.th/api/index?table=SFD_SPB0801&format=csv)
The supplementary source links are retained in `scripts/fetch_nso_2566_data.py` for possible future analysis; they are not used by the current notebook.
