-- ============================================================================
-- Compliance: High Risk Entities Query
-- Phase 7 - Analytics Implementation
-- Purpose: Identify potentially high-risk import patterns
-- Note: Uses synthetic IDs only, aggregated for privacy
-- ============================================================================

SELECT 
    LEFT(d.declarant_id, 9) AS importer_group,
    COUNT(*) AS total_declarations,
    SUM(d.total_customs_value) AS total_value,
    AVG(d.total_customs_duty / NULLIF(d.total_customs_value, 0)) AS avg_duty_rate,
    COUNT(*) FILTER (WHERE d.total_customs_duty / NULLIF(d.total_customs_value, 0) < 0.02) AS low_duty_count
FROM declarations d
WHERE d.status = 'CLEARED'
GROUP BY LEFT(d.declarant_id, 9)
HAVING COUNT(*) >= 10 
   AND AVG(d.total_customs_duty / NULLIF(d.total_customs_value, 0)) < 0.05
ORDER BY total_value DESC
LIMIT 20;
