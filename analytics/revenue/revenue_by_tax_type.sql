-- ============================================================================
-- Revenue by Tax Type Analytics Query
-- Phase 7 - Analytics Implementation
-- Purpose: Breakdown of revenue by tax type (duty, VAT, excise)
-- ============================================================================

SELECT 
    COUNT(*) AS total_declarations,
    SUM(total_customs_duty) AS total_customs_duty,
    SUM(total_vat) AS total_vat,
    SUM(total_excise) AS total_excise,
    SUM(total_tax_liability) AS total_tax_liability,
    AVG(total_customs_duty) AS avg_duty,
    AVG(total_vat) AS avg_vat,
    AVG(total_excise) AS avg_excise,
    AVG(total_tax_liability) AS avg_tax_liability
FROM declarations
WHERE status = 'CLEARED';
