# Power Query Data Extraction & Transformation Guide

## Overview
Power Query serves as the Business Intelligence (BI) data preparation layer in Power BI. While primary data validation and cleaning occur in Python, Power Query ingests JSON data from the REST API endpoint (`http://127.0.0.1:8000/api/feedback`), expands the JSON array into tabular form, enforces strict data types, creates calculated M attributes, and prepares the final reporting model.

---

## Complete M Code (`feedback` Query)

```powerquery
let
    // Step 1: Connect to REST API Endpoint
    Source = Json.Document(Web.Contents("http://127.0.0.1:8000/api/feedback")),
    
    # "Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    
    // Step 2: Expand Record Fields
    # "Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", 
        {"response_id", "customer_id", "survey_date", "region", "customer_segment", "industry", "response_channel", "service_category", "nps_score", "csat_score", "resolution_days", "issue_resolved", "feedback_text"}, 
        {"response_id", "customer_id", "survey_date", "region", "customer_segment", "industry", "response_channel", "service_category", "nps_score", "csat_score", "resolution_days", "issue_resolved", "feedback_text"}),
    
    // Step 3: Enforce Explicit Data Types
    # "Changed Type" = Table.TransformColumnTypes(#"Expanded Column1",{
        {"response_id", type text},
        {"customer_id", type text},
        {"survey_date", type date},
        {"region", type text},
        {"customer_segment", type text},
        {"industry", type text},
        {"response_channel", type text},
        {"service_category", type text},
        {"nps_score", Int64.Type},
        {"csat_score", Int64.Type},
        {"resolution_days", Int64.Type},
        {"issue_resolved", type text},
        {"feedback_text", type text}
    }),
    
    // Step 4: Add Custom Column for Power Query NPS Grouping
    # "Added NPS Category" = Table.AddColumn(#"Changed Type", "nps_category", each 
        if [nps_score] >= 9 then "Promoter" 
        else if [nps_score] >= 7 then "Passive" 
        else "Detractor", type text),
        
    // Step 5: Capitalize Category Names (Standardization Safety)
    # "Capitalized Words" = Table.TransformColumns(#"Added NPS Category",{{"service_category", Text.ToTitleCase, type text}})
in
    # "Capitalized Words"
```

---

## Step-by-Step Transformation Rationale

| Step # | Transformation Name | M Code Applied | Business & Technical Rationale |
| :--- | :--- | :--- | :--- |
| **1** | **Web API Source** | `Web.Contents("http://127.0.0.1:8000/api/feedback")` | Decouples report data ingestion from direct file system paths, enabling dynamic scheduled refreshes through the FastAPI backend. |
| **2** | **JSON Record Expansion** | `Table.ExpandRecordColumn(...)` | Flattens the array of JSON record objects into a structured 13-column tabular dataset required by Power BI. |
| **3** | **Type Transformation** | `Table.TransformColumnTypes(...)` | Prevents implicit text conversions; sets `survey_date` to `Date` (enables time intelligence), numerical fields to `Int64` (enables aggregation). |
| **4** | **NPS Grouping Column** | `Table.AddColumn(..., "nps_category", ...)` | Adds an M-calculated column classifying responses into `Promoter`, `Passive`, or `Detractor` for slicing and color conditional formatting. |
| **5** | **Category Standardization** | `Text.ToTitleCase` | Failsafe measure ensuring all service categories render cleanly across reports regardless of upstream API payload formatting. |

---

## Power Query vs. Python Pipeline Boundary

| Functionality | Handled in Python Pipeline | Handled in Power Query | Rationale |
| :--- | :---: | :---: | :--- |
| **Deduplication** | ✅ | ❌ | Deduplication requires full database audit and row hashes; best executed centrally in Python. |
| **Out-of-range Filtering** | ✅ | ❌ | Invalid NPS/CSAT rows are stripped prior to database entry to maintain data warehouse integrity. |
| **Null Imputation** | ✅ | ❌ | Categorical defaults (`"Unknown"`, `"No feedback provided"`) and median CSAT are set upstream. |
| **JSON Ingestion & Typing** | ❌ | ✅ | Power BI requires explicit schema definition upon API response parsing. |
| **BI Field Formatting** | ❌ | ✅ | UI text formatting and date typing are standard BI transformation practices. |
