# Customer Voice & NPS Analytics - Comprehensive Interview Guide

## Overview
This interview preparation guide provides concise, truthful, and defensible answers aligned precisely with the implementation of this portfolio project. Every answer reflects the actual code, SQL schema, REST API endpoints, DAX measures, and business findings in the repository.

---

## 1. DATASET QUESTIONS

### Q1: Why did you use a synthetic dataset?
- **Answer:** I used a synthetic dataset for educational and portfolio demonstration purposes to ensure data privacy and avoid exposing proprietary corporate information. Creating synthetic data also allowed me to seed controlled real-world data quality issues (duplicates, nulls, out-of-range values) to demonstrate data profiling, validation, and cleaning pipelines.

### Q2: Why 6,000 raw records?
- **Answer:** 6,000 records represents a realistic 12-month survey volume for a mid-sized B2B/B2C SaaS company (~500 responses/month). It is large enough to show meaningful statistical trends across regions and segments, while remaining lightweight enough to process instantaneously in Python, SQLite, and Power BI.

### Q3: Why these 13 columns?
- **Answer:** These 13 columns capture both **customer metadata** (`customer_id`, `region`, `customer_segment`, `industry`), **survey touchpoints** (`survey_date`, `response_channel`, `service_category`), **customer satisfaction metrics** (`nps_score`, `csat_score`), **operational service SLAs** (`resolution_days`, `issue_resolved`), and **qualitative feedback** (`feedback_text`). Together, they enable cross-functional analysis joining CSAT/NPS with operational resolution performance.

### Q4: What data-quality issues did you intentionally introduce?
- **Answer:** I introduced 9 types of realistic anomalies into the raw data:
  1. 35 exact duplicate survey response rows
  2. 90 missing CSAT scores (~1.5%)
  3. 59 missing industry values (~1.0%)
  4. 59 missing feedback text fields (~1.0%)
  5. 79 non-standard service category spellings (mixed casing/whitespace)
  6. 15 out-of-range NPS scores (<0 or >10, e.g. -2, 99)
  7. 12 out-of-range CSAT scores (<1 or >5, e.g. 0, 6)
  8. 14 negative resolution days (e.g. -5)
  9. 10 malformed/unparseable dates (e.g. '2025-13-45', 'INVALID_DATE')

### Q5: How did you detect and clean them?
- **Answer:** I used Pandas in `python/data_profiling.py` and `python/data_cleaning.py`. Duplicates were detected via `df.duplicated(subset=['response_id'])` (35 rows dropped). Missing industries were imputed with `"Unknown"`, missing feedback with `"No feedback provided"`, and missing CSAT with the median CSAT score (`4`). Range validation filters dropped 51 invalid records violating domain rules (`0 <= nps <= 10`, `1 <= csat <= 5`, `resolution_days >= 0`, valid dates). Text categories were standardized via `.str.strip().str.title()`. Final clean record count: **5,914**.

---

## 2. PYTHON / PANDAS QUESTIONS

### Q1: Why Python and Pandas for cleaning?
- **Answer:** Python and Pandas provide a programmatically reproducible, automated data cleaning pipeline. Unlike manual Excel edits or UI-based tools, Python scripts can be version-controlled, automated in CI/CD pipelines, and audited end-to-end via automated logging.

### Q2: What Pandas functions did you use?
- **Answer:** `pd.read_csv()`, `df.duplicated()`, `df.drop_duplicates()`, `df.isna()`, `df.fillna()`, `pd.to_numeric()`, `pd.to_datetime()`, `.str.strip()`, `.str.title()`, `df.groupby()`, `df.value_counts()`, and `df.to_csv()`.

### Q3: Why perform cleaning in Python instead of Power Query?
- **Answer:** Centralizing cleaning logic in Python ensures that downstream consumers (SQLite database, REST API, SQL queries, Python notebooks, and BI tools) all receive clean, consistent data from a single source of truth, rather than repeating transformations separately in each tool.

---

## 3. SQL & SQLITE QUESTIONS

### Q1: Why SQLite?
- **Answer:** SQLite is a serverless, self-contained relational database that requires zero infrastructure overhead. It allows querying using standard ANSI SQL while keeping the database file lightweight and easily shareable inside the repository (`data/customer_voice.db`).

### Q2: What queries did you write?
- **Answer:** I wrote 14 analytical queries in `sql/analysis_queries.sql` covering total responses, average NPS/CSAT, promoter/passive/detractor counts, net NPS formula, regional/segment/category breakdowns, channel volume, and resolution SLA analysis by NPS category.

