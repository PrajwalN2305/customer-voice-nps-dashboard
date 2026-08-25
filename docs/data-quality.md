# Data Quality & Cleaning Audit Documentation

## Executive Summary
This document provides an end-to-end audit trail of the data profiling, validation, and cleaning rules applied by `python/data_cleaning.py` to convert `data/raw/customer_voice_raw.csv` into `data/processed/customer_voice_cleaned.csv`.

---

## Metric Overview: Raw vs. Cleaned Dataset

| Metric | Raw Dataset (`customer_voice_raw.csv`) | Cleaned Dataset (`customer_voice_cleaned.csv`) | Net Change / Difference |
| :--- | :--- | :--- | :--- |
| **Total Record Count** | **6,000** | **5,914** | -86 records dropped (~1.43%) |
| **Duplicate Responses** | 35 | 0 | -35 duplicate rows removed |
| **Missing CSAT Values** | 90 | 0 | All imputed with median CSAT (4) |
| **Missing Industry Values** | 60 | 0 | All imputed with `"Unknown"` |
| **Missing Feedback Text** | 60 | 0 | All imputed with `"No feedback provided"` |
| **Invalid NPS Scores (<0 or >10)** | 15 | 0 | 15 invalid rows dropped |
| **Invalid CSAT Scores (<1 or >5)** | 12 | 0 | 12 invalid rows dropped |
| **Negative Resolution Days** | 15 | 0 | 15 invalid rows dropped |
| **Malformed Survey Dates** | 10 | 0 | 10 malformed rows dropped |
| **Non-standard Categories** | 80 | 0 | All standardized to Title Case |

---

## Detailed Data Quality & Cleaning Treatments Log

### 1. Duplicate survey responses
- **Detection Method:** `df.duplicated(subset=["response_id"])`
- **Affected Records:** `35`
- **Treatment Applied:** Removed duplicate response rows, keeping the first occurrence.
- **Business & Technical Rationale:** Duplicate survey IDs distort satisfaction metrics and response volume counts.
- **Post-Cleaning Verification Result:** 0 duplicate response IDs in cleaned dataset (5965 records remaining).

### 2. Inconsistent category casing & trailing whitespace
- **Detection Method:** String inspection & regex comparison against standard category values
- **Affected Records:** `79`
- **Treatment Applied:** Applied `.str.strip().str.title()` standardization.
- **Business & Technical Rationale:** Categories like "customer support" and "DELIVERY" cause fragmented reporting in SQL and Power BI.
- **Post-Cleaning Verification Result:** 5 standardized categories: Product, Delivery, Customer Support, Quality, Pricing.

### 3. Missing industry values
- **Detection Method:** `df["industry"].isna()` check
- **Affected Records:** `59`
- **Treatment Applied:** Imputed missing values with categorical placeholder `"Unknown"`.
- **Business & Technical Rationale:** Preserves valid survey data and NPS/CSAT scores without discarding customer responses.
- **Post-Cleaning Verification Result:** 0 missing industry values; categorized under "Unknown" segment.

### 4. Missing feedback text
- **Detection Method:** `df["feedback_text"].isna()` check
- **Affected Records:** `59`
- **Treatment Applied:** Imputed missing text with `"No feedback provided"`.
- **Business & Technical Rationale:** Ensures tabular display in Power BI feedback tables does not break or show null indicators.
- **Post-Cleaning Verification Result:** 0 missing feedback text fields.

### 5. Missing CSAT scores
- **Detection Method:** `df["csat_score"].isna()` check
- **Affected Records:** `90`
- **Treatment Applied:** Imputed missing CSAT values with overall dataset median CSAT score (3).
- **Business & Technical Rationale:** Avoids dropping responses with valid NPS scores while maintaining neutral CSAT baseline.
- **Post-Cleaning Verification Result:** 0 missing CSAT scores; all imputed with score = 3.

### 6. Invalid NPS scores (<0 or >10)
- **Detection Method:** Range check: `(nps_score < 0) | (nps_score > 10)`
- **Affected Records:** `15`
- **Treatment Applied:** Removed invalid NPS records from the dataset.
- **Business & Technical Rationale:** NPS is defined strictly on a 0 to 10 integer scale. Invalid scores corrupt promoter/detractor calculations.
- **Post-Cleaning Verification Result:** 0 invalid NPS scores in processed dataset (5950 records remaining).

### 7. Invalid CSAT scores (<1 or >5)
- **Detection Method:** Range check: `(csat_score < 1) | (csat_score > 5)`
- **Affected Records:** `12`
- **Treatment Applied:** Removed invalid CSAT records from the dataset.
- **Business & Technical Rationale:** CSAT is defined strictly on a 1 to 5 integer Likert scale.
- **Post-Cleaning Verification Result:** 0 invalid CSAT scores in processed dataset (5938 records remaining).

### 8. Negative resolution days (<0)
- **Detection Method:** Logical check: `resolution_days < 0`
- **Affected Records:** `14`
- **Treatment Applied:** Removed records with negative resolution days.
- **Business & Technical Rationale:** Resolution time cannot be negative in a real-world service process; indicates data entry/timestamp errors.
- **Post-Cleaning Verification Result:** 0 negative resolution day records (5924 records remaining).

### 9. Malformed / invalid survey dates
- **Detection Method:** `pd.to_datetime(survey_date, errors="coerce").isna()`
- **Affected Records:** `10`
- **Treatment Applied:** Removed records with unparseable or malformed dates.
- **Business & Technical Rationale:** Valid ISO dates (`YYYY-MM-DD`) are required for time-series trend analysis and Power BI date tables.
- **Post-Cleaning Verification Result:** 0 malformed date strings in cleaned dataset (5914 records remaining).

---

## Post-Cleaning Validation & Integrity Checks
After pipeline execution, `customer_voice_cleaned.csv` was subjected to automated verification:

1. **Schema Check:** All 13 columns preserved (`response_id`, `customer_id`, `survey_date`, `region`, `customer_segment`, `industry`, `response_channel`, `service_category`, `nps_score`, `csat_score`, `resolution_days`, `issue_resolved`, `feedback_text`).
2. **Range Verification:** 
   - `0 <= nps_score <= 10`: **VERIFIED (Min: 0, Max: 10)**
   - `1 <= csat_score <= 5`: **VERIFIED (Min: 1, Max: 5)**
   - `resolution_days >= 0`: **VERIFIED (Min: 1, Max: 21)**
3. **Null Check:** 0 Null values across all critical columns.
4. **Primary Key Integrity:** `response_id` is unique for all 5,914 rows.
