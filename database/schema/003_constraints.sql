-- ============================================================================
-- Phase 4: Database Constraints
-- Project: Customs Revenue and Trade Volume Prediction Analytics Platform
-- Status: SYNTHETIC DATA ONLY - Privacy Clean
-- ============================================================================

-- ============================================================================
-- Foreign Key Constraints
-- ============================================================================

-- Declaration Items to Declaration
ALTER TABLE declaration_items
    ADD CONSTRAINT fk_items_declaration
    FOREIGN KEY (declaration_id) 
    REFERENCES declarations(declaration_id)
    ON DELETE CASCADE;

-- Payments to Declaration
ALTER TABLE payments
    ADD CONSTRAINT fk_payments_declaration
    FOREIGN KEY (declaration_id) 
    REFERENCES declarations(declaration_id)
    ON DELETE CASCADE;

-- Declaration to Port Reference
ALTER TABLE declarations
    ADD CONSTRAINT fk_declaration_port
    FOREIGN KEY (office_code) 
    REFERENCES port_reference(port_code);

-- Declaration Items to HS Code Reference
ALTER TABLE declaration_items
    ADD CONSTRAINT fk_items_hs_code
    FOREIGN KEY (hs_code) 
    REFERENCES hs_code_reference(hs_code);

-- Declaration to Trader Reference
ALTER TABLE declarations
    ADD CONSTRAINT fk_declaration_trader
    FOREIGN KEY (declarant_id) 
    REFERENCES trader_reference(trader_id);

-- ============================================================================
-- Unique Constraints
-- ============================================================================

-- Ensure unique item sequence per declaration
ALTER TABLE declaration_items
    ADD CONSTRAINT uk_declaration_item_sequence
    UNIQUE (declaration_id, item_sequence);

-- Ensure unique payment per declaration
ALTER TABLE payments
    ADD CONSTRAINT uk_payment_declaration
    UNIQUE (declaration_id);

-- ============================================================================
-- Check Constraints (Additional Validation)
-- ============================================================================

-- Declarations: Ensure total amounts are non-negative
ALTER TABLE declarations
    ADD CONSTRAINT chk_total_customs_value CHECK (total_customs_value >= 0),
    ADD CONSTRAINT chk_total_customs_duty CHECK (total_customs_duty >= 0),
    ADD CONSTRAINT chk_total_excise CHECK (total_excise >= 0),
    ADD CONSTRAINT chk_total_vat CHECK (total_vat >= 0),
    ADD CONSTRAINT chk_total_tax_liability CHECK (total_tax_liability >= 0);

-- Declaration Items: Ensure calculated amounts are non-negative
ALTER TABLE declaration_items
    ADD CONSTRAINT chk_customs_value CHECK (customs_value >= 0),
    ADD CONSTRAINT chk_customs_duty CHECK (customs_duty >= 0),
    ADD CONSTRAINT chk_excise_amount CHECK (excise_amount >= 0),
    ADD CONSTRAINT chk_vat_amount CHECK (vat_amount >= 0);

-- Payment: Ensure payment amount matches declaration total
ALTER TABLE payments
    ADD CONSTRAINT chk_payment_date_range CHECK (
        payment_date >= '2024-01-01' AND payment_date <= '2026-12-31'
    );

-- ============================================================================
-- Indexes for Query Performance
-- ============================================================================

-- Declarations composite indexes
CREATE INDEX IF NOT EXISTS idx_decl_date_status 
    ON declarations(declaration_date, status);

CREATE INDEX IF NOT EXISTS idx_decl_trader_date 
    ON declarations(declarant_id, declaration_date);

CREATE INDEX IF NOT EXISTS idx_decl_port_date 
    ON declarations(office_code, declaration_date);

-- Declaration Items composite indexes
CREATE INDEX IF NOT EXISTS idx_item_decl_value 
    ON declaration_items(declaration_id, customs_value);

CREATE INDEX IF NOT EXISTS idx_item_hs_origin 
    ON declaration_items(hs_code, origin_country);

-- Payments: payment date and status
CREATE INDEX IF NOT EXISTS idx_pay_date_status 
    ON payments(payment_date, payment_status);

-- ============================================================================
-- Triggers for Audit Trail (Optional)
-- ============================================================================

-- Update timestamp trigger for declarations
CREATE OR REPLACE FUNCTION update_declaration_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_declaration_update
    BEFORE UPDATE ON declarations
    FOR EACH ROW
    EXECUTE FUNCTION update_declaration_timestamp();

-- ============================================================================
-- Database Security (SYNTHETIC DATA ONLY)
-- ============================================================================

-- Create read-only role for analytics
CREATE ROLE IF NOT EXISTS analytics_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_reader;

-- Create ETL role for data loading
CREATE ROLE IF NOT EXISTS etl_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO etl_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO etl_user;

-- Create admin role
CREATE ROLE IF NOT EXISTS db_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO db_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO db_admin;

-- Revoke public access (demonstration system)
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;

-- ============================================================================
-- End of Constraints
-- ============================================================================