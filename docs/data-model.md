# Power BI Data Model Documentation

## Overview
The Power BI data model for the **Customer Voice & NPS Analytics Dashboard** follows a clean **Single-Fact / Star-Schema Design** centered on the `feedback` table, connected to a DAX-generated `Dim_Date` dimension table.

---

## Data Model Architecture

```
┌─────────────────────────────────┐
│            Dim_Date             │
│  (Calculated Dimension Table)   │
├─────────────────────────────────┤
│ PK: Date                        │
│     Year                        │
│     Quarter                     │
│     MonthNo                     │
│     MonthName                   │
│     YearMonth                   │
└────────────────┬────────────────┘
                 │ 1
                 │
                 │ (1-to-Many Relationship)
                 │ Filter direction: Single (Dim_Date -> feedback)
                 │
                 │ *
┌────────────────┴────────────────┐
│            feedback             │
│       (Primary Fact Table)      │
├─────────────────────────────────┤
│ PK: response_id                 │
│ FK: survey_date                 │
│     customer_id                 │
│     region                      │
│     customer_segment            │
│     industry                    │
│     response_channel            │
│     service_category            │
│     nps_score                   │
│     csat_score                  │
│     resolution_days             │
│     issue_resolved              │
│     feedback_text               │
└─────────────────────────────────┘
```

---

## Model Entities & Tables

### 1. `feedback` (Primary Fact Table)
- **Source:** Loaded via Power Query from REST API (`http://127.0.0.1:8000/api/feedback`).
- **Primary Key:** `response_id`
- **Granularity:** One record per survey response submission.
- **Record Count:** 5,914 cleaned records.
- **Role:** Stores all quantitative metrics (`nps_score`, `csat_score`, `resolution_days`) and dimensional attributes (`region`, `customer_segment`, `industry`, `response_channel`, `service_category`).

### 2. `Dim_Date` (Date Dimension Table)
- **Source:** Created dynamically in Power BI using DAX `CALENDARAUTO()`.
- **Primary Key:** `Date`
- **Role:** Enables Time Intelligence functions (YTD, Prior Month comparisons, continuous date slicing).
- **DAX Definition:**

```dax
Dim_Date = 
VAR MinDate = MIN(feedback[survey_date])
VAR MaxDate = MAX(feedback[survey_date])
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "MonthNo", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMM"),
    "YearMonth", FORMAT([Date], "YYYY-MM"),
    "DayOfWeek", FORMAT([Date], "DDD")
)
```

---

## Relationship Configuration

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter Direction | Active | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Dim_Date` | `Date` | `feedback` | `survey_date` | One-to-Many (`1:*`) | Single (`Dim_Date` filters `feedback`) | `True` | Standard Time Intelligence relationship filtering fact records by calendar periods. |

---

## Design Principles & Interview Rationale
1. **Why Single-Fact Model?**
   - The analysis focuses strictly on survey responses and operational resolution data captured at survey submission time. Denormalized attributes (`region`, `segment`, `category`) inside `feedback` optimize performance and eliminate unnecessary schema complexity.
2. **Why a Separate Date Table?**
   - Direct date slicing on `survey_date` can cause missing dates in monthly trend lines if no survey was submitted on a specific day. `Dim_Date` provides a continuous calendar range required for robust DAX Time Intelligence metrics.
3. **Mark as Date Table:**
   - `Dim_Date` is explicitly marked as a Date Table in Power BI Desktop to suppress automatic hidden local date hierarchies and optimize memory footprint.
