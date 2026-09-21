# Household Income and Debt Analysis — Results

**Data source:** `data/raw/SFD_SPB0801.csv` only (NSO, B.E. 2566 / C.E. 2023).

The notebook uses the rows where both socioeconomic classifications are `รวมทั้งสิ้น` for province-level comparisons. The source contains **3,388 rows**, **77 provinces**, and four indicators: monthly income, monthly expenses, average household debt, and expenses as a percentage of income.

## Main findings

- **Highest average household debt:** Phuket (`ภูเก็ต`) — **424,977 baht**.
- **Highest average monthly household income:** Pathum Thani (`ปทุมธานี`) — **45,729 baht/month**.
- **Pearson income–debt correlation:** **0.488** across 77 provincial averages.
- **Spearman rank correlation:** **0.389**.
- **Mean provincial monthly income:** **26,445 baht/month**.
- **Mean provincial average debt:** **195,125 baht**.
- **Highest detailed socioeconomic group for both income and debt:** managers, academics, and professionals (`ผู้จัดการนักวิชาการและผู้ปฏิบัติงานวิชาชีพ`) — mean income **48,292.91 baht/month** and mean debt **558,901.04 baht**.

## Regional summary

These are **unweighted means of provincial averages**, not household-weighted regional totals.

| Region | Provinces | Mean income (baht/month) | Mean debt (baht) | Mean expenses/income |
|---|---:|---:|---:|---:|
| Bangkok and 3 provinces (`กรุงเทพมหานครและ 3 จังหวัด`) | 4 | 38,702.50 | 250,762.00 | 82.62% |
| Northeast (`ภาคตะวันออกเฉียงเหนือ`) | 20 | 22,889.55 | 208,481.00 | 83.56% |
| South (`ภาคใต้`) | 14 | 27,514.00 | 200,481.21 | 83.21% |
| North (`ภาคเหนือ`) | 17 | 23,155.29 | 190,497.12 | 79.44% |
| Central (`ภาคกลาง`) | 22 | 29,309.82 | 173,033.45 | 80.40% |

Bangkok and 3 provinces has the highest simple mean for both income and debt.

## Top provinces

### By average household debt

| Rank | Province | Income (baht/month) | Debt (baht) | Expenses/income |
|---:|---|---:|---:|---:|
| 1 | Phuket (`ภูเก็ต`) | 41,865 | 424,977 | 93.02% |
| 2 | Pathum Thani (`ปทุมธานี`) | 45,729 | 362,493 | 78.73% |
| 3 | Amnat Charoen (`อำนาจเจริญ`) | 28,515 | 337,610 | 79.61% |
| 4 | Ratchaburi (`ราชบุรี`) | 31,368 | 314,967 | 84.28% |
| 5 | Krabi (`กระบี่`) | 28,360 | 314,717 | 86.52% |
| 6 | Phetchabun (`เพชรบูรณ์`) | 27,717 | 309,224 | 75.43% |
| 7 | Nakhon Ratchasima (`นครราชสีมา`) | 27,775 | 303,257 | 77.77% |
| 8 | Surin (`สุรินทร์`) | 22,216 | 290,152 | 82.29% |
| 9 | Mukdahan (`มุกดาหาร`) | 24,925 | 285,176 | 78.03% |
| 10 | Chon Buri (`ชลบุรี`) | 35,981 | 282,402 | 88.06% |

### By average monthly household income

| Rank | Province | Income (baht/month) | Debt (baht) | Expenses/income |
|---:|---|---:|---:|---:|
| 1 | Pathum Thani (`ปทุมธานี`) | 45,729 | 362,493 | 78.73% |
| 2 | Chanthaburi (`จันทบุรี`) | 43,857 | 248,280 | 62.30% |
| 3 | Phuket (`ภูเก็ต`) | 41,865 | 424,977 | 93.02% |
| 4 | Bangkok (`กรุงเทพมหานคร`) | 40,051 | 161,050 | 81.74% |
| 5 | Nonthaburi (`นนทบุรี`) | 36,767 | 267,543 | 85.21% |
| 6 | Chon Buri (`ชลบุรี`) | 35,981 | 282,402 | 88.06% |
| 7 | Phra Nakhon Si Ayutthaya (`พระนครศรีอยุธยา`) | 33,919 | 231,845 | 78.84% |
| 8 | Saraburi (`สระบุรี`) | 33,894 | 254,307 | 80.29% |
| 9 | Surat Thani (`สุราษฎร์ธานี`) | 33,523 | 225,020 | 78.61% |
| 10 | Nakhon Si Thammarat (`นครศรีธรรมราช`) | 33,414 | 268,956 | 69.04% |

## Data-quality checks

- No duplicate complete rows.
- No duplicate rows for the key `(year, province, indicator, soc_eco_class1, soc_eco_class2)`.
- No numeric parsing failures in `value`.
- The `attribute` field has 3,266 missing values because it contains notes only for selected observations.
- There are 122 noted zero estimates; these are retained as published and are not automatically treated as missing data.

## Interpretation and limitations

The correlation is a descriptive association between **provincial averages in one year**, not household-level evidence or proof that income causes debt. Phuket's highest value is average debt per household, not total provincial debt. Regional figures are unweighted, and the socioeconomic rankings are category averages rather than totals or shares of households.

Supplementary CSV files remain in the repository for possible later work, but they are intentionally **not loaded by the current notebook**.

## Source links

- [data.go.th dataset 0705_08_0031](https://data.go.th/dataset/0705_08_0031)
- [NSO CSV resource: SFD_SPB0801](https://catalogapi.nso.go.th/api/index?table=SFD_SPB0801&format=csv)
