# Phase 2 - Synthetic Data Design Specification

## Purpose
This document defines the design rules for synthetic data generation. All identifiers, fields, and values must be demonstrably fake while maintaining structural realism. This ensures the demonstration system remains clearly distinguishable from any real production data.

---

## 2.1 Identifier Design

### 2.1.1 Declaration ID Format

**Format Pattern:**
```
DEC-[YYYYMMDD]-[XXXXXXX]
```
Where:
- `DEC-` = Fixed prefix (Declaration)
- `[YYYYMMDD]` = Date of declaration (8 digits)
- `[XXXXXXX]` = Random 7-digit sequence (0000001-9999999)

**Examples:**
- `DEC-20260331-0001234`
- `DEC-20260115-0087542`
- `DEC-20251220-0010000`

**Validation Rules:**
- Must be unique per declaration
- Date must be within valid range (2024-01-01 to 2026-12-31)
- Sequence number must not start with zeros only

---

### 2.1.2 Importer/T trader ID Format

**Format Pattern:**
```
IMP-[XXXXX]-[XXXXXXX]
```
Where:
- `IMP-` = Fixed prefix (Importer)
- `[XXXXX]` = 5-digit region code (random)
- `[XXXXXXX]` = 7-digit entity sequence (random)

**Examples:**
- `IMP-12345-0000001` (Entity 1 in region 12345)
- `IMP-98765-0000250` (Entity 250 in region 98765)
- `IMP-55555-0005000` (Entity 5000 in region 55555)

**Validation Rules:**
- Region codes must fall within 10000-99999
- Entity sequence within 0000001-0009999
- No correlation between entity numbers and actual company data

---

### 2.1.3 Payment Reference Format

**Format Pattern:**
```
PMT-[YYYYMMDD]-[XXXXXXXX]
```
Where:
- `PMT-` = Fixed prefix (Payment)
- `[YYYYMMDD]` = Payment date (8 digits)
- `[XXXXXXXX]` = 8-digit random reference

**Examples:**
- `PMT-20260331-12345678`
- `PMT-20260115-87654321`
- `PMT-20251220-00000001`

**Validation Rules:**
- Must be unique per payment
- Date must correspond to declaration date or within 7 days after

---

## 2.2 Field Design

### 2.2.1 HS Code Format

**Structure:** Real HS code format (6-10 digits) from valid WCO structure

**Valid Ranges:**
- Chapters 01-97 (all WCO chapters)
- Must follow valid HS hierarchy (e.g., 84.13 is valid, 84.99 is valid)
- National tariff extensions allowed (8-10 digits)

**Examples of Valid HS Codes:**
- `8471300000` - Portable digital automatic data processing machines
- `8517120000` - Telephones for cellular networks
- `6204620000` - Women's trousers of cotton
- `3002150000` - Immunological products, unmixed
- `8703235010` - Motor vehicles with engine >1500cc but <=3000cc

**Validation Rules:**
- Must be a valid HS code structure
- Must not reference real transaction data
- Must be from published WCO tariff schedules (public knowledge)

---

### 2.2.2 Country Codes (ISO 3166-1)

**Format:** 2-character alpha-2 codes (ISO standard)

**Allowed Countries:**
```
AU, BD, BR, CA, CN, DE, FR, GB, ID, IN, IT, JP, KR, MY, NL, PH, SG, TH, TW, US, VN
```

**Distribution Weighting:**
- CN (China): 35%
- JP (Japan): 15%
- US (United States): 12%
- KR (South Korea): 10%
- TH (Thailand): 8%
- ID (Indonesia): 5%
- MY (Malaysia): 5%
- Other: 10%

**Validation Rules:**
- Must be valid ISO 3166-1 alpha-2 codes
- Must not reference real trading partner relationships

---

### 2.2.3 Port Codes

**Format:** 4-character alphanumeric codes (generic, non-real)

**Generic Port Codes:**
```
PORT001 - Port Alpha
PORT002 - Port Beta  
PORT003 - Port Gamma
PORT004 - Port Delta
PORT005 - Port Epsilon
PORT006 - Port Zeta
PORT007 - Port Eta
PORT008 - Port Theta
PORT009 - Port Iota
PORT010 - Port Kappa
```

**Validation Rules:**
- Must be valid format (PORT + 3-digit)
- Must not correspond to actual port identifiers in any country

---

### 2.2.4 Currency Codes

**Format:** 3-character ISO 4217 codes

**Allowed Currencies:**
```
USD - US Dollar
EUR - Euro
JPY - Japanese Yen
CNY - Chinese Yuan
GBP - British Pound
THB - Thai Baht
KRW - South Korean Won
SGD - Singapore Dollar
MYR - Malaysian Ringgit
IDR - Indonesian Rupiah
```

**Validation Rules:**
- Must be valid ISO 4217 codes
- Exchange rates must be synthetic but within realistic ranges

---

## 2.3 Data Rules

### 2.3.1 Value Ranges

#### Customs Value (per item)
| Metric | Range (USD) |
|--------|-------------|
| Minimum | 100.00 |
| Maximum | 5,000,000.00 |
| Median | 15,000.00 |
| Mean | 75,000.00 |

**Distribution:** Log-normal distribution (80% of values between 500 and 100,000)

#### Quantity (per item)
| Metric | Range |
|--------|-------|
| Minimum | 1 unit |
| Maximum | 100,000 units |
| Unit Type | Kilograms, Liters, Pieces |

