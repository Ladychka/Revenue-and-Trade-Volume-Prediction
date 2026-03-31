-- ============================================================================
-- Phase 4: Core Database Tables
-- Project: Customs Revenue and Trade Volume Prediction Analytics Platform
-- Status: SYNTHETIC DATA ONLY - Privacy Clean
-- ============================================================================

-- 4.1 Declaration Table
-- Purpose: Stores customs import declarations with synthetic identifiers
-- ============================================================================

CREATE TABLE IF NOT EXISTS declarations (
    -- Primary synthetic identifier: DEC-YYYYMMDD-XXXXXXX
    declaration_id VARCHAR(25) PRIMARY KEY,
    
    -- Declaration metadata
    declaration_date DATE NOT NULL,
    declaration_type VARCHAR(20) NOT NULL DEFAULT 'IMPORT',
    status VARCHAR(20) NOT NULL DEFAULT 'LODGED',
    
    -- Synthetic entity references (IMP-XXXXX-XXXXXXX format)
    declarant_id VARCHAR(20) NOT NULL,
    office_code VARCHAR(10) NOT NULL,
    
    -- Financial aggregates (calculated from items)
    total_items INTEGER NOT NULL DEFAULT 0,
    total_customs_value DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    total_customs_duty DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    total_excise DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    total_vat DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    total_tax_liability DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    
    -- Currency (ISO 4217)
    currency_code VARCHAR(3) NOT NULL DEFAULT 'USD',
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_declaration_id_format CHECK (
        declaration_id ~ '^DEC-[0-9]{8}-[0-9]{7}$'
    ),
    CONSTRAINT chk_declarant_id_format CHECK (
        declarant_id ~ '^IMP-[0-9]{5}-[0-9]{7}$'
    ),
    CONSTRAINT chk_port_code_format CHECK (
        office_code ~ '^PORT[0-9]{3}$'
    ),
    CONSTRAINT chk_status_valid CHECK (
        status IN ('LODGED', 'PROCESSED', 'CLEARED', 'REJECTED')
    ),
    CONSTRAINT chk_declaration_type_valid CHECK (
        declaration_type IN ('IMPORT', 'EXPORT', 'TRANSIT')
    ),
    CONSTRAINT chk_date_range CHECK (
        declaration_date >= '2024-01-01' AND declaration_date <= '2025-12-31'
    )
);

-- Indexes for performance
CREATE INDEX idx_declaration_date ON declarations(declaration_date);
CREATE INDEX idx_declaration_status ON declarations(status);
CREATE INDEX idx_declarant_id ON declarations(declarant_id);
CREATE INDEX idx_office_code ON declarations(office_code);
CREATE INDEX idx_origin_country ON declarations(origin_country);

COMMENT ON TABLE declarations IS 'Customs import declarations with synthetic identifiers - NO REAL DATA';

-- 4.2 Declaration Items Table
-- Purpose: Stores individual line items within declarations
-- ============================================================================

