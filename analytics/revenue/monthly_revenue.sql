-- ============================================================================
-- Monthly Revenue Analytics Query
-- Phase 7 - Analytics Implementation
-- Purpose: Get monthly revenue summaries for reporting
-- ============================================================================

-- Monthly revenue summary by status
SELECT 
    EXTRACT(YEAR FROM declaration_date) AS year,
    EXTRACT(MONTH FROM declaration_date) AS month,
    COUNT(*) FILTER (WHERE status = 'CLEARED') AS cleared_declarations,
    SUM(total_customs_value) AS total_customs_value,
    SUM(total_customs_duty) AS total_customs_duty,
    SUM(total_vat) AS total_vat,
    SUM(total_tax_liability) AS total_tax_liability
FROM declarations
WHERE status = 'CLEARED'
GROUP BY 
    EXTRACT(YEAR FROM declaration_date),
    EXTRACT(MONTH FROM declaration_date)
ORDER BY year, month;
