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

**Note:** These formulas represent the mathematical structure of tax calculations as established under customs law. They are presented without numerical examples or actual data references.