CREATE TABLE IF NOT EXISTS declaration_items (
    -- Composite primary key
    item_id VARCHAR(30) PRIMARY KEY,
    declaration_id VARCHAR(25) NOT NULL,
    item_sequence INTEGER NOT NULL,
    
    -- Product classification (valid WCO HS codes - 6 to 10 digits)
    hs_code VARCHAR(10) NOT NULL,
    goods_description VARCHAR(500) NOT NULL,
    origin_country VARCHAR(2) NOT NULL,
    
    -- Quantity details
    quantity DECIMAL(15, 3) NOT NULL,
    quantity_unit VARCHAR(10) NOT NULL,
    statistical_quantity DECIMAL(15, 3),
    
    -- Value and rates
    customs_value DECIMAL(15, 2) NOT NULL,
    duty_rate DECIMAL(8, 4) NOT NULL DEFAULT 0.0000,
    customs_duty DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    
    -- Excise (applicable to specific goods)
    excise_applicable BOOLEAN NOT NULL DEFAULT FALSE,
    excise_type VARCHAR(20),
    excise_rate DECIMAL(8, 4) DEFAULT 0.0000,
    excise_amount DECIMAL(15, 2) DEFAULT 0.00,
    specific_excise_rate DECIMAL(15, 4),
    
    -- VAT
    vat_rate DECIMAL(5, 4) NOT NULL DEFAULT 0.0000,
    vat_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    
    -- Preferential treatment
    preferential_indicator BOOLEAN NOT NULL DEFAULT FALSE,
    preferential_rate DECIMAL(8, 4) DEFAULT 0.0000,
    preferential_country VARCHAR(2),
    
    -- Foreign key
    CONSTRAINT fk_declaration FOREIGN KEY (declaration_id) 
        REFERENCES declarations(declaration_id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT chk_item_id_format CHECK (
        item_id ~ '^[A-Z]{3}-[0-9]{8}-[0-9]{7}-[0-9]{3}$'
    ),
    CONSTRAINT chk_hs_code_valid CHECK (
        hs_code ~ '^[0-9]{6,10}$'
    ),
    CONSTRAINT chk_country_iso CHECK (
        origin_country ~ '^[A-Z]{2}$'
    ),
    CONSTRAINT chk_quantity_positive CHECK (
        quantity > 0
    ),
    CONSTRAINT chk_duty_rate_range CHECK (
        duty_rate >= 0.0000 AND duty_rate <= 1.0000
    ),
    CONSTRAINT chk_vat_rate_range CHECK (
        vat_rate >= 0.0000 AND vat_rate <= 0.2000
    ),
    CONSTRAINT chk_item_sequence CHECK (
        item_sequence >= 1 AND item_sequence <= 100
    ),
    CONSTRAINT chk_excise_type CHECK (
        excise_type IN ('AD_VALOREM', 'SPECIFIC', 'MIXED') OR excise_type IS NULL
    )
);

-- Indexes
CREATE INDEX idx_item_declaration ON declaration_items(declaration_id);
CREATE INDEX idx_item_hs_code ON declaration_items(hs_code);
CREATE INDEX idx_item_origin ON declaration_items(origin_country);
CREATE INDEX idx_item_chapter ON declaration_items(LEFT(hs_code, 2));

COMMENT ON TABLE declaration_items IS 'Declaration line items - SYNTHETIC DATA ONLY';

-- 4.3 Payments Table
-- Purpose: Stores payment records with synthetic identifiers
-- ============================================================================

CREATE TABLE IF NOT EXISTS payments (
    -- Primary synthetic identifier: PMT-YYYYMMDD-XXXXXXXX
    payment_id VARCHAR(25) PRIMARY KEY,
    
    -- Foreign key to declaration
    declaration_id VARCHAR(25) NOT NULL,
    
    -- Payment details
    payment_date DATE NOT NULL,
    payment_amount DECIMAL(15, 2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL DEFAULT 'WIRE',
    currency_code VARCHAR(3) NOT NULL DEFAULT 'USD',
    
    -- Exchange rate for currency conversion
    exchange_rate DECIMAL(12, 6) NOT NULL DEFAULT 1.000000,
    
    -- Payment reference (synthetic)
    bank_reference VARCHAR(30),
    batch_reference VARCHAR(30),
    
    -- Status
    payment_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    
    -- Foreign key
    CONSTRAINT fk_payment_declaration FOREIGN KEY (declaration_id) 
        REFERENCES declarations(declaration_id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT chk_payment_id_format CHECK (
        payment_id ~ '^PMT-[0-9]{8}-[0-9]{8}$'
    ),
    CONSTRAINT chk_payment_method CHECK (
        payment_method IN ('CASH', 'WIRE', 'CARD', 'CHECK')
    ),
    CONSTRAINT chk_payment_status CHECK (
        payment_status IN ('PENDING', 'PROCESSED', 'COMPLETED', 'FAILED', 'REFUNDED')
    ),
    CONSTRAINT chk_exchange_rate_positive CHECK (
        exchange_rate > 0
    ),
    CONSTRAINT chk_payment_amount_positive CHECK (
        payment_amount > 0
    )
);

-- Indexes
CREATE INDEX idx_payment_declaration ON payments(declaration_id);
CREATE INDEX idx_payment_date ON payments(payment_date);
CREATE INDEX idx_payment_status ON payments(payment_status);

COMMENT ON TABLE payments IS 'Payment records - SYNTHETIC DATA ONLY - NO REAL FINANCIAL DATA';

-- 4.4 Exchange Rates Table
-- Purpose: Daily exchange rates for currency conversion
-- ============================================================================

CREATE TABLE IF NOT EXISTS exchange_rates (
    rate_date DATE NOT NULL,
    from_currency VARCHAR(3) NOT NULL,
    to_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    rate_value DECIMAL(12, 6) NOT NULL,
    
    -- Primary key
    PRIMARY KEY (rate_date, from_currency),
    
    -- Constraints
    CONSTRAINT chk_currency_code CHECK (
        from_currency ~ '^[A-Z]{3}$'
    ),
    CONSTRAINT chk_rate_positive CHECK (
        rate_value > 0
    )
);

CREATE INDEX idx_exchange_rate_date ON exchange_rates(rate_date);

COMMENT ON TABLE exchange_rates IS 'Exchange rates - SYNTHETIC DATA ONLY';

-- ============================================================================
-- End of Core Tables
-- ============================================================================