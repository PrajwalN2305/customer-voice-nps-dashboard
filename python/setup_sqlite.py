import sqlite3
import pandas as pd
import os

def setup_sqlite():
    db_path = 'data/customer_voice.db'
    cleaned_csv = 'data/processed/customer_voice_cleaned.csv'
    schema_sql_path = 'sql/schema.sql'
    queries_sql_path = 'sql/analysis_queries.sql'
    
    if not os.path.exists(cleaned_csv):
        raise FileNotFoundError(f"Cleaned CSV not found at {cleaned_csv}")
        
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    os.makedirs('sql', exist_ok=True)
    
    # 1. Write sql/schema.sql
    schema_sql = """-- Customer Voice & NPS Analytics Database Schema
-- Table: feedback

DROP TABLE IF EXISTS feedback;

CREATE TABLE feedback (
    response_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    survey_date DATE NOT NULL,
    region TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    industry TEXT NOT NULL,
    response_channel TEXT NOT NULL,
    service_category TEXT NOT NULL,
    nps_score INTEGER CHECK (nps_score >= 0 AND nps_score <= 10),
    csat_score INTEGER CHECK (csat_score >= 1 AND csat_score <= 5),
    resolution_days INTEGER CHECK (resolution_days >= 0),
    issue_resolved TEXT CHECK (issue_resolved IN ('Yes', 'No')),
    feedback_text TEXT
);

CREATE INDEX idx_feedback_survey_date ON feedback(survey_date);
CREATE INDEX idx_feedback_region ON feedback(region);
CREATE INDEX idx_feedback_segment ON feedback(customer_segment);
CREATE INDEX idx_feedback_category ON feedback(service_category);
"""
    with open(schema_sql_path, 'w', encoding='utf-8') as f:
        f.write(schema_sql)
        
    # 2. Write sql/analysis_queries.sql
    queries_sql = """-- Customer Voice & NPS Analytics - Analytical Queries

-- 1. Total Responses
SELECT COUNT(*) AS total_responses
FROM feedback;

-- 2. Average NPS Score
SELECT ROUND(AVG(nps_score), 2) AS avg_nps_score
FROM feedback;

-- 3. Average CSAT
SELECT ROUND(AVG(csat_score), 2) AS avg_csat_score
FROM feedback;

-- 4. Promoter Count (NPS 9-10)
SELECT COUNT(*) AS promoter_count
FROM feedback
WHERE nps_score >= 9;

-- 5. Passive Count (NPS 7-8)
SELECT COUNT(*) AS passive_count
FROM feedback
WHERE nps_score IN (7, 8);

-- 6. Detractor Count (NPS 0-6)
SELECT COUNT(*) AS detractor_count
FROM feedback
WHERE nps_score <= 6;

-- 7. Net NPS (%)
SELECT 
    COUNT(*) AS total_responses,
    SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS promoters,
    SUM(CASE WHEN nps_score IN (7, 8) THEN 1 ELSE 0 END) AS passives,
    SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) AS detractors,
    ROUND(
        (CAST(SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS FLOAT) - 
         CAST(SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) AS FLOAT)) 
        / COUNT(*) * 100, 2
    ) AS net_nps_pct
FROM feedback;

-- 8. NPS by Region
SELECT 
    region,
    COUNT(*) AS total_responses,
    SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS promoters,
    SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) AS detractors,
    ROUND(
        (CAST(SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS FLOAT) - 
         CAST(SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) AS FLOAT)) 
        / COUNT(*) * 100, 2
    ) AS net_nps_pct
FROM feedback
GROUP BY region
ORDER BY net_nps_pct DESC;

-- 9. NPS by Customer Segment
SELECT 
    customer_segment,
    COUNT(*) AS total_responses,
    SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS promoters,
    SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) AS detractors,
    ROUND(
        (CAST(SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS FLOAT) - 
         CAST(SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) AS FLOAT)) 
        / COUNT(*) * 100, 2
    ) AS net_nps_pct
FROM feedback
GROUP BY customer_segment
ORDER BY net_nps_pct DESC;

-- 10. NPS by Service Category
SELECT 
    service_category,
    COUNT(*) AS total_responses,
    SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS promoters,
    SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) AS detractors,
    ROUND(
        (CAST(SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS FLOAT) - 
         CAST(SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END) AS FLOAT)) 
        / COUNT(*) * 100, 2
    ) AS net_nps_pct
FROM feedback
GROUP BY service_category
ORDER BY net_nps_pct DESC;

-- 11. Response Volume by Channel
SELECT 
    response_channel,
    COUNT(*) AS total_responses,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM feedback), 2) AS channel_pct
FROM feedback
GROUP BY response_channel
ORDER BY total_responses DESC;

-- 12. Average Resolution Days by NPS Category
SELECT 
    CASE 
        WHEN nps_score >= 9 THEN 'Promoter (9-10)'
        WHEN nps_score >= 7 THEN 'Passive (7-8)'
        ELSE 'Detractor (0-6)'
    END AS nps_category,
    COUNT(*) AS response_count,
    ROUND(AVG(resolution_days), 2) AS avg_resolution_days
FROM feedback
GROUP BY 1
ORDER BY avg_resolution_days ASC;

-- 13. CSAT by Customer Segment
SELECT 
    customer_segment,
    COUNT(*) AS total_responses,
    ROUND(AVG(csat_score), 2) AS avg_csat_score
FROM feedback
GROUP BY customer_segment
ORDER BY avg_csat_score DESC;

-- 14. Service Category Response Distribution
SELECT 
    service_category,
    COUNT(*) AS total_responses,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM feedback), 2) AS category_pct,
    ROUND(AVG(csat_score), 2) AS avg_csat,
    ROUND(AVG(resolution_days), 2) AS avg_resolution_days
FROM feedback
GROUP BY service_category
ORDER BY total_responses DESC;
"""
    with open(queries_sql_path, 'w', encoding='utf-8') as f:
        f.write(queries_sql)

    # 3. Create SQLite DB and populate
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute schema
    cursor.executescript(schema_sql)
    
    # Load DataFrame
    df = pd.read_csv(cleaned_csv)
    df.to_sql('feedback', conn, if_exists='append', index=False)
    
    conn.commit()
    
    # Verify count
    cursor.execute("SELECT COUNT(*) FROM feedback;")
    db_count = cursor.fetchone()[0]
    
    print(f"SQLite DB initialized successfully at {db_path}.")
    print(f"Loaded {db_count} records into 'feedback' table.")
    
    # 4. Test all queries
    print("\nExecuting and validating all 14 analytical SQL queries:")
    query_blocks = [q.strip() for q in queries_sql.split(';') if q.strip() and not q.strip().startswith('--')]
    
    for idx, query in enumerate(query_blocks, 1):
        # get title line
        first_line = query.split('\n')[0] if query.split('\n')[0].startswith('--') else f"Query {idx}"
        cursor.execute(query)
        res = cursor.fetchall()
        print(f"[{idx}/14] {first_line}: {len(res)} rows returned. Sample: {res[0] if res else 'Empty'}")
        
    conn.close()

if __name__ == '__main__':
    setup_sqlite()
