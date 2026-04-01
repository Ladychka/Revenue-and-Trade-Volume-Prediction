-- ============================================================================
-- Trade by HS Code Analytics Query
-- Phase 7 - Analytics Implementation
-- Purpose: Trade volume breakdown by HS code chapter
-- ============================================================================

SELECT 
    LEFT(di.hs_code, 2) AS hs_chapter,
    hs.description AS chapter_description,
    COUNT(DISTINCT d.declaration_id) AS total_declarations,
    COUNT(di.item_id) AS total_items,
    SUM(di.quantity) AS total_quantity,
    SUM(di.customs_value) AS total_customs_value,
    SUM(di.customs_duty) AS total_customs_duty,
    SUM(di.vat_amount) AS total_vat,
    AVG(di.customs_value) AS avg_shipment_value
FROM declaration_items di
JOIN declarations d ON di.declaration_id = d.declaration_id
LEFT JOIN hs_code_reference hs ON LEFT(di.hs_code, 2) = hs.chapter
WHERE d.status = 'CLEARED'
GROUP BY LEFT(di.hs_code, 2), hs.description
ORDER BY total_customs_value DESC
LIMIT 20;
