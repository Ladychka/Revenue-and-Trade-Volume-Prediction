-- ============================================================================
-- Compliance: Variance Summary Analytics
-- Phase 7 - Analytics Implementation
-- Purpose: Revenue variance from expected values
-- ============================================================================

SELECT 
    EXTRACT(YEAR FROM declaration_date) AS year,
    EXTRACT(MONTH FROM declaration_date) AS month,
    SUM(total_customs_value) AS actual_value,
    SUM(total_customs_duty) AS actual_duty,
    SUM(total_vat) AS actual_vat,
    -- Expected values based on historical average rates
    SUM(total_customs_value) * 0.06 AS expected_duty,
    SUM(total_customs_value) * 0.17 AS expected_vat,
    -- Variance
    SUM(total_customs_duty) - (SUM(total_customs_value) * 0.06) AS duty_variance,
    SUM(total_vat) - (SUM(total_customs_value) * 0.17) AS vat_variance
FROM declarations
WHERE status = 'CLEARED'
GROUP BY EXTRACT(YEAR FROM declaration_date), EXTRACT(MONTH FROM declaration_date)
ORDER BY year, month;
