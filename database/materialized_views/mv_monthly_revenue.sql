-- ============================================================================
-- Phase 7: Materialized View - Monthly Revenue
-- Purpose: Pre-computed monthly revenue aggregations for fast analytics
-- ============================================================================

-- Drop existing materialized view if exists
DROP MATERIALIZED VIEW IF EXISTS mv_monthly_revenue;

-- Create materialized view with aggregated revenue by month
CREATE MATERIALIZED VIEW mv_monthly_revenue AS
SELECT 
    -- Time dimension
    EXTRACT(YEAR FROM d.declaration_date)::INTEGER AS year,
    EXTRACT(MONTH FROM d.declaration_date)::INTEGER AS month,
    TO_CHAR(d.declaration_date, 'YYYY-MM') AS month_label,
    
    -- Status breakdown
    COUNT(*) FILTER (WHERE d.status = 'CLEARED') AS cleared_declarations,
    COUNT(*) FILTER (WHERE d.status = 'REJECTED') AS rejected_declarations,
    COUNT(*) FILTER (WHERE d.status = 'PROCESSED') AS processed_declarations,
    COUNT(*) AS total_declarations,
    
    -- Volume metrics
    SUM(d.total_items) AS total_items,
    
    -- Value metrics
    SUM(d.total_customs_value) AS total_customs_value,
    SUM(d.total_customs_duty) AS total_customs_duty,
    SUM(d.total_excise) AS total_excise,
    SUM(d.total_vat) AS total_vat,
    SUM(d.total_tax_liability) AS total_tax_liability,
    
    -- Averages
    AVG(d.total_customs_value) AS average_declaration_value,
    AVG(d.total_customs_duty) AS average_duty,
    AVG(d.total_vat) AS average_vat,
    
    -- Duty rate average
    CASE 
        WHEN SUM(d.total_customs_value) > 0 
        THEN SUM(d.total_customs_duty) / SUM(d.total_customs_value)
        ELSE 0
    END AS effective_duty_rate,
    
    -- Metadata
    MAX(d.updated_at) AS last_updated

FROM declarations d
WHERE d.status = 'CLEARED'
GROUP BY 
    EXTRACT(YEAR FROM d.declaration_date),
    EXTRACT(MONTH FROM d.declaration_date),
    TO_CHAR(d.declaration_date, 'YYYY-MM')
ORDER BY year, month;

-- Create unique index for concurrent refresh
CREATE UNIQUE INDEX idx_mv_monthly_revenue_ym 
    ON mv_monthly_revenue (year, month);

-- Create indexes for common query patterns
CREATE INDEX idx_mv_monthly_revenue_year 
    ON mv_monthly_revenue (year);

CREATE INDEX idx_mv_monthly_revenue_month_label 
    ON mv_monthly_revenue (month_label);

COMMENT ON MATERIALIZED VIEW mv_monthly_revenue IS 
    'Aggregated monthly revenue metrics - REFRESH ON SCHEDULE';

-- ============================================================================
-- Access Control
-- ============================================================================

-- Grant read-only access to analytics role
GRANT SELECT ON mv_monthly_revenue TO analytics_reader;

-- Deny direct table access (use views/materialized views only)
-- This is handled by REVOKE in 003_constraints.sql