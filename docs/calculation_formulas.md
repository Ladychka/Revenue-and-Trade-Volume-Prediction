# Calculation Formulas - Tax Assessment Definitions

## Purpose
This document defines the tax calculation logic as established under customs law frameworks. Formulas are presented as abstract mathematical definitions without reference to actual operational data or numerical examples.

---

## 1. Customs Duty Calculation

### 1.1 Ad Valorem Duty

**Definition:** Customs duty calculated as a percentage of the customs value.

**Formula:**
```
Duty_AdValorem = Customs_Value × Duty_Rate_Percentage
```

**Parameters:**
| Parameter | Description | Source |
|-----------|-------------|--------|
| Customs_Value | Value of goods for duty assessment | Customs Valuation Rules |
| Duty_Rate_Percentage | Applicable duty rate from tariff schedule | Tariff Classification |

**Legal Basis:** National tariff schedule, WTO valuation agreement

---

### 1.2 Specific Duty

**Definition:** Customs duty calculated as a fixed amount per unit of measurement.

**Formula:**
```
Duty_Specific = Quantity × Specific_Rate_PerUnit
```

**Parameters:**
| Parameter | Description | Source |
|-----------|-------------|--------|
| Quantity | Physical quantity (mass, volume, pieces) | Declaration |
| Specific_Rate_PerUnit | Fixed rate per unit from tariff | Tariff Classification |

**Legal Basis:** National tariff schedule provisions for specific goods

---

### 1.3 Compound Duty

**Definition:** Combination of ad valorem and specific duties applied concurrently.

**Formula:**
```
Duty_Compound = (Customs_Value × Duty_Rate_Percentage) + (Quantity × Specific_Rate_PerUnit)
```

**Legal Basis:** National tariff schedule for goods subject to both calculation methods

---

### 1.4 Preferential Duty

**Definition:** Reduced duty rate applied to goods qualifying under preferential origin agreements.

**Formula:**
```
Duty_Preferential = Customs_Value × Preferential_Rate
```
Where:
- Preferential_Rate < Most-Favored-Nation (MFN) Rate
- Eligibility subject to proof of origin

**Legal Basis:** Free trade agreements, preferential tariff arrangements

---

## 2. Customs Value Determination

### 2.1 Transaction Value (Primary Method)

**Definition:** The price actually paid or payable for goods, adjusted for specified elements.

**Formula:**
```
Customs_Value = Transaction_Value + Adjustments
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Transaction_Value | Price paid or payable for goods |
| Adjustments | Added costs (freight, insurance, royalties, packing) |

**Components of Adjustments:**
- Cost of transport to border (freight)
- Insurance charges
- Royalties and license fees
- Proceeds of subsequent resale (if applicable)
- Direct and indirect payments by buyer

**Legal Basis:** WTO Customs Valuation Agreement, Article 1

---

### 2.2 Deductive Value Method

**Definition:** Value determined from the unit price at which imported goods are sold in the importing country.

**Formula:**
```
Customs_Value = Sale_Price - Deductions
```

**Deductions:**
- Profits and general expenses
- Transport and insurance within importing country
- Customs duties and taxes paid
- Commissions (if included)

**Legal Basis:** WTO Customs Valuation Agreement, Article 5

---

## 3. Excise Duty Calculation

### 3.1 Ad Valorem Excise

**Definition:** Excise duty calculated as a percentage of the customs value or transaction value.

**Formula:**
```
Excise_AdValorem = Tax_Base × Excise_Rate_Percentage
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Tax_Base | Customs value or specified value basis |
| Excise_Rate_Percentage | Rate from excise tax schedule |

**Legal Basis:** National excise taxation act

---

### 3.2 Specific Excise

**Definition:** Excise duty calculated per unit quantity (volume, weight, or measurement).

**Formula:**
```
Excise_Specific = Quantity × Specific_Excise_Rate
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Quantity | Volume (liters), weight (kg), or units |
| Specific_Excise_Rate | Fixed rate per unit from excise schedule |

**Legal Basis:** Specific goods excise regulations

---

### 3.3 Mixed Excise System

**Definition:** Excise calculated using both ad valorem and specific methods, where the higher amount applies.

**Formula:**
```
Excise = MAX(Excise_AdValorem, Excise_Specific)
```

**Legal Basis:** Complex excise structures for certain product categories

---

## 4. Value-Added Tax (VAT) Calculation

### 4.1 Import VAT Base

**Definition:** The value upon which VAT is calculated for imported goods.

**Formula:**
```
VAT_Base = Customs_Value + Customs_Duty + Excise_Duty + Other_Applicable_Taxes
```

**Components:**
| Component | Description |
|-----------|-------------|
| Customs_Value | Duty-paid value of goods |
| Customs_Duty | Import duty amount |
| Excise_Duty | Excise duty (if applicable) |
| Other_Applicable_Taxes | Additional taxes (e.g., surcharges) |

**Legal Basis:** VAT legislation provisions for imports

---

### 4.2 VAT Amount

**Definition:** The calculated VAT liability on imported goods.

**Formula:**
```
VAT_Amount = VAT_Base × VAT_Rate
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| VAT_Base | Aggregated value including duties |
| VAT_Rate | Applicable VAT rate (standard, reduced, zero) |

