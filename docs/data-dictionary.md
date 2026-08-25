# Customer Voice & NPS Analytics - Data Dictionary

## Overview
This data dictionary details the schema, definitions, valid ranges, business rules, and dashboard usage for all 13 columns in the `feedback` dataset (`data/raw/customer_voice_raw.csv` and `data/processed/customer_voice_cleaned.csv`).

---

## Column Specifications

| # | Column Name | Data Type | Meaning / Description | Example Value | Valid Range / Categories | Used in Dashboard |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `response_id` | `TEXT` (String) | Primary key uniquely identifying each survey submission. | `RSP-0001` | Alphanumeric (`RSP-0001` to `RSP-6000`) | Yes (Card count) |
| **2** | `customer_id` | `TEXT` (String) | Customer account identifier. Customers can submit multiple survey responses over time. | `CUST-1042` | Alphanumeric (`CUST-1000` to `CUST-5199`) | Yes (Detail table) |
| **3** | `survey_date` | `DATE` (`YYYY-MM-DD`) | Date when the survey response was recorded. | `2025-06-15` | ISO Date (`2025-01-01` to `2025-12-31`) | Yes (Time trend, Slicer, Date table) |
| **4** | `region` | `TEXT` (Categorical) | Geographical region of the customer account. | `North America` | `North America`, `Europe`, `Asia-Pacific`, `Latin America`, `Middle East & Africa` | Yes (Bar chart, Slicer) |
| **5** | `customer_segment` | `TEXT` (Categorical) | Commercial tier classification of the customer. | `Enterprise` | `Enterprise`, `Mid-Market`, `SMB` | Yes (Bar chart, Slicer) |
| **6** | `industry` | `TEXT` (Categorical) | Industry sector of the customer organization. | `Technology` | `Technology`, `Healthcare`, `Finance`, `Retail`, `Manufacturing`, `Unknown` | Yes (Slicer, Filters) |
| **7** | `response_channel` | `TEXT` (Categorical) | Survey collection channel or touchpoint. | `Email` | `Email`, `Phone`, `Web`, `In-App` | Yes (Bar chart, Filters) |
| **8** | `service_category` | `TEXT` (Categorical) | Operational service domain related to customer survey feedback. | `Customer Support` | `Product`, `Delivery`, `Customer Support`, `Quality`, `Pricing` | Yes (Bar charts, Slicer, Feedback table) |
| **9** | `nps_score` | `INTEGER` | Net Promoter Score rating provided by customer (scale 0-10). | `9` | Integer `0` to `10` | Yes (NPS KPI, NPS category DAX) |
| **10** | `csat_score` | `INTEGER` | Customer Satisfaction Score rating (scale 1-5 Likert scale). | `4` | Integer `1` to `5` | Yes (CSAT KPI, Segment bar chart) |
| **11** | `resolution_days` | `INTEGER` | Number of elapsed calendar days to resolve the associated support issue. | `3` | Non-negative integer (`>= 0`) | Yes (Resolution days KPI, NPS bar chart) |
| **12** | `issue_resolved` | `TEXT` (Categorical) | Status flag indicating whether the support case was successfully closed. | `Yes` | `Yes`, `No` | Yes (Feedback detail table) |
| **13** | `feedback_text` | `TEXT` (String) | Short verbatim text submitted by the customer explaining their rating. | `"Support response was extremely fast."` | Text string / `"No feedback provided"` | Yes (Voice of Customer detail tables) |

---

## Derived Metrics & Calculations

### 1. NPS Classification Rule
- **Promoters:** `nps_score` >= 9 (High advocacy, low churn risk)
- **Passives:** `nps_score` in (7, 8) (Satisfied but unenthusiastic)
- **Detractors:** `nps_score` <= 6 (Unsatisfied, high escalation risk)

### 2. Net Promoter Score Formula
$$\text{Net NPS (\%)} = \left( \frac{\text{Count of Promoters} - \text{Count of Detractors}}{\text{Total Responses}} \right) \times 100$$
*(Range: -100% to +100%)*
