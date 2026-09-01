# Household Income and Debt Analysis

การสำรวจข้อมูลรายได้และหนี้สินครัวเรือนระดับจังหวัดของประเทศไทยจากสำนักงานสถิติแห่งชาติ (NSO) ปี พ.ศ. 2566 (ค.ศ. 2023)

## Contents

- `household_income_debt_analysis.ipynb` — notebook ตรวจสอบคุณภาพข้อมูลและวิเคราะห์เชิงสำรวจ
- `data/raw/SFD_SPB0801.csv` — CSV จากทรัพยากร NSO ที่เชื่อมโยงโดย data.go.th
- `data/raw/SFD_SPB0802_66.csv` — รายได้จำแนกตามแหล่งที่มา ระดับจังหวัด
- `data/raw/SFD_SPB0806.csv` และ `data/raw/SFD_SPB0807.csv` — หนี้สินเฉลี่ยระดับจังหวัด ทั้งครัวเรือนและเฉพาะครัวเรือนที่เป็นหนี้
- `data/raw/SES_OS_29_2566.csv` ถึง `SES_OS_31_2566.csv` — จำนวนครัวเรือนที่เป็นหนี้ แหล่งเงินกู้ และประเภทหนี้ระดับภูมิภาค
- `data/raw/SES_41_01_2566.csv` ถึง `SES_41_05_2566.csv` — รายได้ การกระจายรายได้ และ quintile ระดับภูมิภาค/สถานะทางเศรษฐสังคม
- `scripts/fetch_nso_2566_data.py` — ดาวน์โหลดทรัพยากร NSO และกรองให้เหลือปี พ.ศ. 2566
- `scripts/extend_household_notebook.py` — สร้างส่วนวิเคราะห์ชุดข้อมูลเสริมใน notebook
- `requirements.txt` — dependencies สำหรับ environment และการรัน notebook

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook household_income_debt_analysis.ipynb
```

## Initial findings

จากแถว `รวมทั้งสิ้น` ระดับจังหวัดในไฟล์นี้:

- มีข้อมูล 3,388 แถว ครอบคลุม 77 จังหวัด 4 ตัวชี้วัด และไม่พบแถวซ้ำ
- Pearson correlation ระหว่างรายได้รวมต่อเดือนกับหนี้สินเฉลี่ยระดับจังหวัดเท่ากับประมาณ `0.488` (Spearman `0.389`) ซึ่งเป็นความสัมพันธ์เชิงบวกระดับปานกลางในข้อมูลแบบ cross-sectional ไม่ใช่หลักฐานเชิงเหตุผล
- จังหวัดที่มีหนี้สินเฉลี่ยสูงสุดคือภูเก็ต (`424,977` บาท)
- จังหวัดที่มีรายได้รวมเฉลี่ยต่อเดือนสูงสุดคือปทุมธานี (`45,729` บาท/เดือน)
- หากสรุปเป็นค่าเฉลี่ยแบบไม่ถ่วงน้ำหนักของค่าเฉลี่ยจังหวัด กลุ่ม “กรุงเทพมหานครและ 3 จังหวัด” สูงสุดทั้งด้านรายได้และหนี้สิน
- ในหมวดหมู่สถานะทางเศรษฐสังคมย่อย กลุ่มผู้จัดการ นักวิชาการ และผู้ปฏิบัติงานวิชาชีพมีค่าเฉลี่ยรายได้และหนี้สินสูงสุด แต่ข้อมูลนี้ไม่ได้วัดสัดส่วนหรือยอดรวมของรายได้/หนี้สิน และไม่ได้บอกวัตถุประสงค์ของหนี้

## Supplementary 2566 findings

- ตารางเสริมทั้งหมดใน repository ถูกกรองให้เหลือปี พ.ศ. 2566 เช่นเดียวกับฐานเดิม
- ตารางระดับจังหวัดใหม่ทั้งสามตารางมีจังหวัดตรงกัน 77 จังหวัดกับ `SFD_SPB0801`
- รายได้ครัวเรือนไทยมาจาก “รายได้จากการทำงาน” มากที่สุด: 20,465 บาท/เดือน หรือประมาณ 70.50% ของรายได้ต่อเดือน จาก `SES_41_01`
- พบครัวเรือนที่เป็นหนี้ 11,472,172 ครัวเรือน จาก `SES_OS_29`
- ในตารางจำนวนครัวเรือนตามแหล่งเงินกู้ วัตถุประสงค์ที่มีจำนวนสูงสุดทั้งหนี้ในระบบและหนี้นอกระบบคือการอุปโภคบริโภคในครัวเรือน แต่ตัวเลขสองประเภทแหล่งเงินกู้ไม่ควรถูกบวกเป็นยอดรวม เพราะครัวเรือนหนึ่งอาจมีหนี้ทั้งสองประเภท

## Time-period and data-quality note

The provincial resources `SFD_SPB0802_66`, `SFD_SPB0806`, and `SFD_SPB0807` are B.E. 2566 and use the same 77 provinces as the original table. The `SES_*` resources were originally multi-year regional tables; this repository stores only their B.E. 2566 rows, and keeps them separate from province-level joins.

The overlap check found one published difference in 770 income keys: the Samut Sakhon agricultural-tenant category is `600` in `SFD_SPB0801` and `-600` in `SFD_SPB0802_66`. Both raw values are preserved and the notebook reports the discrepancy.

## Sources

- [data.go.th dataset 0705_08_0031](https://data.go.th/dataset/0705_08_0031)
- [NSO CSV resource: SFD_SPB0801](https://catalogapi.nso.go.th/api/index?table=SFD_SPB0801&format=csv)
- [data.go.th: average monthly household income](https://data.go.th/dataset/os_08_00007)
- [data.go.th: average household debt](https://data.go.th/dataset/os_08_00011)
- [data.go.th: number of indebted households](https://data.go.th/dataset/os_08_00012)
- [data.go.th: household income](https://data.go.th/dataset/ns_08_20241)
- [NSO CSV resource: SFD_SPB0802_66](https://catalogapi.nso.go.th/api/index?table=SFD_SPB0802_66&format=csv)
- [NSO CSV resource: SFD_SPB0806](https://catalogapi.nso.go.th/api/index?table=SFD_SPB0806&format=csv)
- [NSO CSV resource: SFD_SPB0807](https://catalogapi.nso.go.th/api/index?table=SFD_SPB0807&format=csv)
- [NSO CSV resource: SES_OS_29](https://catalogapi.nso.go.th/api/index?table=SES_OS_29&format=csv)
- [NSO CSV resource: SES_OS_30](https://catalogapi.nso.go.th/api/index?table=SES_OS_30&format=csv)
- [NSO CSV resource: SES_OS_31](https://catalogapi.nso.go.th/api/index?table=SES_OS_31&format=csv)
- [NSO CSV resource: SES_41_01](https://catalogapi.nso.go.th/api/index?table=SES_41_01&format=csv)
- [NSO Income and Income Distribution 2023, Table 3](https://www.nso.go.th/public/e-book/Analytical-Reports/Income-2566/47/)
- [NSO Income and Income Distribution 2023, Table 16](https://www.nso.go.th/public/e-book/Analytical-Reports/Income-2566/94/)