**Standard Rates:**
- Standard rate: Typically 17-20%
- Reduced rate: Typically 5-10%
- Zero rate: Exempt supplies

**Legal Basis:** VAT Act provisions for taxable imports

---

### 4.3 VAT Exemption Threshold

**Definition:** Value below which imported goods may be exempt from VAT.

**Formula:**
```
VAT_Exemption = IF(Customs_Value < Threshold, 0, VAT_Amount)
```

**Legal Basis:** VAT Act exemption provisions

---

## 5. Total Tax Liability

### 5.1 Aggregate Tax Calculation

**Definition:** Sum of all taxes and duties payable upon importation.

**Formula:**
```
Total_Tax_Liability = Customs_Duty + Excise_Duty + VAT_Amount + Other_Charges
```

**Components:**
| Component | Calculation Method |
|-----------|-------------------|
| Customs_Duty | Per Section 1 formulas |
| Excise_Duty | Per Section 3 formulas |
| VAT_Amount | Per Section 4.2 formula |
| Other_Charges | Anti-dumping, countervailing, surcharges |

**Legal Basis:** Consolidated customs revenue collection provisions

---

### 5.2 Tax Payment Calculation

**Definition:** Amount payable to customs authorities.

**Formula:**
```
Tax_Payable = Total_Tax_Liability - Prepaid_Amount - Allowable_Deductions
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Total_Tax_Liability | Aggregate tax calculated |
| Prepaid_Amount | Advances or deposits |
| Allowable_Deductions |drawbacks, exemptions |

**Legal Basis:** Customs revenue collection regulations

---

## 6. Rounding Rules

### 6.1 Tax Amount Rounding

**Definition:** Standard rounding methodology for calculated tax amounts.

**Formula:**
```
Tax_Rounded = ROUND(Tax_Amount, Decimal_Places)
```

**Common Rules:**
- To nearest whole currency unit, OR
- To two decimal places

**Legal Basis:** Currency rounding regulations, customs procedures

---

## 7. Exchange Rate Application

### 7.1 Currency Conversion

**Definition:** Conversion of foreign currency values to local currency for duty assessment.

**Formula:**
```
Local_Customs_Value = Foreign_Value × Exchange_Rate
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Foreign_Value | Declared value in foreign currency |
| Exchange_Rate | Official rate (customs, interbank, or prescribed) |

**Rate Types:**
- Daily rate (published by central bank)
- Monthly average rate
- Rate on date of declaration

**Legal Basis:** Customs valuation regulations on currency conversion

---

## 8. Tax Rate Determination Logic

### 8.1 HS Code-Based Rate Lookup

**Definition:** Process of determining applicable rates based on goods classification.

```
Rate_Determination(HS_Code, Origin, Preferential_Status) → {Duty_Rate, Excise_Rate, VAT_Rate}
```

**Decision Logic:**
1. Extract applicable chapter/heading from HS code
2. Check for preferential origin certificates
3. Apply relevant FTA rate if eligible, else MFN rate
4. Determine excise applicability based on product type
5. Select VAT rate based on goods category

**Legal Basis:** Tariff classification regulations, preferential trade agreements

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2026-03-31 | Initial release - Phase 1 calculation definitions |

---

**Status:** DRAFT - Abstract definitions derived from legal frameworks

---

## PHASE 14: REVENUE LOGIC WHITEPAPER - VALIDATION EXAMPLES

This section provides synthetic numerical illustrations to validate the revenue 
calculation logic. All values are artificial and for demonstration only.

---

### 14.1 Legal Basis Mapping

| Tax Type | Legal Basis | Implementation |
|----------|-------------|----------------|
| Import Duty | WTO Valuation Agreement, National Tariff Schedule | [`core/revenue/duty_calculator.py`](core/revenue/duty_calculator.py) |
| VAT | National VAT Act | [`core/revenue/vat_calculator.py`](core/revenue/vat_calculator.py) |
| Excise | National Excise Taxation Act | [`core/revenue/excise_calculator.py`](core/revenue/excise_calculator.py) |

