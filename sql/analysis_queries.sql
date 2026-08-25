-- Customer Voice & NPS Analytics - Analytical Queries

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
