# Dataset Profile Report: `customer_voice_raw.csv`

## Executive Summary
This profile report documents the structural integrity, statistical distributions, and data quality anomalies of the raw synthetic dataset calculated directly from `data/raw/customer_voice_raw.csv`.

---

## 1. Overview Statistics

| Metric | Calculated Value |
| :--- | :--- |
| **Total Rows** | 6,000 |
| **Total Columns** | 13 |
| **Duplicate Rows (Exact)** | 35 |
| **Duplicate Response IDs** | 35 |

---

## 2. Column Summary & Missing Values

| Column Name | Data Type | Null Count | Null % | Unique Values | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `response_id` | `object` | 0 | 0.00% | 5965 | `RSP-0001` |
| `customer_id` | `object` | 0 | 0.00% | 3149 | `CUST-1912` |
| `survey_date` | `object` | 2 | 0.03% | 369 | `2025-01-13` |
| `region` | `object` | 0 | 0.00% | 5 | `North America` |
| `customer_segment` | `object` | 0 | 0.00% | 3 | `SMB` |
| `industry` | `object` | 59 | 0.98% | 5 | `Finance` |
| `response_channel` | `object` | 0 | 0.00% | 4 | `Phone` |
| `service_category` | `object` | 0 | 0.00% | 10 | `Product` |
| `nps_score` | `int64` | 0 | 0.00% | 16 | `4` |
| `csat_score` | `float64` | 90 | 1.50% | 9 | `1.0` |
| `resolution_days` | `int64` | 0 | 0.00% | 13 | `14` |
| `issue_resolved` | `object` | 0 | 0.00% | 2 | `Yes` |
| `feedback_text` | `object` | 60 | 1.00% | 26 | `Quality has visibly degrade...` |

---

## 3. Domain Validation & Quality Anomalies

| Quality Check Rule | Condition | Total Invalid Records | Status |
| :--- | :--- | :--- | :--- |
| **Duplicate Responses** | Identical `response_id` | 35 | ⚠️ Action Required (Deduplicate) |
| **Missing CSAT Scores** | `csat_score` is Null | 90 | ⚠️ Action Required (Impute / Handle) |
| **Out-of-Range CSAT** | `csat_score` < 1 or > 5 | 12 | ❌ Invalid Values (Drop / Flag) |
| **Out-of-Range NPS** | `nps_score` < 0 or > 10 | 15 | ❌ Invalid Values (Drop / Flag) |
| **Negative Resolution Days** | `resolution_days` < 0 | 14 | ❌ Invalid Values (Drop / Flag) |
| **Malformed / Invalid Dates** | `survey_date` unparseable | 10 | ❌ Invalid Values (Drop / Flag) |
| **Categorical Spacing/Case** | `service_category` non-standard | 79 | ⚠️ Action Required (Standardize) |

### Inconsistent Service Category Variants Found:
- `Product `: 29 records
- `customer support`: 18 records
- `QUALITY `: 13 records
- `DELIVERY`: 11 records
- `pricing`: 8 records

---

## 4. Numerical Column Ranges

| Column | Min | Max | Mean | Median | Std Dev |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `nps_score` | -2.0 | 99.0 | 6.09 | 7.0 | 3.65 |
| `csat_score` | 0.0 | 9.0 | 3.08 | 3.0 | 1.50 |
| `resolution_days` | -5.0 | 21.0 | 4.86 | 4.0 | 4.14 |

---

## 5. Raw Frequency Distributions

### Raw NPS Score Distribution (Valid 0-10 Range)
| Score | Count | Percentage | Classification |
| :--- | :--- | :--- | :--- |
| **0** | 352 | 5.88% | Detractor (0-6) |
| **1** | 297 | 4.96% | Detractor (0-6) |
| **2** | 340 | 5.68% | Detractor (0-6) |
| **3** | 371 | 6.20% | Detractor (0-6) |
| **4** | 424 | 7.08% | Detractor (0-6) |
| **5** | 468 | 7.82% | Detractor (0-6) |
| **6** | 606 | 10.13% | Detractor (0-6) |
| **7** | 800 | 13.37% | Passive (7-8) |
| **8** | 830 | 13.87% | Passive (7-8) |
| **9** | 805 | 13.45% | Promoter (9-10) |
| **10** | 692 | 11.56% | Promoter (9-10) |

### Raw CSAT Score Distribution (Valid 1-5 Range)
| CSAT Score | Meaning | Count | Percentage |
| :--- | :--- | :--- | :--- |
| **1** | Very Dissatisfied | 1268 | 21.50% |
| **2** | Dissatisfied | 1129 | 19.14% |
| **3** | Neutral | 829 | 14.06% |
| **4** | Satisfied | 1263 | 21.41% |
| **5** | Very Satisfied | 1409 | 23.89% |
