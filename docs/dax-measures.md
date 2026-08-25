# Power BI DAX Measures Reference Guide

## Overview
This document contains the exact DAX (Data Analysis Expressions) measure formulas implemented in Power BI for the **Customer Voice & NPS Analytics Dashboard**. All DAX calculations have been cross-validated against Python and SQL outputs to ensure 100% mathematical consistency.

---

## Complete DAX Measures Dictionary

### 1. Total Responses
```dax
Total Responses = 
COUNTROWS(feedback)
```
- **Description:** Calculates the total count of valid survey responses.
- **DAX Functions:** `COUNTROWS`
- **Output Format:** Whole number with comma separators (e.g. `5,914`).
- **Validation:** Matches SQL `SELECT COUNT(*) FROM feedback` (5,914).

---

### 2. Promoters
```dax
Promoters = 
CALCULATE(
    COUNTROWS(feedback),
    feedback[nps_score] >= 9
)
```
- **Description:** Counts survey responses with an NPS score of 9 or 10.
- **DAX Functions:** `CALCULATE`, `COUNTROWS`
- **Output Format:** Whole number (e.g. `1,485`).
- **Validation:** Matches SQL `WHERE nps_score >= 9` (1,485).

---

### 3. Passives
```dax
Passives = 
CALCULATE(
    COUNTROWS(feedback),
    feedback[nps_score] = 7 || feedback[nps_score] = 8
)
```
- **Description:** Counts survey responses with an NPS score of 7 or 8.
- **DAX Functions:** `CALCULATE`, `COUNTROWS`
- **Output Format:** Whole number (e.g. `1,608`).
- **Validation:** Matches SQL `WHERE nps_score IN (7, 8)` (1,608).

---

### 4. Detractors
```dax
Detractors = 
CALCULATE(
    COUNTROWS(feedback),
    feedback[nps_score] <= 6
)
```
- **Description:** Counts survey responses with an NPS score of 0 through 6.
- **DAX Functions:** `CALCULATE`, `COUNTROWS`
- **Output Format:** Whole number (e.g. `2,821`).
- **Validation:** Matches SQL `WHERE nps_score <= 6` (2,821).

---

### 5. Promoter %
```dax
Promoter % = 
DIVIDE([Promoters], [Total Responses], 0)
```
- **Description:** Percentage share of promoter responses relative to total responses.
- **DAX Functions:** `DIVIDE` (Safe division preventing division-by-zero errors)
- **Output Format:** Percentage with 2 decimal places (e.g. `25.11%`).

---

### 6. Detractor %
```dax
Detractor % = 
DIVIDE([Detractors], [Total Responses], 0)
```
- **Description:** Percentage share of detractor responses relative to total responses.
- **DAX Functions:** `DIVIDE`
- **Output Format:** Percentage with 2 decimal places (e.g. `47.70%`).

---

### 7. Net NPS (Score / Point Metric)
```dax
NPS = 
([Promoter %] - [Detractor %]) * 100
```
- **Description:** Official Net Promoter Score represented as a point score value ranging from -100 to +100 (% Promoters minus % Detractors multiplied by 100).
- **DAX Functions:** Basic measure subtraction & scalar multiplication
- **Output Format:** Decimal number formatted with explicit sign (e.g. `-22.6` or `-22.59`). Note: NPS is formatted as a point score, NOT a percentage symbol.
- **Validation:** Matches Python/SQL calculation (`25.11% - 47.70% = -22.59` / `-22.6` rounded).

---

### 8. Average CSAT
```dax
Average CSAT = 
AVERAGE(feedback[csat_score])
```
- **Description:** Mean customer satisfaction rating across filtered responses.
- **DAX Functions:** `AVERAGE`
- **Output Format:** Decimal number with 2 decimal places (e.g. `3.07`).
- **Validation:** Matches SQL `SELECT AVG(csat_score) FROM feedback` (`3.07`).

---

### 9. Average Resolution Days
```dax
Average Resolution Days = 
AVERAGE(feedback[resolution_days])
```
- **Description:** Mean number of calendar days taken to resolve support issues.
- **DAX Functions:** `AVERAGE`
- **Output Format:** Decimal number with 2 decimal places (e.g. `4.89 days`).
- **Validation:** Matches SQL `SELECT AVG(resolution_days) FROM feedback` (`4.89`).

---

## Reconciliation Summary Table (Python vs SQL vs DAX)

| Metric | Python Cleaned Output | SQLite SQL Query Result | Power BI DAX Measure Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Total Responses** | 5,914 | 5,914 | 5,914 | ✅ 100% Match |
| **Promoter Count** | 1,485 | 1,485 | 1,485 | ✅ 100% Match |
| **Passive Count** | 1,608 | 1,608 | 1,608 | ✅ 100% Match |
| **Detractor Count** | 2,821 | 2,821 | 2,821 | ✅ 100% Match |
| **Promoter %** | 25.11% | 25.11% | 25.11% | ✅ 100% Match |
| **Detractor %** | 47.70% | 47.70% | 47.70% | ✅ 100% Match |
| **Net NPS Score** | -22.59 | -22.59 | -22.59 | ✅ 100% Match |
| **Average CSAT** | 3.07 | 3.07 | 3.07 | ✅ 100% Match |
| **Avg Resolution Days** | 4.89 days | 4.89 days | 4.89 days | ✅ 100% Match |
