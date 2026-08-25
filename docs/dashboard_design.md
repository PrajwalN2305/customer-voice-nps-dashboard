# Power BI Dashboard Design Documentation

## Executive Overview
This document details the visual design, page layouts, visual container configurations, color themes, user experience (UX) principles, and visual-by-visual business purposes for the **Customer Voice & NPS Analytics Dashboard**.

The dashboard comprises **EXACTLY TWO** analytical report pages:
1. **Page 1: Customer Experience Overview** (Executive KPIs, Monthly Trends, Regional & Segment NPS)
2. **Page 2: Voice of Customer Analysis** (Service Category Diagnostics, Operational Latency, Escalation Detail Tables)

---

## Design System & Visual Palette

- **Theme:** Professional Dark Slate (`#0F172A` background, `#1E293B` card containers, `#38BDF8` accents).
- **Typography:** Modern clean sans-serif (Segoe UI / Inter).
- **Color Coding:**
  - **Promoters / Positive:** Vibrant Emerald Green (`#10B981`)
  - **Passives / Neutral:** Amber Gold (`#F59E0B`)
  - **Detractors / Negative:** Crimson Red (`#EF4444`)
  - **Primary Metric / Neutral Accents:** Sky Blue (`#38BDF8`), Royal Blue (`#3B82F6`), Soft Purple (`#8B5CF6`)

---

## Page 1: Customer Experience Overview

### Purpose
Serves as an executive monitoring dashboard providing high-level visibility into overall Net Promoter Score (NPS), customer satisfaction (CSAT), monthly performance trends, and regional/segment breakdowns.

### Layout & Visual Grid

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TITLE BANNER: Customer Voice & NPS Analytics                                            │
│ Global Slicers: [Region] [Customer Segment] [Service Category] [Survey Date Range]      │
├───────────────────┬───────────────────┬───────────────────┬────────────────────────────┤
│ KPI CARD 1        │ KPI CARD 2        │ KPI CARD 3        │ KPI CARD 4                 │
│ Total Responses   │ Net NPS Score     │ Average CSAT      │ Promoter Share             │
│ 5,914             │ -22.6             │ 3.07              │ 25.1%                      │
├───────────────────┴───────────────────┼───────────────────┴────────────────────────────┤
│ VISUAL 1: Line Chart                  │ VISUAL 2: Horizontal Bar Chart                 │
│ Monthly NPS Trend (2025)              │ NPS by Region                                  │
├───────────────────┬───────────────────┴───────────────────┬────────────────────────────┤
│ VISUAL 3: Donut   │ VISUAL 4: Column Chart                │ VISUAL 5: Column Chart     │
│ NPS Category Dist │ Average CSAT by Customer Segment      │ Response Volume by Channel │
│ (Promoter/Pass/Det│                                       │                            │
└───────────────────┴───────────────────────────────────────┴────────────────────────────┘
```

### Visual Specifications

| Container # | Visual Name | Chart Type | Fields & Metrics Used | Business Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **KPI 1** | Total Responses | Card | `[Total Responses]` measure | Tracks overall survey volume to ensure sample size validity. |
| **KPI 2** | Net NPS Score | Card | `[NPS]` measure (Point Score) | Primary executive advocacy metric (-100 to +100 point scale). |
| **KPI 3** | Average CSAT | Card | `[Average CSAT]` measure | Operational satisfaction benchmark on 1–5 scale. |
| **KPI 4** | Promoter Share | Card | `[Promoter %]` measure | Percentage share of loyal customer advocates (NPS 9–10). |
| **Visual 1** | Monthly NPS Trend | Line Chart | X: `Dim_Date[YearMonth]`, Y: `[NPS]` | Identifies multi-month satisfaction trajectory and seasonal shifts. |
| **Visual 2** | NPS by Region | Horizontal Bar | Y: `feedback[region]`, X: `[NPS]` | Highlights geographical performance disparities (e.g. NA vs APAC). |
| **Visual 3** | NPS Category Distribution | Donut Chart | Legend: `nps_category`, Values: `[Total Responses]` | Visualizes breakdown of Promoters (25.1%), Passives (27.2%), and Detractors (47.7%). |
| **Visual 4** | Avg CSAT by Customer Segment | Column Chart | X: `customer_segment`, Y: `[Average CSAT]` | Compares satisfaction across Enterprise, Mid-Market, and SMB accounts. |
| **Visual 5** | Response Volume by Channel | Column Chart | X: `response_channel`, Y: `[Total Responses]` | Evaluates submission channel usage (Email, Phone, Web, In-App). |

---

## Page 2: Voice of Customer Analysis

### Purpose
Provides tactical diagnostic capabilities for product managers and support leads to pinpoint exact service category bottlenecks, analyze operational resolution latency, and inspect low-NPS customer feedback comments.

### Layout & Visual Grid

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TITLE BANNER: Voice of Customer Analysis                                               │
│ Diagnostic Slicers: [Service Category] [Response Channel] [NPS Category]              │
├───────────────────────────────────────┬────────────────────────────────────────────────┤
│ VISUAL 1: Column Chart                │ VISUAL 2: Horizontal Bar Chart                 │
│ Response Dist by Service Category     │ NPS by Service Category                        │
├───────────────────────────────────────┼────────────────────────────────────────────────┤
│ VISUAL 3: Column Chart                │ VISUAL 4: Column Chart                         │
│ NPS by Customer Segment               │ Average Resolution Days by NPS Category        │
├───────────────────────────────────────┴────────────────────────────────────────────────┤
│ VISUAL 5 & 6: Data Grid Table                                                          │
│ Low-NPS Customer Feedback Detail Table (Detractor Escalations: NPS <= 6)               │
│ [Date] [Region] [Segment] [Category] [NPS] [CSAT] [Resolution Days] [Resolved] [Text]  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Visual Specifications

| Container # | Visual Name | Chart Type | Fields & Metrics Used | Business Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Visual 1** | Response Dist by Service Category | Column Chart | X: `service_category`, Y: `[Total Responses]` | Quantifies support ticket volume across Product, Support, Delivery, Pricing, Quality. |
| **Visual 2** | NPS by Service Category | Horizontal Bar | Y: `service_category`, X: `[NPS]` | Pinpoints key category friction points (e.g. Pricing -62.6 vs Product +3.2). |
| **Visual 3** | NPS by Customer Segment | Column Chart | X: `customer_segment`, Y: `[NPS]` | Analyzes NPS distribution across commercial account tiers. |
| **Visual 4** | Resolution Days by NPS Category | Column Chart | X: `nps_category`, Y: `[Average Resolution Days]` | Proves operational SLA gap (Detractors 7.75 days vs Promoters 1.40 days). |
| **Visual 5/6**| Low-NPS Feedback Table | Grid Table | Columns: `survey_date`, `region`, `segment`, `service_category`, `nps_score`, `csat_score`, `resolution_days`, `issue_resolved`, `feedback_text` | Provides verbatim verbatim detractor feedback (NPS <= 6) for root-cause analysis. |

---

## Interactive Slicer Configuration

Both pages include interactive slicers configured for single-select or multi-select filtering:
- **Region Slicer:** Filter all visuals by `North America`, `Europe`, `Asia-Pacific`, `Latin America`, `Middle East & Africa`.
- **Customer Segment Slicer:** Filter by `Enterprise`, `Mid-Market`, `SMB`.
- **Service Category Slicer:** Filter by `Customer Support`, `Delivery`, `Pricing`, `Product`, `Quality`.
- **Survey Date Range Slicer:** Continuous date range slider bound to `Dim_Date[Date]`.
