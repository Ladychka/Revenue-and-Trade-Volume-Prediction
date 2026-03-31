-- ============================================================================
-- Phase 4: Reference Tables
-- Project: Customs Revenue and Trade Volume Prediction Analytics Platform
-- Status: SYNTHETIC DATA ONLY - Privacy Clean
-- ============================================================================

-- 4.5 HS Code Reference Table
-- Purpose: Reference table for HS code tariff rates (synthetic skeleton)
-- ============================================================================

CREATE TABLE IF NOT EXISTS hs_code_reference (
    hs_code VARCHAR(10) PRIMARY KEY,
    chapter VARCHAR(2) NOT NULL,
    heading VARCHAR(4) NOT NULL,
    subheading VARCHAR(6),
    description VARCHAR(500) NOT NULL,
    
    -- Duty rates (from public WCO tariff schedules)
    mfn_duty_rate DECIMAL(8, 4) NOT NULL DEFAULT 0.0000,
    preferential_rate DECIMAL(8, 4),
    
    -- Excise applicability
    excise_applicable BOOLEAN NOT NULL DEFAULT FALSE,
    excise_type VARCHAR(20),
    excise_rate DECIMAL(8, 4),
    specific_excise_rate DECIMAL(15, 4),
    
    -- VAT category
    vat_category VARCHAR(20) NOT NULL DEFAULT 'STANDARD',
    vat_rate DECIMAL(5, 4) NOT NULL DEFAULT 0.1700,
    
    -- Unit of quantity
    unit_of_quantity VARCHAR(10),
    
    -- Constraints
    CONSTRAINT chk_hs_code_format CHECK (
        hs_code ~ '^[0-9]{6,10}$'
    ),
    CONSTRAINT chk_chapter_range CHECK (
        chapter::INTEGER >= 1 AND chapter::INTEGER <= 97
    ),
    CONSTRAINT chk_duty_rate CHECK (
        mfn_duty_rate >= 0.0000 AND mfn_duty_rate <= 1.0000
    ),
    CONSTRAINT chk_vat_rate CHECK (
        vat_rate >= 0.0000 AND vat_rate <= 0.2500
    ),
    CONSTRAINT chk_vat_category CHECK (
        vat_category IN ('STANDARD', 'REDUCED', 'ZERO', 'EXEMPT')
    )
);

CREATE INDEX idx_hs_chapter ON hs_code_reference(chapter);
CREATE INDEX idx_hs_heading ON hs_code_reference(heading);

COMMENT ON TABLE hs_code_reference IS 
    'HS code reference - SYNTHETIC STRUCTURE - Rates from public tariff schedules';

-- 4.6 Port Reference Table
-- Purpose: Reference table for customs ports (generic codes only)
-- ============================================================================

CREATE TABLE IF NOT EXISTS port_reference (
    port_code VARCHAR(10) PRIMARY KEY,
    port_name VARCHAR(100) NOT NULL,
    port_type VARCHAR(20) NOT NULL,
    region_code VARCHAR(10) NOT NULL,
    country_code VARCHAR(2) NOT NULL DEFAULT 'XX',
    
    -- Status
    active BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Constraints
    CONSTRAINT chk_port_code_format CHECK (
        port_code ~ '^PORT[0-9]{3}$'
    ),
    CONSTRAINT chk_port_type CHECK (
        port_type IN ('SEA', 'AIR', 'LAND', 'RAIL', 'POST')
    ),
    CONSTRAINT chk_country_code CHECK (
        country_code ~ '^[A-Z]{2}$'
    )
);

COMMENT ON TABLE port_reference IS 
    'Port reference - GENERIC CODES ONLY - No real port identifiers';

-- 4.7 Country Reference Table
-- Purpose: ISO country codes for origin/destination
-- ============================================================================

CREATE TABLE IF NOT EXISTS country_reference (
    country_code VARCHAR(2) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    iso_alpha_3 VARCHAR(3),
    region VARCHAR(50),
    
    -- Trade agreement membership
    wto_member BOOLEAN NOT NULL DEFAULT TRUE,
    preferential_codes VARCHAR(50),
    
    -- Constraints
    CONSTRAINT chk_country_code_iso CHECK (
        country_code ~ '^[A-Z]{2}$'
    )
);

CREATE INDEX idx_country_region ON country_reference(region);

COMMENT ON TABLE country_reference IS 
    'Country reference - ISO CODES ONLY - No real trade data';

-- 4.8 Currency Reference Table
-- Purpose: ISO currency codes for valuation
-- ============================================================================

CREATE TABLE IF NOT EXISTS currency_reference (
    currency_code VARCHAR(3) PRIMARY KEY,
    currency_name VARCHAR(100) NOT NULL,
    currency_symbol VARCHAR(5),
    decimal_places INTEGER NOT NULL DEFAULT 2,
    
    -- Constraints
    CONSTRAINT chk_currency_code CHECK (
        currency_code ~ '^[A-Z]{3}$'
    ),
    CONSTRAINT chk_decimal_places CHECK (
        decimal_places >= 0 AND decimal_places <= 4
    )
);

COMMENT ON TABLE currency_reference IS 
    'Currency reference - ISO 4217 CODES - No real exchange rate data';

-- 4.9 Importer/T exporter Reference Table
-- Purpose: Synthetic trader entities
-- ============================================================================

CREATE TABLE IF NOT EXISTS trader_reference (
    trader_id VARCHAR(20) PRIMARY KEY,
    trader_type VARCHAR(20) NOT NULL DEFAULT 'IMPORTER',
    region_code VARCHAR(10) NOT NULL,
    
    -- No real company names - generic identifiers only
    entity_code VARCHAR(10),
    
    -- Registration (synthetic format)
    registration_number VARCHAR(30),
    registration_country VARCHAR(2),
    
    -- Status
    active BOOLEAN NOT NULL DEFAULT TRUE,
    risk_category VARCHAR(20) DEFAULT 'STANDARD',
    
    -- Constraints
    CONSTRAINT chk_trader_id_format CHECK (
        trader_id ~ '^IMP-[0-9]{5}-[0-9]{7}$'
    ),
    CONSTRAINT chk_trader_type CHECK (
        trader_type IN ('IMPORTER', 'EXPORTER', 'BOTH')
    ),
    CONSTRAINT chk_risk_category CHECK (
        risk_category IN ('LOW', 'STANDARD', 'ELEVATED', 'HIGH')
    )
);

CREATE INDEX idx_trader_region ON trader_reference(region_code);
CREATE INDEX idx_trader_type ON trader_reference(trader_type);

COMMENT ON TABLE trader_reference IS 
    'Trader reference - SYNTHETIC ENTITIES ONLY - No real company data';

-- ============================================================================
-- End of Reference Tables
-- ============================================================================