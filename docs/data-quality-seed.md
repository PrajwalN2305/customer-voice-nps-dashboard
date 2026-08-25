# Data Quality Seed Documentation

## Overview
To simulate a realistic enterprise customer survey environment for data profiling, validation, and cleaning demonstrations, controlled data-quality issues were intentionally seeded into `data/raw/customer_voice_raw.csv`.

> [!IMPORTANT]
> The raw dataset MUST retain these issues to test data pipeline robustness. Do not clean `customer_voice_raw.csv` directly.

---

## Seeded Data-Quality Issues Summary

| Issue Type | Target Column | Quantity / Percentage | Intentional Error Details | Pipeline Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Missing Values** | `csat_score` | 90 records (~1.5%) | `NaN` / blank values in customer satisfaction rating | Requires missing value treatment / profiling |
| **Missing Values** | `industry` | 60 records (~1.0%) | `NaN` / blank values in customer industry classification | Impute with `"Unknown"` categorical default |
| **Missing Values** | `feedback_text` | 60 records (~1.0%) | `NaN` / blank values in verbatim feedback | Impute with `"No feedback provided"` |
| **Duplicate Records** | All columns / `response_id` | 35 duplicate rows (~0.58%) | Exact row duplicates (identical `response_id` and payload) | Deduplication required in Pandas cleaning pipeline |
| **Inconsistent Categorical Values** | `service_category` | 80 records (~1.33%) | Mixed case and trailing whitespace (e.g. `'customer support'`, `'DELIVERY'`, `'Product '`, `'QUALITY '`) | Text standardization via string trimming and title casing |
| **Out-of-Range Values** | `nps_score` | 15 records (~0.25%) | Invalid scores outside 0–10 range (e.g. `-2`, `-1`, `11`, `12`, `99`) | Range validation rule: flag / remove invalid records |
| **Out-of-Range Values** | `csat_score` | 12 records (~0.20%) | Invalid scores outside 1–5 range (e.g. `0`, `6`, `7`, `9`) | Range validation rule: flag / remove invalid records |
| **Negative Values** | `resolution_days` | 15 records (~0.25%) | Impossible negative days to resolve (e.g. `-5`, `-3`, `-1`) | Logical validation rule: remove records where `resolution_days < 0` |
| **Malformed / Invalid Dates** | `survey_date` | 10 records (~0.17%) | Unparseable or non-existent dates (e.g. `'2025-13-45'`, `'INVALID_DATE'`, `'2025-02-30'`, `''`) | Date parsing validation rule: flag / drop unparseable rows |

---

## Total Data Quality Impact
- **Total Raw Records:** 6,000
- **Total Impacted Records:** ~340 records (~5.6% of raw dataset contains at least one quality anomaly)
- **Clean Records Ratio:** ~94.4% valid records, ensuring realistic noise without corrupting macro business patterns.
