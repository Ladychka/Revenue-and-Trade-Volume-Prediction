# Phase 3 - Logical System Design (Data-Agnostic)

## Purpose
This document defines the logical system design independent of any specific dataset. All entities, relationships, and calculations are defined using the abstract domain concepts from Phase 1 and the synthetic data patterns from Phase 2.

---

## 3.1 Data Model

### 3.1.1 Core Entities

#### Entity: Declaration
**Description:** Abstract representation of a customs declaration as defined in Phase 1 domain glossary.

| Attribute | Type | Constraints | Source |
|-----------|------|-------------|--------|
| declaration_id | VARCHAR(25) | Unique, format: DEC-YYYYMMDD-XXXXXXX | Synthetic ID |
| declaration_date | DATE | Range: 2024-01-01 to 2025-12-31 | Phase 2 |
| declaration_type | VARCHAR(20) | Values: IMPORT, EXPORT, TRANSIT | Domain |
| status | VARCHAR(20) | Values: LODGED, PROCESSED, CLEARED, REJECTED | Domain |
| declarant_id | VARCHAR(20) | Format: IMP-XXXXX-XXXXXXX | Phase 2 |
| office_code | VARCHAR(10) | Format: PORT### | Phase 2 |
| total_items | INTEGER | Min: 1, Max: 100 | Derived |
| total_customs_value | DECIMAL(15,2) | Sum of item values | Derived |
| total_duty | DECIMAL(15,2) | Sum of item duties | Calculated |
| total_vat | DECIMAL(15,2) | Sum of item VAT | Calculated |
| total_excise | DECIMAL(15,2) | Sum of item excise | Calculated |
| total_tax_liability | DECIMAL(15,2) | Total of all taxes | Calculated |
| currency_code | VARCHAR(3) | ISO 4217 | Phase 2 |

**Primary Key:** declaration_id
**Relationships:** One-to-Many with Declaration_Item, One-to-Many with Payment

---

#### Entity: Declaration_Item
**Description:** Abstract representation of a line item within a declaration as defined in Phase 1.

| Attribute | Type | Constraints | Source |
|-----------|------|-------------|--------|
| item_id | VARCHAR(30) | Unique composite key | Synthetic |
| declaration_id | VARCHAR(25) | FK to Declaration | Phase 2 |
| item_sequence | INTEGER | 1-100 per declaration | Synthetic |
| hs_code | VARCHAR(10) | 6-10 digits, valid WCO structure | Phase 2 |
| goods_description | VARCHAR(500) | Text description | Synthetic |
| origin_country | VARCHAR(2) | ISO 3166-1 alpha-2 | Phase 2 |
| quantity | DECIMAL(15,3) | Positive value | Synthetic |
| quantity_unit | VARCHAR(10) | KGM, LTR, PCE | HS-dependent |
| statistical_quantity | DECIMAL(15,3) | For statistical reporting | Synthetic |
| customs_value | DECIMAL(15,2) | Duty base value | Synthetic |
| duty_rate | DECIMAL(8,4) | 0.0000 to 1.0000 | Phase 2 |
| customs_duty | DECIMAL(15,2) | Calculated | Section 3.2 |
| excise_rate | DECIMAL(8,4) | 0.0000 to 1.0000 | Phase 2 |
| excise_amount | DECIMAL(15,2) | Calculated | Section 3.2 |
| vat_rate | DECIMAL(5,4) | 0.0000 to 0.2000 | Phase 2 |
| vat_amount | DECIMAL(15,2) | Calculated | Section 3.2 |
| preferential_indicator | BOOLEAN | TRUE/FALSE | Synthetic |

**Primary Key:** item_id (composite: declaration_id + item_sequence)
**Relationships:** Many-to-One with Declaration

---

#### Entity: Payment
**Description:** Abstract representation of tax payment linked to a declaration.

| Attribute | Type | Constraints | Source |
|-----------|------|-------------|--------|
| payment_id | VARCHAR(25) | Unique, format: PMT-YYYYMMDD-XXXXXXXX | Phase 2 |
| declaration_id | VARCHAR(25) | FK to Declaration | Phase 2 |
| payment_date | DATE | Within 30 days of declaration | Synthetic |
| payment_amount | DECIMAL(15,2) | Equals total_tax_liability | Synthetic |
| payment_method | VARCHAR(20) | Values: CASH, WIRE, CARD | Synthetic |
| currency_code | VARCHAR(3) | ISO 4217 | Phase 2 |
| exchange_rate | DECIMAL(12,6) | To local currency | Phase 2 |

