-- ============================================================================
-- Trade by Country Analytics Query
-- Phase 7 - Analytics Implementation
-- Purpose: Trade volume breakdown by origin country
-- ============================================================================

SELECT 
    di.origin_country AS country_code,
    cr.country_name,
    COUNT(DISTINCT d.declaration_id) AS total_declarations,
    COUNT(di.item_id) AS total_items,
    SUM(di.customs_value) AS total_customs_value,
    SUM(di.customs_duty) AS total_customs_duty,
    SUM(di.vat_amount) AS total_vat,
    AVG(di.customs_value) AS avg_shipment_value
FROM declaration_items di
JOIN declarations d ON di.declaration_id = d.declaration_id
LEFT JOIN country_reference cr ON di.origin_country = cr.country_code
WHERE d.status = 'CLEARED'
GROUP BY di.origin_country, cr.country_name
ORDER BY total_customs_value DESC
LIMIT 20;