**Distribution:** Pareto distribution (most items have low quantity)

#### Duty Rate
| Category | Range |
|----------|-------|
| MFN Rate | 0% - 30% |
| Preferential Rate | 0% - 15% |
| Most Common | 5% - 10% |

#### Tax Rates
| Tax Type | Standard Rate |
|----------|---------------|
| Customs Duty | 0% - 30% (varies by HS) |
| Excise | 0% - 100% (specific goods only) |
| VAT | 0%, 5%, 7%, 10%, 17%, 20% |

---

### 2.3.2 Record Volume Specifications

| Dataset | Target Rows | Description |
|---------|-------------|-------------|
| Declarations | 50,000 | Unique import declarations over 24 months |
| Declaration Items | 150,000 | Average 3 items per declaration |
| Payments | 50,000 | One payment per declaration |
| Exchange Rates | 730 | Daily rates for 24 months |

**Temporal Distribution:**
- 24-month range: 2024-01-01 to 2025-12-31
- Monthly declarations: ~2,000-2,500
- Daily declarations: ~65-85

---

### 2.3.3 Data Distribution Rules

#### By HS Chapter (Weighted)
```
84-85 (Machinery/Electronics): 25%
94-96 (Misc Manufactured): 15%
62-63 (Textiles): 12%
87 (Vehicles): 10%
90-92 (Precision Instruments): 8%
Other Chapters: 30%
```

#### By Port (Weighted)
```
PORT001: 20%
PORT002: 18%
PORT003: 15%
PORT004: 12%
PORT005-PORT010: 35%
```

#### By Tax Type Distribution
```
Duty-only declarations: 40%
Duty + VAT declarations: 50%
Duty + Excise + VAT: 10%
```

---

### 2.3.4 Synthetic Value Generation Rules

**Random Value Generation:**
- Use cryptographically secure random number generation
- Seeds must be project-specific (not tied to any real data)
- No correlation between fields that would exist in real data

**Temporal Consistency:**
- Exchange rates change daily (within realistic bands)
- Declarations follow business day patterns (weekdays only for submission)
- Payment dates align with declaration clearance

**Cross-Field Consistency:**
- Customs value aligns with HS code value patterns
- Quantity units align with HS code (e.g., chapters 28-38 use weight)
- Tax calculations follow Phase 1 formulas with synthetic inputs

---

## 2.4 Validation Requirements

### 2.4.1 Identifier Validation

| Check | Criteria | Action |
|-------|----------|--------|
| Unique Declaration IDs | No duplicates | Fail if duplicate found |
| Valid ID Format | Matches DEC-YYYYMMDD-XXXXXXX | Fail if format invalid |
| Valid Importer Format | Matches IMP-XXXXX-XXXXXXX | Fail if format invalid |
| Valid Payment Format | Matches PMT-YYYYMMDD-XXXXXXXX | Fail if format invalid |

---

### 2.4.2 Content Validation

| Check | Criteria | Action |
|-------|----------|--------|
| No Real Names | No personal names in any field | Fail if found |
| No Real Company Names | No actual company identifiers | Fail if found |
| No Real Addresses | No real address data | Fail if found |
| No Real Financial Data | No actual account numbers | Fail if found |
| No PII Patterns | No patterns matching PII (SSN, etc.) | Fail if found |

---

### 2.4.3 Format Validation

| Check | Criteria | Action |
|-------|----------|--------|
| HS Code Validity | Valid WCO structure | Warn if structure invalid |
| Country Code Validity | Valid ISO 3166-1 | Fail if invalid |
| Port Code Validity | Matches PORT### format | Fail if invalid |
| Currency Code Validity | Valid ISO 4217 | Fail if invalid |
| Date Validity | Within valid range | Fail if out of range |

---

### 2.4.4 Consistency Validation

| Check | Criteria | Action |
|-------|----------|--------|
| Tax Calculation | Must follow Phase 1 formulas | Fail if mismatch |
| Value Consistency | Customs value × duty rate = duty | Warn if significant variance |
| Quantity Units | Must align with HS chapter | Warn if mismatch |
| Payment Alignment | Payment date <= declaration date + 30 | Warn if outside range |

---

## 2.5 Data Generation Guidelines

### 2.5.1 Generator Requirements

**Pseudorandom Number Generator:**
- Use Python's `secrets` module or similar cryptographic RNG
- Each generation run uses unique seed
- No reproducibility required (but seed must be documented)

**Character Sets:**
- Identifiers: Alphanumeric only (uppercase for letters)
- Text fields: ASCII printable characters only
- No Unicode characters beyond basic Latin

### 2.5.2 Data Quality Checks

**Pre-Generation:**
- Validate all format specifications
- Confirm no references to real data sources

**Post-Generation:**
- Run all validation checks (Section 2.4)
- Verify statistical distributions match specifications
- Confirm no data anomalies (negative values, impossible dates)

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2026-03-31 | Initial release - Phase 2 Synthetic Data Design |

---

**Status:** APPROVED - Ready for implementation

**Validation Confirmation:**
- ✅ Fake identifiers defined (declaration ID, importer ID, payment references)
- ✅ Real HS format (WCO structure, no real transactions)
- ✅ ISO country codes (standard codes only)
- ✅ Generic port codes (no real port identifiers)
- ✅ Value ranges defined (min/max, distribution parameters)
- ✅ Record volume specified (50K declarations, 150K items)
- ✅ No real names included in design
- ✅ No real identifiers in design
- ✅ No production values in design