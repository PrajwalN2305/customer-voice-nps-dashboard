import pandas as pd
import numpy as np
import os
import json

def profile_dataset():
    raw_path = 'data/raw/customer_voice_raw.csv'
    output_doc_path = 'docs/dataset-profile.md'
    
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_path}")
        
    df = pd.read_csv(raw_path)
    
    total_rows = len(df)
    total_cols = len(df.columns)
    
    # 1. Missing values
    missing_counts = df.isnull().sum()
    missing_pcts = (missing_counts / total_rows) * 100
    
    # 2. Duplicate rows
    duplicate_rows = df.duplicated().sum()
    duplicate_resp_ids = df['response_id'].duplicated().sum()
    
    # 3. Data types & unique counts
    dtypes = df.dtypes.astype(str).to_dict()
    unique_counts = df.nunique().to_dict()
    
    # 4. Numerical ranges
    numeric_stats = {}
    for col in ['nps_score', 'csat_score', 'resolution_days']:
        col_series = pd.to_numeric(df[col], errors='coerce')
        numeric_stats[col] = {
            'min': float(col_series.min()),
            'max': float(col_series.max()),
            'mean': float(col_series.mean()),
            'median': float(col_series.median()),
            'std': float(col_series.std())
        }
        
    # 5. Domain Validation Checks
    # Invalid NPS (<0 or >10)
    nps_numeric = pd.to_numeric(df['nps_score'], errors='coerce')
    invalid_nps_mask = (nps_numeric < 0) | (nps_numeric > 10) | nps_numeric.isna()
    invalid_nps_count = int(invalid_nps_mask.sum())
    
    # Invalid CSAT (<1 or >5) - excluding missing values
    csat_numeric = pd.to_numeric(df['csat_score'], errors='coerce')
    invalid_csat_mask = ((csat_numeric < 1) | (csat_numeric > 5)) & csat_numeric.notna()
    invalid_csat_count = int(invalid_csat_mask.sum())
    missing_csat_count = int(df['csat_score'].isna().sum())
    
    # Invalid Resolution Days (<0)
    res_numeric = pd.to_numeric(df['resolution_days'], errors='coerce')
    invalid_res_mask = (res_numeric < 0) | res_numeric.isna()
    invalid_res_count = int(invalid_res_mask.sum())
    
    # Invalid / Malformed dates
    parsed_dates = pd.to_datetime(df['survey_date'], format='%Y-%m-%d', errors='coerce')
    invalid_date_count = int(parsed_dates.isna().sum())
    
    # Inconsistent Service Categories
    raw_service_cats = df['service_category'].value_counts(dropna=False).to_dict()
    standard_service_cats = ['Product', 'Delivery', 'Customer Support', 'Quality', 'Pricing']
    inconsistent_cats = {k: v for k, v in raw_service_cats.items() if str(k).strip().title() not in standard_service_cats or str(k) != str(k).strip().title()}
    
    # NPS Distribution
    nps_dist = nps_numeric[~invalid_nps_mask].value_counts().sort_index().to_dict()
    
    # CSAT Distribution (valid values 1..5)
    csat_dist = csat_numeric[(csat_numeric >= 1) & (csat_numeric <= 5)].value_counts().sort_index().to_dict()
    
    # Generate Markdown Output
    doc_content = f"""# Dataset Profile Report: `customer_voice_raw.csv`

## Executive Summary
This profile report documents the structural integrity, statistical distributions, and data quality anomalies of the raw synthetic dataset calculated directly from `data/raw/customer_voice_raw.csv`.

---

## 1. Overview Statistics

| Metric | Calculated Value |
| :--- | :--- |
| **Total Rows** | {total_rows:,} |
| **Total Columns** | {total_cols} |
| **Duplicate Rows (Exact)** | {duplicate_rows} |
| **Duplicate Response IDs** | {duplicate_resp_ids} |

---

## 2. Column Summary & Missing Values

| Column Name | Data Type | Null Count | Null % | Unique Values | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for col in df.columns:
        null_c = missing_counts[col]
        null_p = missing_pcts[col]
        dt = dtypes[col]
        uniq = unique_counts[col]
        sample_val = str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "N/A"
        if len(sample_val) > 30:
            sample_val = sample_val[:27] + "..."
        doc_content += f"| `{col}` | `{dt}` | {null_c} | {null_p:.2f}% | {uniq} | `{sample_val}` |\n"

    doc_content += f"""