**Primary Key:** payment_id
**Relationships:** Many-to-One with Declaration

---

#### Entity: Exchange_Rate
**Description:** Daily exchange rates for currency conversion.

| Attribute | Type | Constraints | Source |
|-----------|------|-------------|--------|
| rate_date | DATE | Daily, unique | Synthetic |
| from_currency | VARCHAR(3) | ISO 4217 | Phase 2 |
| to_currency | VARCHAR(3) | Fixed: USD | Phase 2 |
| rate_value | DECIMAL(12,6) | Positive value | Synthetic |

**Primary Key:** (rate_date, from_currency)

---

#### Entity: HS_Code_Reference
**Description:** Reference table for HS code tariff rates (data-agnostic skeleton).

| Attribute | Type | Constraints | Source |
|-----------|------|-------------|--------|
| hs_code | VARCHAR(10) | 6-10 digits | Phase 2 |
| chapter | VARCHAR(2) | 01-97 | HS structure |
| heading | VARCHAR(4) | HS-4 level | HS structure |
| description | VARCHAR(500) | Product description | WCO |
| mfn_duty_rate | DECIMAL(8,4) | Standard rate | Public tariff |
| preferential_rates | JSONB | FTA rates | Public |
| excise_applicable | BOOLEAN | Excise eligibility | Domain |
| vat_category | VARCHAR(20) | Rate category | Domain |

**Primary Key:** hs_code

---

#### Entity: Port_Reference
**Description:** Reference table for customs ports (generic codes only).

| Attribute | Type | Constraints | Source |
|-----------|------|-------------|--------|
| port_code | VARCHAR(10) | PORT### format | Phase 2 |
| port_name | VARCHAR(100) | Generic name | Phase 2 |
| port_type | VARCHAR(20) | SEA, AIR, LAND | Synthetic |
| region_code | VARCHAR(10) | Geographic region | Synthetic |

**Primary Key:** port_code

---

### 3.1.2 Entity Relationships

```
┌─────────────────┐       ┌──────────────────┐       ┌─────────────┐
│   Declaration   │──────<│ Declaration_Item │>──────│  HS_Code    │
│                 │       │                  │       │  Reference  │
│ (1)───────(N)   │       │ (N)───────(1)   │       │             │
└─────────────────┘       └──────────────────┘       └─────────────┘
        │                         │
        │ (1)                     │
        ▼                         │
┌─────────────────┐               │
│    Payment      │               │
│                 │               │
│ (N)───────(1)   │               │
└─────────────────┘               │

┌─────────────────┐
│    Exchange     │
│      Rate       │
│                 │
│ (N)───────(1)   │
└─────────────────┘
```

**Relationship Cardinalities:**
- Declaration → Declaration_Item: One-to-Many (1 to N)
- Declaration → Payment: One-to-Many (1 to N, typically 1:1)
- Declaration_Item → HS_Code_Reference: Many-to-One
- Declaration → Port_Reference: Many-to-One

---

### 3.1.3 Key Definitions (Synthetic Only)

**Primary Keys:**
- Declaration: `declaration_id` (synthetic format)
- Declaration_Item: Composite key `(declaration_id, item_sequence)`
- Payment: `payment_id` (synthetic format)
- Exchange_Rate: `(rate_date, from_currency)`

**Foreign Keys:**
- `declaration_item.declaration_id` → `declaration.declaration_id`
- `payment.declaration_id` → `declaration.declaration_id`
- `declaration.office_code` → `port_reference.port_code`
- `declaration_item.hs_code` → `hs_code_reference.hs_code`

**No Sensitive Keys:**
- All primary keys use synthetic identifiers (Phase 2 format)
- No natural keys from real data (SSN, TIN, etc.)
- No reference to actual business entities

---

## 3.2 Revenue Logic

### 3.2.1 Import Duty Calculation

**Formula (from Phase 1 - Section 1.1):**
```
Duty_Amount = Customs_Value × Duty_Rate
```

