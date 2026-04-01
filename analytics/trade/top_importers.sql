-- ============================================================================
-- Top Importers (Aggregated) Analytics Query
-- Phase 7 - Analytics Implementation
-- Purpose: Aggregated importer statistics (no individual names)
-- Note: Uses synthetic importer IDs only, no real company data
-- ============================================================================

SELECT 
    LEFT(d.declarant_id, 9) AS importer_prefix,  -- First part of synthetic ID only
    COUNT(*) AS total_declarations,
    SUM(d.total_customs_value) AS total_trade_value,
    SUM(d.total_customs_duty) AS total_duty,
    SUM(d.total_vat) AS total_vat,
    AVG(d.total_customs_value) AS avg_trade_value
FROM declarations d
WHERE d.status = 'CLEARED'
GROUP BY LEFT(d.declarant_id, 9)
HAVING COUNT(*) >= 5  -- Minimum threshold for privacy
ORDER BY total_trade_value DESC
LIMIT 20;