---

## 3. Domain Validation & Quality Anomalies

| Quality Check Rule | Condition | Total Invalid Records | Status |
| :--- | :--- | :--- | :--- |
| **Duplicate Responses** | Identical `response_id` | {duplicate_resp_ids} | ⚠️ Action Required (Deduplicate) |
| **Missing CSAT Scores** | `csat_score` is Null | {missing_csat_count} | ⚠️ Action Required (Impute / Handle) |
| **Out-of-Range CSAT** | `csat_score` < 1 or > 5 | {invalid_csat_count} | ❌ Invalid Values (Drop / Flag) |
| **Out-of-Range NPS** | `nps_score` < 0 or > 10 | {invalid_nps_count} | ❌ Invalid Values (Drop / Flag) |
| **Negative Resolution Days** | `resolution_days` < 0 | {invalid_res_count} | ❌ Invalid Values (Drop / Flag) |
| **Malformed / Invalid Dates** | `survey_date` unparseable | {invalid_date_count} | ❌ Invalid Values (Drop / Flag) |
| **Categorical Spacing/Case** | `service_category` non-standard | {sum(inconsistent_cats.values())} | ⚠️ Action Required (Standardize) |

### Inconsistent Service Category Variants Found:
"""
    for cat_var, cnt in inconsistent_cats.items():
        doc_content += f"- `{cat_var}`: {cnt} records\n"

    doc_content += f"""
---

## 4. Numerical Column Ranges

| Column | Min | Max | Mean | Median | Std Dev |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `nps_score` | {numeric_stats['nps_score']['min']:.1f} | {numeric_stats['nps_score']['max']:.1f} | {numeric_stats['nps_score']['mean']:.2f} | {numeric_stats['nps_score']['median']:.1f} | {numeric_stats['nps_score']['std']:.2f} |
| `csat_score` | {numeric_stats['csat_score']['min']:.1f} | {numeric_stats['csat_score']['max']:.1f} | {numeric_stats['csat_score']['mean']:.2f} | {numeric_stats['csat_score']['median']:.1f} | {numeric_stats['csat_score']['std']:.2f} |
| `resolution_days` | {numeric_stats['resolution_days']['min']:.1f} | {numeric_stats['resolution_days']['max']:.1f} | {numeric_stats['resolution_days']['mean']:.2f} | {numeric_stats['resolution_days']['median']:.1f} | {numeric_stats['resolution_days']['std']:.2f} |

---

## 5. Raw Frequency Distributions

### Raw NPS Score Distribution (Valid 0-10 Range)
| Score | Count | Percentage | Classification |
| :--- | :--- | :--- | :--- |
"""
    valid_nps_total = sum(nps_dist.values())
    for score in range(11):
        cnt = nps_dist.get(score, 0)
        pct = (cnt / valid_nps_total * 100) if valid_nps_total > 0 else 0
        cls = "Detractor (0-6)" if score <= 6 else ("Passive (7-8)" if score <= 8 else "Promoter (9-10)")
        doc_content += f"| **{score}** | {cnt} | {pct:.2f}% | {cls} |\n"

    doc_content += f"""
### Raw CSAT Score Distribution (Valid 1-5 Range)
| CSAT Score | Meaning | Count | Percentage |
| :--- | :--- | :--- | :--- |
"""
    valid_csat_total = sum(csat_dist.values())
    csat_labels = {1: 'Very Dissatisfied', 2: 'Dissatisfied', 3: 'Neutral', 4: 'Satisfied', 5: 'Very Satisfied'}
    for score in range(1, 6):
        cnt = csat_dist.get(score, 0)
        pct = (cnt / valid_csat_total * 100) if valid_csat_total > 0 else 0
        doc_content += f"| **{score}** | {csat_labels[score]} | {cnt} | {pct:.2f}% |\n"

    os.makedirs(os.path.dirname(output_doc_path), exist_ok=True)
    with open(output_doc_path, 'w', encoding='utf-8') as f:
        f.write(doc_content)
        
    print(f"Data profiling complete. Report generated at {output_doc_path}")

if __name__ == '__main__':
    profile_dataset()
