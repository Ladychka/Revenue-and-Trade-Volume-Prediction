-- ============================================================================
-- Phase 7: Materialized View - Trade by HS Code
-- Purpose: Pre-computed trade aggregations by HS chapter/heading
-- ============================================================================

-- Drop existing materialized view if exists
DROP MATERIALIZED VIEW IF EXISTS mv_trade_by_hs;

-- Create materialized view with aggregated trade by HS chapter
CREATE MATERIALIZED VIEW mv_trade_by_hs AS
SELECT 
    -- HS dimension (chapter level only - no tariff line detail)
    LEFT(di.hs_code, 2) AS hs_chapter,
    hs.chapter AS chapter_description,
    
    -- Volume metrics
    COUNT(DISTINCT d.declaration_id) AS total_declarations,
    COUNT(di.item_id) AS total_items,
    SUM(di.quantity) AS total_quantity,
    di.quantity_unit AS quantity_unit,
    
    -- Value metrics
    SUM(di.customs_value) AS total_customs_value,
    SUM(di.customs_duty) AS total_customs_duty,
    SUM(di.vat_amount) AS total_vat_collected,
    
    -- Averages
    AVG(di.customs_value) AS average_shipment_value,
    AVG(di.quantity) AS average_quantity,
    
    -- Effective rates
    CASE 
        WHEN SUM(di.customs_value) > 0 
        THEN SUM(di.customs_duty) / SUM(di.customs_value)
        ELSE 0
    END AS effective_duty_rate,
    
    -- Origin breakdown (top 5 countries, aggregated)
    (SELECT COUNT(DISTINCT di2.origin_country)
     FROM declaration_items di2
     JOIN declarations d2 ON di2.declaration_id = d2.declaration_id
     WHERE d2.status = 'CLEARED' 
       AND LEFT(di2.hs_code, 2) = LEFT(di.hs_code, 2)) AS origin_countries,
    
    -- Metadata
    MAX(d.updated_at) AS last_updated

FROM declaration_items di
JOIN declarations d ON di.declaration_id = d.declaration_id
LEFT JOIN hs_code_reference hs ON LEFT(di.hs_code, 2) = hs.chapter
WHERE d.status = 'CLEARED'
GROUP BY 
    LEFT(di.hs_code, 2),
    hs.chapter,
    di.quantity_unit
HAVING COUNT(DISTINCT d.declaration_id) >= 5  -- Privacy threshold
ORDER BY total_customs_value DESC;

-- Create unique index for concurrent refresh
CREATE UNIQUE INDEX idx_mv_trade_by_hs_chapter 
    ON mv_trade_by_hs (hs_chapter);

-- Create indexes for query patterns
CREATE INDEX idx_mv_trade_by_hs_value 
    ON mv_trade_by_hs (total_customs_value DESC);

CREATE INDEX idx_mv_trade_by_hs_items 
    ON mv_trade_by_hs (total_items DESC);

COMMENT ON MATERIALIZED VIEW mv_trade_by_hs IS 
    'Aggregated trade by HS chapter - REFRESH ON SCHEDULE - Privacy threshold: 5+ declarations';

-- ============================================================================
-- Access Control
-- ============================================================================

GRANT SELECT ON mv_trade_by_hs TO analytics_reader;