**Implementation Logic:**
```
IF (Preferential_Indicator = TRUE AND Preferential_Rate_Applicable > 0)
    THEN Duty_Rate = Preferential_Rate
    ELSE Duty_Rate = MFN_Rate
END IF

Duty_Amount = ROUND(Customs_Value × Duty_Rate, 2)
```

**Data-Agnostic Notes:**
- Uses abstract Duty_Rate from HS_Code_Reference
- Applies preferential flag from Declaration_Item
- Rounds to 2 decimal places per Section 3.2.4

---

### 3.2.2 VAT Calculation

**Formula (from Phase 1 - Section 4.1-4.2):**
```
VAT_Base = Customs_Value + Customs_Duty + Excise_Amount + Other_Taxes
VAT_Amount = VAT_Base × VAT_Rate
```

**Implementation Logic:**
```
VAT_Base = Customs_Value + Customs_Duty + Excise_Amount + 0
VAT_Rate = Lookup_VAT_Rate(hs_code, origin_country, preferential_status)
VAT_Amount = ROUND(VAT_Base × VAT_Rate, 2)
```

**Data-Agnostic Notes:**
- VAT_Base includes duty and excise
- VAT_Rate determined by HS code and origin
- Standard rates: 0%, 5%, 7%, 10%, 17%, 20%

---

### 3.2.3 Excise Calculation

**Formula (from Phase 1 - Section 3.1-3.3):**

**Ad Valorem Method:**
```
Excise_Amount = Customs_Value × Excise_Rate
```

**Specific Method:**
```
Excise_Amount = Quantity × Specific_Excise_Rate_Per_Unit
```

**Implementation Logic:**
```
Excise_Applicable = Lookup_Excise_Applicability(hs_code)

IF Excise_Applicable = TRUE
    THEN
        IF Excise_Type = AD_VALOREM
            THEN Excise_Amount = ROUND(Customs_Value × Excise_Rate, 2)
        ELSE IF Excise_Type = SPECIFIC
            THEN Excise_Amount = ROUND(Quantity × Specific_Rate, 2)
        ELSE IF Excise_Type = MIXED
            THEN 
                Excise_AV = Customs_Value × Excise_Rate
                Excise_SP = Quantity × Specific_Rate
                Excise_Amount = MAX(Excise_AV, Excise_SP)
        END IF
    ELSE Excise_Amount = 0
END IF
```

**Data-Agnostic Notes:**
- Excise applies to specific goods only (tobacco, alcohol, fuel)
- Some products use mixed calculation method

---

### 3.2.4 Rounding Rules

**Standard Rounding:**
- All monetary amounts: Round to 2 decimal places
- Exchange rates: Round to 6 decimal places
- Percentages/rates: Store to 4 decimal places (0.0000 to 1.0000)
- Quantities: Round to 3 decimal places

**Rounding Method:**
```
ROUND(value, precision) - Standard mathematical rounding
(0.5 rounds up to 1.00)
```

**Currency Conversion Rounding:**
- Convert foreign currency using exchange rate
- Apply standard rounding to 2 decimal places
- Original precision: 6 decimal places for exchange rate

---

### 3.2.5 Total Tax Liability

**Formula (from Phase 1 - Section 5.1):**
```
Total_Tax_Liability = Customs_Duty + Excise_Amount + VAT_Amount + Other_Charges
```

**Implementation:**
```
Total_Tax = Customs_Duty + Excise_Amount + VAT_Amount + 0
```

---

## 3.3 Trade Logic

### 3.3.1 Trade Value Calculation

**Aggregate Value:**
```
Total_Trade_Value = SUM(Declarations.customs_value) 
                   WHERE Declaration.status = 'CLEARED'
```

**By Dimension Aggregations:**
- By Country: `SUM(customs_value) GROUP BY origin_country`
- By HS Chapter: `SUM(customs_value) GROUP BY hs_code.chapter`
- By Port: `SUM(customs_value) GROUP BY office_code`
- By Month: `SUM(customs_value) GROUP BY YEAR(declaration_date), MONTH(declaration_date)`

---

### 3.3.2 Volume Metrics

**Item Count:**
```
Total_Items = COUNT(Declaration_Item) 
             WHERE Declaration.status = 'CLEARED'
```

