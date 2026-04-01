-- ============================================================================
-- Compliance Views
-- Phase 7 - Database Views Implementation
-- Purpose: Aggregated compliance views for API access
-- ============================================================================

-- View: Variance summary
CREATE OR REPLACE VIEW v_variance_summary AS
SELECT 
    EXTRACT(YEAR FROM declaration_date) AS year,
    EXTRACT(MONTH FROM declaration_date) AS month,
    SUM(total_customs_value) AS actual_value,
    SUM(total_customs_duty) AS actual_duty,
    SUM(total_customs_duty) / NULLIF(SUM(total_customs_value), 0) AS effective_duty_rate,
    AVG(total_customs_duty / NULLIF(total_customs_value, 0)) AS avg_duty_rate
FROM declarations
WHERE status = 'CLEARED' AND total_customs_value > 0
GROUP BY EXTRACT(YEAR FROM declaration_date), EXTRACT(MONTH FROM declaration_date);

-- View: Risk indicators
CREATE OR REPLACE VIEW v_risk_indicators AS
SELECT 
    COUNT(*) AS total_declarations,
    COUNT(*) FILTER (WHERE total_customs_duty / NULLIF(total_customs_value, 0) < 0.02) AS low_duty_count,
    COUNT(*) FILTER (WHERE total_customs_duty / NULLIF(total_customs_value, 0) < 0.02)::float / COUNT(*) AS low_duty_ratio,
    AVG(total_customs_duty / NULLIF(total_customs_value, 0)) AS avg_duty_rate
FROM declarations
WHERE status = 'CLEARED' AND total_customs_value > 0;
