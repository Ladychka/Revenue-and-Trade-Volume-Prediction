# Domain Glossary - Customs Revenue Analytics

## Purpose
This document provides abstract definitions for core customs domain concepts, established through conceptual study without reference to actual operational data.

---

## 1. Core Entity Definitions

### 1.1 Declaration (Abstract)

**Definition:** A Declaration is an abstract construct representing a formal communication to customs authorities containing particulars of goods, their classification, origin, value, and the intended customs treatment, submitted by or on behalf of an importer or exporter.

**Key Attributes (Abstract):**
- **Declaration Identifier:** Unique reference assigned to distinguish each Declaration
- **Declaration Type:** Classification indicating the purpose (e.g., import, export, transit, temporary admission)
- **Declaration Date:** Timestamp of submission or acceptance
- **Declarant:** Party submitting the Declaration (abstract entity reference)
- **Trader:** Owner or consignee of the goods (abstract entity reference)
- **Office of Entry/Exit:** Customs office where goods are entered
- **Status:** Lifecycle state (e.g., lodged, processed, cleared, rejected)
- **Items:** Collection of goods covered by this Declaration

**Note:** The Declaration itself is an abstract container - it does not contain goods but references Items that collectively represent the goods described.

---

### 1.2 Item (Abstract)

**Definition:** An Item is an abstract construct representing a distinct line entry within a Declaration, describing a specific quantity of goods with their classification, value, and applicable duties.

**Key Attributes (Abstract):**
- **Item Sequence Number:** Position of the Item within the parent Declaration
- **HS Code:** Harmonized System code classifying the goods (6 to 10 digits)
- **Goods Description:** Textual description of the goods
- **Origin Country:** Country where goods were produced or last substantially transformed
- **Quantity:** Measurement of goods (e.g., net mass in kilograms, supplementary unit)
- **Statistical Quantity:** Quantity for statistical purposes
- **Customs Value:** Value upon which duty is assessed (after adjustments)
- **Duty Rate:** Applicable rate of customs duty (percentage or fixed amount)
- **Excise Rate:** Applicable excise duty rate (if applicable)
- **VAT Rate:** Applicable value-added tax rate
- **Tax Assessment:** Abstract representation of taxes due for this Item
- **Preferential Treatment:** Indicator of eligibility for preferential duty rates

**Note:** Each Item represents a separable portion of goods that can be separately classified, valued, and taxed.

---

### 1.3 Tax Assessment (Abstract)

**Definition:** A Tax Assessment is an abstract construct representing the determination and computation of taxes, duties, and other charges payable upon importation or exportation of goods.

**Key Attributes (Abstract):**
- **Assessment Identifier:** Unique reference for the Tax Assessment
- **Associated Item:** Reference to the Item to which this assessment applies
- **Customs Duty:** Amount of customs duty calculated
- **Excise Duty:** Amount of excise duty calculated (if applicable)
- **Value-Added Tax (VAT):** Amount of VAT calculated
- **Other Duties/Charges:** Additional charges (e.g., anti-dumping, countervailing, surcharges)
- **Total Tax Liability:** Sum of all assessed taxes and duties
- **Tax Base:** Value or quantity upon which taxes are calculated
- **Assessment Date:** Date when assessment was computed
- **Currency:** Currency in which amounts are expressed

**Note:** The Tax Assessment represents the computational result of applying tax rules to an Item's attributes.

---

## 2. Supporting Concepts

### 2.1 Harmonized System (HS) Code

**Definition:** A standardized numerical method of classifying traded products, maintained by the World Customs Organization (WCO), used by more than 200 countries as the basis for customs tariffs and trade statistics.

**Structure:**
- Chapter (2 digits): Broadest level (e.g., 84 = Nuclear Reactors)
- Heading (4 digits): More specific category
- Subheading (6 digits): Further subdivision
- National Tariff Line (8-10 digits): Country-specific extension

### 2.2 Customs Value

**Definition:** The value of goods for customs purposes, determined according to the principles of the WTO Customs Valuation Agreement, used as the basis for calculating import duties.

**Components:**
- Transaction value (price paid or payable)
- Adjustments: freight, insurance, packing, royalties, etc.

### 2.3 Origin

**Definition:** The country where goods were produced, grown, manufactured, or substantially transformed, determining applicable duty rates and preferential treatment eligibility.

**Types:**
- Preferential origin (under free trade agreements)
- Non-preferential origin (for MFN duties, marking requirements)

### 2.4 Duty Rate

**Definition:** The percentage or specific amount of customs duty applicable to imported goods, determined by their HS classification and origin.

**Types:**
- Ad valorem: Percentage of customs value
- Specific: Fixed amount per unit
- Compound: Combination of both

---

## 3. Tax Type Definitions

### 3.1 Customs Duty

**Definition:** A tax imposed on goods when they cross national borders, calculated based on the classification, value, and origin of goods.

**Legal Basis:** National customs legislation, tariff schedules

### 3.2 Excise Duty

**Definition:** An indirect tax levied on specific goods (e.g., alcohol, tobacco, petroleum products) at the point of manufacture or import, typically based on quantity or value.

**Legal Basis:** Excise taxation acts, specific product regulations

### 3.3 Value-Added Tax (VAT)

**Definition:** A consumption tax applied to goods and services at each stage of production and distribution, calculated on the value added at each stage, with import VAT applied on customs value plus duties.

**Legal Basis:** VAT legislation, typically applied at standard or reduced rates

---

## 4. Process-Related Definitions

### 4.1 Clearance

**Definition:** The process by which goods are authorized for release from customs control after verification of Declaration, payment of duties, and compliance with regulations.

### 4.2 Risk Assessment

**Definition:** The systematic evaluation of Declaration characteristics to identify potential compliance risks, using criteria such as HS code, origin, declarant history, and declared value.

### 4.3 Post-Clearance Audit

**Definition:** Examination of Declaration and supporting documentation after clearance to verify correctness of classification, valuation, and duty payment.

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2026-03-31 | Initial release - Phase 1 Domain Understanding |

---

**Status:** DRAFT - Subject to refinement during Phase 1

**Note:** This glossary represents abstract domain concepts derived from public knowledge sources and legal frameworks. No actual operational data has been referenced in its creation.