**Quantity Metrics:**
```
Total_Quantity = SUM(quantity) 
                GROUP BY quantity_unit, hs_code
                (normalize to standard unit per chapter)
```

**Declaration Count:**
```
Total_Declarations = COUNT(DISTINCT declaration_id)
                    WHERE Declaration.status = 'CLEARED'
```

---

### 3.3.3 Aggregation Levels

**Temporal Aggregations:**
| Level | Grouping | Use Case |
|-------|----------|----------|
| Daily | declaration_date | Operational reports |
| Weekly | YEARWEEK(declaration_date) | Short-term trends |
| Monthly | YEAR(declaration_date), MONTH(declaration_date) | Monthly statistics |
| Quarterly | QUARTER(declaration_date) | Quarterly review |
| Annual | YEAR(declaration_date) | Annual reports |

**Geographic Aggregations:**
| Level | Grouping | Use Case |
|-------|----------|----------|
| Country | origin_country | Trade partner analysis |
| Region | origin_country (grouped) | Regional trade patterns |
| Port | office_code | Port performance |
| Port Region | port_reference.region_code | Regional customs operations |

**Product Aggregations:**
| Level | Grouping | Use Case |
|-------|----------|----------|
| HS-2 (Chapter) | hs_code[1:2] | High-level sector analysis |
| HS-4 (Heading) | hs_code[1:4] | Product category analysis |
| HS-6 (Subheading) | hs_code[1:6] | Detailed product analysis |
| HS-10 (Tariff Line) | hs_code (full) | Granular product analysis |

---

### 3.3.4 Trade Statistics Calculations

**Average Declaration Value:**
```
Avg_Declaration_Value = Total_Trade_Value / Total_Declarations
```

**Duty Collection Rate:**
```
Duty_Collection_Rate = (SUM(Customs_Duty) / SUM(Customs_Value)) × 100
```

**Clearance Rate:**
```
Clearance_Rate = (COUNT(status = 'CLEARED') / COUNT(status = 'CLEARED' + 'REJECTED')) × 100
```

**Top Importers:**
```
TOP_N_Importers = SELECT declarant_id, SUM(customs_value) as total_value
                  FROM Declaration
                  GROUP BY declarant_id
                  ORDER BY total_value DESC
                  LIMIT N
```

---

## 3.4 Review

### 3.4.1 Sensitive Attribute Check

**Attributes Reviewed:**
| Entity | Attribute | Sensitive? | Justification |
|--------|-----------|------------|---------------|
| Declaration | declaration_id | No | Synthetic format only |
| Declaration | declarant_id | No | Synthetic format only (IMP-*) |
| Declaration_Item | goods_description | No | Generic product descriptions |
| Declaration_Item | origin_country | No | ISO codes only |
| Payment | payment_id | No | Synthetic format only |
| Payment | payment_amount | No | Synthetic amounts |

**Result:** No sensitive attributes exist in the logical model.

---

### 3.4.2 Data-Agnostic Confirmation

- ✅ All identifiers use Phase 2 synthetic patterns
- ✅ No natural person identifiers (SSN, passport, etc.)
- ✅ No real business identifiers (actual TIN, registration numbers)
- ✅ No geographic precision beyond generic port codes
- ✅ All keys are synthetic and non-correlating

---

### 3.4.3 Logical Design Freeze

**Design Status:** FROZEN

This logical system design is data-agnostic and ready for implementation. The design:
- Uses abstract entities from Phase 1 domain glossary
- Applies synthetic identifiers from Phase 2 data design
- Implements calculations from Phase 1 formulas
- Contains no sensitive attributes

**Implementation may proceed to database creation phase.**

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2026-03-31 | Initial release - Phase 3 Logical System Design |

---

**Status:** FROZEN - Ready for database implementation

**Verification:**
- ✅ Core entities identified (Declaration, Declaration_Item, Payment, Exchange_Rate, References)
- ✅ Relationships defined (1:N, N:1, N:N via junction)
- ✅ Keys defined using synthetic identifiers
- ✅ Revenue logic implemented (duty, VAT, excise formulas)
- ✅ Trade logic defined (value, volume, aggregations)
- ✅ No sensitive attributes confirmed
- ✅ Logical design frozen