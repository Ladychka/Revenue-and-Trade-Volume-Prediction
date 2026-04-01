-- ============================================================================
-- Trade Views
-- Phase 7 - Database Views Implementation
-- Purpose: Aggregated trade views for API access
-- ============================================================================

-- View: Trade by country
CREATE OR REPLACE VIEW v_trade_by_country AS
SELECT 
    di.origin_country AS country_code,
    cr.country_name,
    COUNT(DISTINCT d.declaration_id) AS declarations,
    COUNT(di.item_id) AS items,
    SUM(di.customs_value) AS total_value,
    SUM(di.customs_duty) AS total_duty,
    AVG(di.customs_value) AS avg_value
FROM declaration_items di
JOIN declarations d ON di.declaration_id = d.declaration_id
LEFT JOIN country_reference cr ON di.origin_country = cr.country_code
WHERE d.status = 'CLEARED'
GROUP BY di.origin_country, cr.country_name;

-- View: Trade by HS code
CREATE OR REPLACE VIEW v_trade_by_hs AS
SELECT 
    LEFT(di.hs_code, 2) AS chapter,
    LEFT(di.hs_code, 4) AS heading,
    di.hs_code,
    hs.description AS hs_description,
    COUNT(DISTINCT d.declaration_id) AS declarations,
    COUNT(di.item_id) AS items,
    SUM(di.customs_value) AS total_value,
    SUM(di.customs_duty) AS total_duty
FROM declaration_items di
JOIN declarations d ON di.declaration_id = d.declaration_id
LEFT JOIN hs_code_reference hs ON di.hs_code = hs.hs_code
WHERE d.status = 'CLEARED'
GROUP BY LEFT(di.hs_code, 2), LEFT(di.hs_code, 4), di.hs_code, hs.description;

-- View: Trade summary
CREATE OR REPLACE VIEW v_trade_summary AS
SELECT 
    COUNT(DISTINCT d.declaration_id) AS total_declarations,
    COUNT(di.item_id) AS total_items,
    SUM(di.customs_value) AS total_value,
    SUM(di.customs_duty) AS total_duty,
    SUM(di.vat_amount) AS total_vat,
    AVG(di.customs_value) AS avg_value
FROM declaration_items di
JOIN declarations d ON di.declaration_id = d.declaration_id
WHERE d.status = 'CLEARED';
