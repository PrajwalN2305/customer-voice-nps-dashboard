import pandas as pd
import numpy as np

def audit():
    raw_path = 'data/raw/customer_voice_raw.csv'
    df_raw = pd.read_csv(raw_path)
    
    raw_total = len(df_raw)
    print(f"1. RAW ROWS: {raw_total}")
    
    # Check duplicates
    dup_mask = df_raw.duplicated(subset=['response_id'], keep='first')
    dup_count = int(dup_mask.sum())
    print(f"2. DUPLICATES (response_id): {dup_count}")
    
    df_dedup = df_raw[~dup_mask].copy()
    
    # Check missing industry (repaired via 'Unknown')
    missing_ind = int(df_dedup['industry'].isna().sum())
    print(f"3. MISSING INDUSTRY (REPAIRED -> 'Unknown'): {missing_ind}")
    
    # Check missing feedback_text (repaired via 'No feedback provided')
    missing_fb = int(df_dedup['feedback_text'].isna().sum())
    print(f"4. MISSING FEEDBACK (REPAIRED -> 'No feedback provided'): {missing_fb}")
    
    # Check missing CSAT (repaired via median CSAT 4)
    missing_csat = int(df_dedup['csat_score'].isna().sum())
    print(f"5. MISSING CSAT (REPAIRED -> median 4): {missing_csat}")
    
    # Check non-standard category casing (repaired via .str.strip().str.title())
    dirty_cats = int(df_dedup['service_category'].apply(lambda x: str(x) != str(x).strip().title()).sum())
    print(f"6. INCONSISTENT CATEGORIES (REPAIRED -> Title Case): {dirty_cats}")
    
    # Invalid NPS (<0 or >10 or NaN)
    nps_num = pd.to_numeric(df_dedup['nps_score'], errors='coerce')
    invalid_nps_mask = (nps_num < 0) | (nps_num > 10) | nps_num.isna()
    invalid_nps_count = int(invalid_nps_mask.sum())
    print(f"7. INVALID NPS RECORDS (REMOVED): {invalid_nps_count}")
    
    # Invalid CSAT (<1 or >5) - excluding the NaN values which were imputed
    csat_num = pd.to_numeric(df_dedup['csat_score'], errors='coerce')
    invalid_csat_mask = ((csat_num < 1) | (csat_num > 5)) & csat_num.notna()
    invalid_csat_count = int(invalid_csat_mask.sum())
    print(f"8. INVALID CSAT RECORDS (REMOVED): {invalid_csat_count}")
    
    # Invalid Resolution Days (<0)
    res_num = pd.to_numeric(df_dedup['resolution_days'], errors='coerce')
    invalid_res_mask = (res_num < 0) | res_num.isna()
    invalid_res_count = int(invalid_res_mask.sum())
    print(f"9. INVALID RESOLUTION DAYS (REMOVED): {invalid_res_count}")
    
    # Invalid Dates
    dates_parsed = pd.to_datetime(df_dedup['survey_date'], format='%Y-%m-%d', errors='coerce')
    invalid_date_mask = dates_parsed.isna()
    invalid_date_count = int(invalid_date_mask.sum())
    print(f"10. INVALID DATES (REMOVED): {invalid_date_count}")
    
    # Combined invalid rows mask across invalid NPS, CSAT, Resolution Days, Dates
    combined_invalid_mask = invalid_nps_mask | invalid_csat_mask | invalid_res_mask | invalid_date_mask
    total_invalid_removed = int(combined_invalid_mask.sum())
    print(f"11. TOTAL INVALID ROWS REMOVED: {total_invalid_removed}")
    
    final_count = len(df_dedup) - total_invalid_removed
    print(f"12. RECONCILED CLEANED ROWS: {final_count}")
    print(f"    Formula: {raw_total} (Raw) - {dup_count} (Duplicates) - {total_invalid_removed} (Invalid Records) = {final_count}")

if __name__ == '__main__':
    audit()
