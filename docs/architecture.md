# End-to-End System Architecture Documentation

## Overview
This document describes the technical data pipeline and architecture of the **Customer Voice & NPS Analytics Dashboard**. The project implements a modern, decoupled analytics architecture spanning synthetic data generation, data profiling, pandas cleaning, relational database storage, REST API microservices, Power Query M transformations, and Power BI visualization.

---

## High-Level Architecture Diagram

![System Architecture](architecture.png)

```
6,000 Synthetic Customer Feedback Records
                    ↓
             Python / Pandas
                    ↓
        Data Profiling + EDA
                    ↓
       Data Cleaning + Validation
                    ↓
                 SQLite
                    ↓
                   SQL
                    ↓
                FastAPI
                    ↓
                  JSON
                    ↓
              Power Query
                    ↓
             Power BI Model
                    ↓
                  DAX
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
Customer Experience      Voice of Customer
     Dashboard                Dashboard
```

---

## Stage-by-Stage Architecture Breakdown

### 1. Data Ingestion & Synthetic Generation Layer
- **Source:** `python/generate_raw_data.py`
- **Output:** `data/raw/customer_voice_raw.csv` (6,000 raw records, 13 schema columns).
- **Purpose:** Simulates an enterprise customer feedback survey stream containing realistic operational dependencies (satisfaction correlation with resolution time) and intentional controlled data quality flaws.

### 2. Data Profiling & Exploratory Analysis Layer
- **Modules:** `python/data_profiling.py`, `python/eda.py`
- **Outputs:** `docs/dataset-profile.md`, `screenshots/eda/*.png`
- **Purpose:** Programmatically inspects missingness, data types, value distributions, and out-of-bounds metrics prior to cleaning. Computes exploratory EDA charts.

### 3. Data Cleaning & Validation Pipeline
- **Module:** `python/data_cleaning.py`
- **Output:** `data/processed/customer_voice_cleaned.csv` (5,914 cleaned records) & `docs/data-quality.md`
- **Purpose:** Applies deterministic data cleaning logic: removes duplicate responses, imputes missing categorical defaults, filters invalid scores (<0/>10 NPS, <1/>5 CSAT, negative resolution days), standardizes text categories, and validates schema output.

### 4. Relational Analytical Database Layer
- **Engine:** SQLite 3 (`data/customer_voice.db`)
- **Artifacts:** `sql/schema.sql`, `sql/analysis_queries.sql`
- **Purpose:** Serves as the central structured data repository storing the cleaned `feedback` fact table. Indexed on key dimension columns (`survey_date`, `region`, `customer_segment`, `service_category`) for query performance.

### 5. Microservice REST API Layer
- **Framework:** FastAPI / Uvicorn (`api/main.py`, `api/database.py`)
- **Endpoints:**
  - `GET /api/health`: Health status & SQLite connectivity verification.
  - `GET /api/feedback`: Exposes cleaned SQLite data as JSON payload with optional parameter filtering (`limit`, `skip`, `region`, `customer_segment`).
- **Purpose:** Decouples BI reporting tools from direct file system paths, enabling scalable JSON data delivery over standard web protocols.

### 6. Power Query Data Transformation Layer
- **Tool:** Power Query (M Language in Power BI Desktop)
- **Artifact:** `docs/power-query.md`
- **Purpose:** Fetches live JSON payload from FastAPI, expands record arrays into tabular format, enforces explicit data types, and adds custom M calculated attributes (`nps_category`).

### 7. Analytical Data Model & DAX Layer
- **Tool:** Power BI Data Model
- **Artifacts:** `docs/data-model.md`, `docs/dax-measures.md`
- **Purpose:** Establishes a Star-Schema data model connecting `feedback` to a DAX-calculated `Dim_Date` calendar table. Implements 9 explicit DAX measures (`Total Responses`, `NPS`, `Average CSAT`, etc.) for dynamic report slicing.

### 8. Interactive Reporting & Dashboard Presentation
- **Pages:**
  - **Page 1: Customer Experience Overview** (Executive KPIs, Monthly Trends, Regional & Segment NPS)
  - **Page 2: Voice of Customer Analysis** (Service Category Diagnostics, Operational Latency, Escalation Detail Tables)
- **Artifacts:** `screenshots/customer_experience_overview.png`, `screenshots/voice_of_customer.png`
- **Purpose:** Provides business stakeholders with interactive executive monitoring and tactical voice-of-customer diagnostics.