### Q3: Explain key SQL concepts used (`GROUP BY`, `WHERE`, `HAVING`, `CASE`).
- **Answer:**
  - `WHERE`: Filters rows prior to aggregation (e.g. `WHERE nps_score >= 9`).
  - `GROUP BY`: Aggregates metrics by categorical dimensions (e.g. `GROUP BY region`).
  - `HAVING`: Filters aggregated group results post-`GROUP BY`.
  - `CASE`: Conditional expressions used to build the net NPS metric inside SQL: `SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END)`.

---

## 4. FASTAPI & REST API QUESTIONS

### Q1: Why build a REST API?
- **Answer:** In modern data engineering, BI tools often consume data from enterprise microservices or data lakes rather than direct file system paths. Building a REST API using FastAPI demonstrates an end-to-end data pipeline where data flows from database -> API -> Web/BI tool.

### Q2: What endpoints did you create?
- **Answer:** Two endpoints:
  1. `GET /api/health`: Verifies API operational status, SQLite connection, and total record count.
  2. `GET /api/feedback`: Queries SQLite and returns cleaned records as a JSON array with query parameter filtering (`skip`, `limit`, `region`, `customer_segment`).

### Q3: Why didn't you build POST/PUT/DELETE endpoints?
- **Answer:** This API's sole responsibility in the data pipeline is read-only analytical data ingestion for reporting (ETL/ELT pipeline). Adding mutation endpoints (POST/PUT/DELETE) without authentication would introduce security risks without adding analytical value.

---

## 5. POWER QUERY & POWER BI QUESTIONS

### Q1: How does Power Query fetch API data?
- **Answer:** Power Query uses `Web.Contents("http://127.0.0.1:8000/api/feedback")` combined with `Json.Document()` and `Table.ExpandRecordColumn()` to parse the REST API's JSON array into structured tabular format.

### Q2: What transformations did Power Query perform?
- **Answer:** In Power Query, I set explicit column data types (Date, Int64, Text), added an M calculated column for `nps_category`, applied Title Case standardization, and validated schema structure.

### Q3: Explain your Power BI Data Model.
- **Answer:** I implemented a Star Schema with `feedback` as the central Fact table connected in a 1-to-many (`1:*`) relationship to a DAX-calculated `Dim_Date` calendar table (`Dim_Date[Date]` -> `feedback[survey_date]`).

---

## 6. DAX & METRIC QUESTIONS

### Q1: What is NPS and how is it calculated?
- **Answer:** Net Promoter Score (NPS) measures customer advocacy on a scale of 0 to 10:
  - **Promoters:** 9–10
  - **Passives:** 7–8
  - **Detractors:** 0–6
  - **Net NPS Score:** `NPS = (% Promoters - % Detractors) * 100` represented as a point score value ranging from -100 to +100 (e.g. `-22.6`).

### Q2: Why use `DIVIDE()` in DAX instead of `/`?
- **Answer:** `DIVIDE(numerator, denominator, alternateResult)` handles division-by-zero safely by returning `0` or `BLANK()` instead of raising runtime calculation errors in visuals.

### Q3: Measure vs. Calculated Column?
- **Answer:** 
  - **Calculated Column:** Evaluated row-by-row during data refresh and stored in RAM. Used for slicers and row groupings (`nps_category`).
  - **Measure:** Evaluated dynamically at query time based on user visual filter context. Consumes zero storage RAM and is used for numerical aggregations (`Total Responses`, `NPS`).

---

## 7. BUSINESS INSIGHTS & STRATEGY

### Q1: What were your top business findings?
- **Answer:**
  1. Overall Net NPS Score is **-22.6** (points) with an Average CSAT of **3.07**.
  2. Detractors experienced **7.75 average resolution days**, compared to **1.40 days** for Promoters—showing operational latency is strongly associated with customer dissatisfaction.
  3. Pricing (**-62.6 NPS**) and Delivery (**-62.4 NPS**) are the primary negative sentiment drivers.
  4. Enterprise accounts report NPS of **-21.8**, Mid-Market **-23.5**, and SMB **-21.9**.

### Q2: What would you improve in a production environment?
- **Answer:**
  1. Migrate SQLite to PostgreSQL or Snowflake for multi-user concurrency and enterprise data warehousing.
  2. Containerize the FastAPI backend using Docker.
  3. Deploy automated CI/CD unit testing (PyTest) for data cleaning functions.
  4. Implement OAuth2 / JWT authentication on API endpoints.
  5. Schedule automated incremental refreshes in Power BI Service via Gateway.
