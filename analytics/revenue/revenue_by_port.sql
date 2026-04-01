-- ============================================================================
-- Revenue by Port Analytics Query
-- Phase 7 - Analytics Implementation
-- Purpose: Revenue breakdown by customs port
-- ============================================================================

SELECT 
    d.office_code AS port_code,
    pr.port_name,
    COUNT(*) AS total_declarations,
    COUNT(*) FILTER (WHERE d.status = 'CLEARED') AS cleared_declarations,
    SUM(d.total_customs_value) AS total_customs_value,
    SUM(d.total_customs_duty) AS total_customs_duty,
    SUM(d.total_vat) AS total_vat,
    SUM(d.total_tax_liability) AS total_tax_liability,
    AVG(d.total_customs_value) AS avg_declaration_value
FROM declarations d
LEFT JOIN port_reference pr ON d.office_code = pr.port_code
WHERE d.status = 'CLEARED'
GROUP BY d.office_code, pr.port_name
ORDER BY total_tax_liability DESC
LIMIT 20;
