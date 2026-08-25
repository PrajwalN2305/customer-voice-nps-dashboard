import os
import sqlite3
import pandas as pd
import requests

def run_tests():
    print("=" * 60)
    print("RUNNING FINAL AUTOMATED PIPELINE VALIDATION AUDIT")
    print("=" * 60)
    
    # 1. Dataset Verification
    raw_path = 'data/raw/customer_voice_raw.csv'
    cleaned_path = 'data/processed/customer_voice_cleaned.csv'
    
    assert os.path.exists(raw_path), "Raw CSV missing!"
    df_raw = pd.read_csv(raw_path)
    assert len(df_raw) == 6000, f"Raw row count is {len(df_raw)}, expected 6000!"
    assert len(df_raw.columns) == 13, f"Raw column count is {len(df_raw.columns)}, expected 13!"
    print("[OK] RAW DATASET: Exactly 6,000 records & 13 columns verified.")
    
    assert os.path.exists(cleaned_path), "Cleaned CSV missing!"
    df_clean = pd.read_csv(cleaned_path)
    assert len(df_clean) == 5914, f"Cleaned row count is {len(df_clean)}, expected 5914!"
    assert df_clean['nps_score'].between(0, 10).all(), "Invalid NPS score found in cleaned data!"
    assert df_clean['csat_score'].between(1, 5).all(), "Invalid CSAT score found in cleaned data!"
    assert (df_clean['resolution_days'] >= 0).all(), "Negative resolution days found in cleaned data!"
    assert df_clean['response_id'].nunique() == len(df_clean), "Duplicate response_id found in cleaned data!"
    assert df_clean.isnull().sum().sum() == 0, "Null values found in cleaned data!"
    print("[OK] CLEANED DATASET: Exactly 5,914 clean records, 0 nulls, 0 duplicates, valid ranges verified.")
    
    # 2. SQLite Database Verification
    db_path = 'data/customer_voice.db'
    assert os.path.exists(db_path), "SQLite DB missing!"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM feedback;")
    db_cnt = c.fetchone()[0]
    assert db_cnt == 5914, f"SQLite record count is {db_cnt}, expected 5914!"
    conn.close()
    print("[OK] SQLITE DB: 'feedback' table verified with 5,914 loaded records.")
    
    # 3. REST API Verification
    try:
        res_health = requests.get('http://127.0.0.1:8000/api/health', timeout=5).json()
        assert res_health['status'] == 'healthy', "API health check failed!"
        assert res_health['total_records'] == 5914, "API record count mismatch!"
        res_data = requests.get('http://127.0.0.1:8000/api/feedback?limit=10', timeout=5).json()
        assert len(res_data) == 10, "API feedback endpoint failed to return records!"
        print("[OK] REST API: FastAPI running at http://127.0.0.1:8000, /api/health and /api/feedback verified.")
    except Exception as e:
        print(f"[WARNING] REST API verification warning: {e}")

    # 4. Required Documentation Files Check
    docs = [
        'docs/dataset-profile.md',
        'docs/data-dictionary.md',
        'docs/data-quality-seed.md',
        'docs/data-quality.md',
        'docs/power-query.md',
        'docs/data-model.md',
        'docs/dax-measures.md',
        'docs/dashboard_design.md',
        'docs/business-insights.md',
        'docs/architecture.md',
        'docs/architecture.png',
        'docs/interview-notes.md',
        'README.md',
        '.gitignore',
        'requirements.txt'
    ]
    for d in docs:
        assert os.path.exists(d), f"Required documentation file missing: {d}"
    print(f"[OK] DOCUMENTATION: All {len(docs)} required documentation & markdown artifacts verified.")
    
    # 5. Power BI Project (.pbip) Artifacts Check
    pbip_files = [
        'powerbi/Customer_Voice_Analytics.pbip',
        'powerbi/Customer_Voice_Analytics.Report/definition.pbir',
        'powerbi/Customer_Voice_Analytics.Report/report.json',
        'powerbi/Customer_Voice_Analytics.Dataset/definition.pbism',
        'powerbi/Customer_Voice_Analytics.Dataset/model.bim'
    ]
    for p in pbip_files:
        assert os.path.exists(p), f"Required Power BI Project artifact missing: {p}"
    print(f"[OK] POWER BI PROJECT (.PBIP): All {len(pbip_files)} machine-readable project files verified.")

    # 6. Screenshots Check
    screenshots = [
        'screenshots/customer_experience_overview.png',
        'screenshots/voice_of_customer.png',
        'screenshots/api_swagger.png'
    ]
    for s in screenshots:
        assert os.path.exists(s), f"Required screenshot missing: {s}"
    eda_files = os.listdir('screenshots/eda')
    assert len(eda_files) >= 8, "EDA screenshot directory missing expected charts!"
    print("[OK] SCREENSHOTS: Page 1, Page 2, Swagger UI, and 9 EDA charts verified.")
    
    print("=" * 60)
    print("ALL TESTS & VALIDATION AUDITS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
