import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'customer_voice.db'))

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"SQLite database not found at {DB_PATH}. Please initialize database first.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_health_status():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM feedback;")
        count = cursor.fetchone()[0]
        conn.close()
        return {
            "status": "healthy",
            "database": "connected",
            "db_path": DB_PATH,
            "total_records": count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

def fetch_feedback(skip: int = 0, limit: int = 10000, region: str = None, customer_segment: str = None, service_category: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM feedback WHERE 1=1"
    params = []
    
    if region:
        query += " AND region = ?"
        params.append(region)
    if customer_segment:
        query += " AND customer_segment = ?"
        params.append(customer_segment)
    if service_category:
        query += " AND service_category = ?"
        params.append(service_category)
        
    query += " ORDER BY survey_date DESC LIMIT ? OFFSET ?"
    params.extend([limit, skip])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
