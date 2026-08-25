from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import uvicorn
from api.database import fetch_health_status, fetch_feedback

app = FastAPI(
    title="Customer Voice & NPS Analytics REST API",
    description="REST API pipeline delivering cleaned customer feedback records from SQLite database to Power Query and Power BI.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Customer Voice & NPS Analytics API",
        "documentation": "/docs",
        "health_check": "/api/health",
        "feedback_endpoint": "/api/feedback"
    }

@app.get("/api/health")
def get_health():
    """
    Health check endpoint returning API operational status and SQLite connection details.
    """
    status = fetch_health_status()
    if status["status"] == "unhealthy":
        raise HTTPException(status_code=500, detail=status)
    return status

@app.get("/api/feedback")
def get_feedback_records(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(10000, ge=1, le=10000, description="Maximum number of records to return"),
    region: Optional[str] = Query(None, description="Filter by geographical region"),
    customer_segment: Optional[str] = Query(None, description="Filter by segment (Enterprise, Mid-Market, SMB)"),
    service_category: Optional[str] = Query(None, description="Filter by service category")
):
    """
    Retrieve cleaned customer feedback survey responses from SQLite database.
    Exposes dataset directly for Power Query consumption.
    """
    try:
        records = fetch_feedback(
            skip=skip,
            limit=limit,
            region=region,
            customer_segment=customer_segment,
            service_category=service_category
        )
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
