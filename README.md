# Household Income and Debt Analysis

การสำรวจข้อมูลรายได้และหนี้สินครัวเรือนระดับจังหวัดของประเทศไทยจากสำนักงานสถิติแห่งชาติ (NSO) ปี พ.ศ. 2566 (ค.ศ. 2023)

## Contents

- `household_income_debt_analysis.ipynb` — notebook ตรวจสอบคุณภาพข้อมูลและวิเคราะห์เชิงสำรวจ
- `data/raw/SFD_SPB0801.csv` — CSV จากทรัพยากร NSO ที่เชื่อมโยงโดย data.go.th
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

## Sources

- [data.go.th dataset 0705_08_0031](https://data.go.th/dataset/0705_08_0031)
- [NSO CSV resource: SFD_SPB0801](https://catalogapi.nso.go.th/api/index?table=SFD_SPB0801&format=csv)
- [NSO Income and Income Distribution 2023, Table 3](https://www.nso.go.th/public/e-book/Analytical-Reports/Income-2566/47/)
- [NSO Income and Income Distribution 2023, Table 16](https://www.nso.go.th/public/e-book/Analytical-Reports/Income-2566/94/)

