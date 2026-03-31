-- ============================================================================
-- Phase 7: Materialized View - Trade by Country
-- Purpose: Pre-computed trade aggregations by origin country
-- ============================================================================

-- Drop existing materialized view if exists
DROP MATERIALIZED VIEW IF EXISTS mv_trade_by_country;

-- Create materialized view with aggregated trade by country
CREATE MATERIALIZED VIEW mv_trade_by_country AS
SELECT 
    -- Country dimension (ISO codes only - no real identifiers)
    di.origin_country AS country_code,
    cr.country_name AS country_name,
    
    -- Volume metrics
    COUNT(DISTINCT d.declaration_id) AS total_declarations,
    COUNT(di.item_id) AS total_items,
    
    -- Value metrics
    SUM(di.customs_value) AS total_customs_value,
    SUM(di.customs_duty) AS total_customs_duty,
    SUM(di.vat_amount) AS total_vat_collected,
    SUM(di.excise_amount) AS total_excise_collected,
    
    -- Averages
    AVG(di.customs_value) AS average_shipment_value,
    
    -- Effective rates
    CASE 
        WHEN SUM(di.customs_value) > 0 
        THEN SUM(di.customs_duty) / SUM(di.customs_value)
        ELSE 0
    END AS effective_duty_rate,
    
    CASE 
        WHEN SUM(di.customs_value) + SUM(di.customs_duty) > 0 
        THEN SUM(di.vat_amount) / (SUM(di.customs_value) + SUM(di.customs_duty))
        ELSE 0
    END AS effective_vat_rate,
    
    -- Top HS chapters (aggregated - no individual codes)
    (SELECT STRING_AGG(DISTINCT LEFT(di.hs_code, 2), ', ' ORDER BY LEFT(di.hs_code, 2))
     FROM declaration_items di2
     JOIN declarations d2 ON di2.declaration_id = d2.declaration_id
     WHERE d2.status = 'CLEARED' 
       AND di2.origin_country = di.origin_country
       AND LEFT(di2.hs_code, 2) IN ('84', '85', '87', '62', '90', '30', '39')
     LIMIT 5) AS top_hs_chapters,
    
    -- Metadata
    MAX(d.updated_at) AS last_updated

FROM declaration_items di
JOIN declarations d ON di.declaration_id = d.declaration_id
LEFT JOIN country_reference cr ON di.origin_country = cr.country_code
WHERE d.status = 'CLEARED'
GROUP BY 
    di.origin_country,
    cr.country_name
HAVING COUNT(DISTINCT d.declaration_id) >= 5  -- Privacy threshold
ORDER BY total_customs_value DESC;

-- Create unique index for concurrent refresh
CREATE UNIQUE INDEX idx_mv_trade_by_country_code 
    ON mv_trade_by_country (country_code);

-- Create indexes for query patterns
CREATE INDEX idx_mv_trade_by_country_value 
    ON mv_trade_by_country (total_customs_value DESC);

COMMENT ON MATERIALIZED VIEW mv_trade_by_country IS 
    'Aggregated trade by country - REFRESH ON SCHEDULE - Privacy threshold: 5+ declarations';

-- ============================================================================
-- Access Control
-- ============================================================================

GRANT SELECT ON mv_trade_by_country TO analytics_reader;