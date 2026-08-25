-- Customer Voice & NPS Analytics Database Schema
-- Table: feedback

DROP TABLE IF EXISTS feedback;

CREATE TABLE feedback (
    response_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    survey_date DATE NOT NULL,
    region TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    industry TEXT NOT NULL,
    response_channel TEXT NOT NULL,
    service_category TEXT NOT NULL,
    nps_score INTEGER CHECK (nps_score >= 0 AND nps_score <= 10),
    csat_score INTEGER CHECK (csat_score >= 1 AND csat_score <= 5),
    resolution_days INTEGER CHECK (resolution_days >= 0),
    issue_resolved TEXT CHECK (issue_resolved IN ('Yes', 'No')),
    feedback_text TEXT
);

CREATE INDEX idx_feedback_survey_date ON feedback(survey_date);
CREATE INDEX idx_feedback_region ON feedback(region);
CREATE INDEX idx_feedback_segment ON feedback(customer_segment);
CREATE INDEX idx_feedback_category ON feedback(service_category);
