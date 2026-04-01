# Data Dictionary - Phase 1
# This document describes the key data elements in the system.

---

## Core Tables

### declarations
| Column | Type | Description |
|--------|------|-------------|
| declaration_id | VARCHAR(25) | Synthetic ID: DEC-YYYYMMDD-XXXXXXX |
| declaration_date | DATE | Date of declaration |
| status | VARCHAR(20) | LODGED, PROCESSED, CLEARED, REJECTED |
| declarant_id | VARCHAR(20) | Synthetic importer ID |
| office_code | VARCHAR(10) | Customs port code |
| total_customs_value | DECIMAL(15,2) | Total customs value |
| total_customs_duty | DECIMAL(15,2) | Total duty |
| total_vat | DECIMAL(15,2) | Total VAT |
| total_tax_liability | DECIMAL(15,2) | Total taxes |

### declaration_items
| Column | Type | Description |
|--------|------|-------------|
| item_id | VARCHAR(30) | Synthetic item ID |
| hs_code | VARCHAR(10) | HS classification (6-10 digits) |
| customs_value | DECIMAL(15,2) | Item value |
| duty_rate | DECIMAL(8,4) | Duty rate |
| vat_rate | DECIMAL(5,4) | VAT rate |

### payments
| Column | Type | Description |
|--------|------|-------------|
| payment_id | VARCHAR(25) | Synthetic payment ID |
| declaration_id | VARCHAR(25) | Reference to declaration |
| payment_amount | DECIMAL(15,2) | Payment in KHR |

---

## Reference Tables

### hs_code_reference
HS code with tariff rates.

### port_reference
Customs ports.

### country_reference
ISO country codes.

### currency_reference
ISO currency codes.