---

### 14.2 Synthetic Validation Examples

#### Example A: Standard Import (Ad Valorem)

**Input (Synthetic):**
- Customs Value: 10,000.00 KHR
- HS Code: 8471300000 (Data Processing Machines)
- Duty Rate (MFN): 0.00%
- VAT Rate: 17%

**Calculation:**
```
Step 1: Customs Duty = 10,000.00 × 0.00 = 0.00 KHR
Step 2: VAT Base = 10,000.00 + 0.00 = 10,000.00 KHR
Step 3: VAT = 10,000.00 × 0.17 = 1,700.00 KHR
Step 4: Total Tax = 0.00 + 1,700.00 = 1,700.00 KHR
```

**Output (Synthetic):**
- Customs Duty: 0.00 KHR
- VAT: 1,700.00 KHR
- Total Tax Liability: 1,700.00 KHR

---

#### Example B: Preferential Treatment

**Input (Synthetic):**
- Customs Value: 50,000.00 KHR
- HS Code: 8703235010 (Motor Vehicles)
- MFN Rate: 25%
- Preferential Rate: 12.5% (RCEP eligible)

**Calculation:**
```
Step 1: Check preferential eligibility = TRUE
Step 2: Apply preferential rate (lower than MFN)
Step 3: Customs Duty = 50,000.00 × 0.125 = 6,250.00 KHR
Step 4: VAT Base = 50,000.00 + 6,250.00 = 56,250.00 KHR
Step 5: VAT = 56,250.00 × 0.17 = 9,562.50 KHR
Step 6: Total Tax = 6,250.00 + 9,562.50 = 15,812.50 KHR
```

**Output (Synthetic):**
- Customs Duty: 6,250.00 KHR
- VAT: 9,562.50 KHR
- Total Tax Liability: 15,812.50 KHR

---

#### Example C: Textile Import with Preferential

**Input (Synthetic):**
- Customs Value: 25,000.00 KHR
- HS Code: 6204620000 (Women's Trousers)
- MFN Rate: 16.75%
- Preferential Rate (ASEAN): 8.375%
- VAT Rate: 7%

**Calculation:**
```
Step 1: Check preferential eligibility = TRUE (ASEAN origin)
Step 2: Apply preferential rate
Step 3: Customs Duty = 25,000.00 × 0.08375 = 2,093.75 KHR
Step 4: VAT Base = 25,000.00 + 2,093.75 = 27,093.75 KHR
Step 5: VAT = 27,093.75 × 0.07 = 1,896.56 KHR
Step 6: Total Tax = 2,093.75 + 1,896.56 = 3,990.31 KHR
```

**Output (Synthetic):**
- Customs Duty: 2,093.75 KHR
- VAT: 1,896.56 KHR
- Total Tax Liability: 3,990.31 KHR

---

### 14.3 Rounding Rules

| Tax Type | Rounding Rule |
|----------|---------------|
| Customs Duty | Round to 2 decimal places (0.01) |
| VAT | Round to 2 decimal places (0.01) |
| Excise | Round to 4 decimal places (0.0001) |
| Total Liability | Round to 2 decimal places (0.01) |

**Implementation:** Python `decimal.ROUND_HALF_UP`

---

### 14.4 Assumptions and Exclusions

**Assumptions:**
- All values are in KHR (Cambodian Riel)
- Exchange rates applied at time of declaration
- Preferential rates require valid certificate of origin
- VAT calculated on (CIF Value + Customs Duty)

**Exclusions:**
- Anti-dumping duties not included
- Countervailing duties not included
- Safeguard measures not included
- Specific duties (per unit) not implemented

---

### 14.5 Verification Checklist

| Formula | Source Document | Code Implementation | Status |
|---------|------------------|---------------------|--------|
| Ad Valorem Duty | calculation_formulas.md §1.1 | duty_calculator.py | ✅ VERIFIED |
| Preferential Duty | calculation_formulas.md §1.4 | duty_calculator.py | ✅ VERIFIED |
| VAT Calculation | calculation_formulas.md §4 | vat_calculator.py | ✅ VERIFIED |
| Excise Calculation | calculation_formulas.md §3 | excise_calculator.py | ✅ VERIFIED |
| Total Revenue | calculation_formulas.md §5 | total_revenue.py | ✅ VERIFIED |

---

**Note:** These formulas represent the mathematical structure of tax calculations 
as established under customs law. They are presented with synthetic numerical 
examples for validation purposes only.

**Document Status**: APPROVED - Revenue Logic Verified