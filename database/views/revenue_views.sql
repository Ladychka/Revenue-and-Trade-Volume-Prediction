-- ============================================================================
-- Revenue Views
-- Phase 7 - Database Views Implementation
-- Purpose: Aggregated revenue views for API access
-- ============================================================================

-- View: Monthly revenue summary
CREATE OR REPLACE VIEW v_monthly_revenue AS
SELECT 
    EXTRACT(YEAR FROM declaration_date) AS year,
    EXTRACT(MONTH FROM declaration_date) AS month,
    TO_CHAR(declaration_date, 'YYYY-MM') AS month_label,
    COUNT(*) FILTER (WHERE status = 'CLEARED') AS cleared_declarations,
    SUM(total_customs_value) AS total_customs_value,
    SUM(total_customs_duty) AS total_customs_duty,
    SUM(total_vat) AS total_vat,
    SUM(total_excise) AS total_excise,
    SUM(total_tax_liability) AS total_tax_liability
FROM declarations
WHERE status = 'CLEARED'
GROUP BY EXTRACT(YEAR FROM declaration_date), EXTRACT(MONTH FROM declaration_date), TO_CHAR(declaration_date, 'YYYY-MM');

-- View: Revenue by port summary
CREATE OR REPLACE VIEW v_revenue_by_port AS
SELECT 
    d.office_code AS port_code,
    pr.port_name,
    COUNT(*) AS total_declarations,
    SUM(d.total_customs_value) AS total_value,
    SUM(d.total_customs_duty) AS total_duty,
    SUM(d.total_vat) AS total_vat
FROM declarations d
LEFT JOIN port_reference pr ON d.office_code = pr.port_code
WHERE d.status = 'CLEARED'
GROUP BY d.office_code, pr.port_name;

-- View: Revenue by tax type
CREATE OR REPLACE VIEW v_revenue_by_tax_type AS
SELECT 
    SUM(total_customs_duty) AS total_duty,
    SUM(total_vat) AS total_vat,
    SUM(total_excise) AS total_excise,
    SUM(total_tax_liability) AS total_liability,
    COUNT(*) AS total_declarations
FROM declarations
WHERE status = 'CLEARED';
