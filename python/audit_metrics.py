import pandas as pd
import sqlite3

def audit_metrics():
    cleaned_path = 'data/processed/customer_voice_cleaned.csv'
    db_path = 'data/customer_voice.db'
    
    df = pd.read_csv(cleaned_path)
    
    total = len(df)
    promoters = (df['nps_score'] >= 9).sum()
    passives = ((df['nps_score'] == 7) | (df['nps_score'] == 8)).sum()
    detractors = (df['nps_score'] <= 6).sum()
    
    promoter_pct = (promoters / total) * 100
    passive_pct = (passives / total) * 100
    detractor_pct = (detractors / total) * 100
    
    nps_score = promoter_pct - detractor_pct
    avg_csat = df['csat_score'].mean()
    avg_res_days = df['resolution_days'].mean()
    
    print("--- PYTHON METRICS RECONCILIATION ---")
    print(f"Total Responses:          {total}")
    print(f"Promoters (9-10):         {promoters} ({promoter_pct:.2f}%)")
    print(f"Passives (7-8):           {passives} ({passive_pct:.2f}%)")
    print(f"Detractors (0-6):         {detractors} ({detractor_pct:.2f}%)")
    print(f"Net NPS Score (Points):   {nps_score:.2f}  (Formatted: {nps_score:.1f})")
    print(f"Average CSAT:             {avg_csat:.2f}")
    print(f"Average Resolution Days:  {avg_res_days:.2f} days")
    
    # Check SQLite SQL Queries
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    sql_total = c.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
    sql_prom = c.execute("SELECT COUNT(*) FROM feedback WHERE nps_score >= 9").fetchone()[0]
    sql_pass = c.execute("SELECT COUNT(*) FROM feedback WHERE nps_score IN (7, 8)").fetchone()[0]
    sql_det = c.execute("SELECT COUNT(*) FROM feedback WHERE nps_score <= 6").fetchone()[0]
    sql_nps = c.execute("""
        SELECT ROUND(
            (CAST(SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS FLOAT) - 
             CAST(SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) AS FLOAT)) 
            / COUNT(*) * 100, 2
        ) FROM feedback
    """).fetchone()[0]
    sql_csat = c.execute("SELECT ROUND(AVG(csat_score), 2) FROM feedback").fetchone()[0]
    sql_res = c.execute("SELECT ROUND(AVG(resolution_days), 2) FROM feedback").fetchone()[0]
    conn.close()
    
    print("\n--- SQL METRICS RECONCILIATION ---")
    print(f"SQL Total Responses:      {sql_total}")
    print(f"SQL Promoters:            {sql_prom}")
    print(f"SQL Passives:             {sql_pass}")
    print(f"SQL Detractors:           {sql_det}")
    print(f"SQL Net NPS Score:        {sql_nps}")
    print(f"SQL Average CSAT:         {sql_csat}")
    print(f"SQL Avg Resolution Days:  {sql_res} days")
    
    assert total == sql_total
    assert promoters == sql_prom
    assert passives == sql_pass
    assert detractors == sql_det
    assert round(nps_score, 2) == sql_nps
    assert round(avg_csat, 2) == sql_csat
    assert round(avg_res_days, 2) == sql_res
    print("\n[OK] PYTHON AND SQL METRICS RECONCILE 100% PERFECTLY!")

if __name__ == '__main__':
    audit_metrics()
