# Phase 15 - Analytics & Insight Definition

## Purpose
This document defines the Key Performance Indicators (KPIs) and analytical insights 
that the Customs Revenue Analytics Platform can generate. All insights are aggregate-only 
and do not identify individual entities.

---

## 15.1 KPI Definitions

### Revenue KPIs

| KPI | Definition | Formula | Data Source |
|-----|-------------|---------|--------------|
| **Total Revenue** | Total tax collected (duty + VAT + excise) | SUM(total_tax_liability) | mv_monthly_revenue |
| **Revenue Growth Rate** | Month-over-month revenue change | ((Current - Previous) / Previous) × 100 | mv_monthly_revenue |
| **Duty Collection** | Total customs duty collected | SUM(total_customs_duty) | mv_monthly_revenue |
| **VAT Collection** | Total VAT collected | SUM(total_vat) | mv_monthly_revenue |
| **Average Declaration Value** | Mean customs value per declaration | AVG(total_customs_value) | mv_monthly_revenue |
| **Effective Duty Rate** | Average duty rate applied | SUM(duty) / SUM(value) | mv_monthly_revenue |

### Trade KPIs

| KPI | Definition | Formula | Data Source |
|-----|-------------|---------|--------------|
| **Total Trade Value** | Total customs value of imports | SUM(customs_value) | mv_trade_by_hs |
| **Trade Volume** | Total quantity of goods | SUM(quantity) | mv_trade_by_hs |
| **Declaration Count** | Number of cleared declarations | COUNT(*) | mv_monthly_revenue |
| **Item Count** | Total line items processed | SUM(total_items) | mv_monthly_revenue |
| **Average Shipment Value** | Mean value per shipment | AVG(customs_value) | mv_trade_by_hs |

### Concentration KPIs

| KPI | Definition | Formula | Data Source |
|-----|-------------|---------|--------------|
| **Commodity Concentration** | Top HS code share of total | (Top HS value / Total value) × 100 | mv_trade_by_hs |
| **Country Concentration** | Top country share of total | (Top Country value / Total value) × 100 | mv_trade_by_country |
| **Port Concentration** | Top port share of total | (Top Port value / Total value) × 100 | mv_trade_by_country |

---

## 15.2 Aggregation Levels

### By Time Period

| Level | Granularity | Use Case |
|-------|-------------|----------|
| Monthly | Month | Revenue trends, seasonal analysis |
| Quarterly | Quarter | Fiscal period reporting |
| Yearly | Year | Annual comparison |

### By HS Code

| Level | Example | Use Case |
|-------|---------|----------|
| Chapter | 84 (Machinery) | Sector-level analysis |
| Heading | 8471 (Computers) | Product category analysis |
| Subheading | 847130 (Laptops) | Detailed product analysis |

### By Country

| Level | Use Case |
|-------|----------|
| Origin Country | Trading partner analysis |
| Region | Geographic clustering |

### By Port

| Level | Use Case |
|-------|----------|
| Port Code | Port performance |
| Region | Regional logistics |

---

## 15.3 Insight Boundaries

### ✅ Supported Insights

The following insights are supported by the system:

1. **Revenue Trends**
   - Monthly/quarterly/yearly revenue totals
   - Growth rates (month-over-month, year-over-year)
   - Duty vs VAT composition

2. **Trade Patterns**
   - Trade value by country of origin
   - Trade by HS chapter/heading
   - Top traded commodities

3. **Port Performance**
   - Revenue by port
   - Trade volume by port
   - Processing efficiency

4. **Commodity Analysis**
   - Top HS codes by value
   - Sector distribution
   - Duty collection by commodity

5. **Risk Indicators**
   - Variance from expected revenue
   - High-risk HS code patterns
   - Country risk profiles

### ❌ Unsupported Insights

The following insights are NOT supported by the system:

| Unsupported Insight | Reason |
|---------------------|--------|
| Individual company analysis | Aggregate only |
| Specific importer activity | No declarant-level data |
| Single declaration details | Aggregation threshold: 5+ |
| Real-time clearance status | System is non-operational |
| Auditor-specific findings | Not applicable |
| Broker performance | No broker data |
| Specific penalty cases | Not applicable |
| Real inspection outcomes | Not applicable |
| Actual seizure records | Not applicable |

---

## 15.4 Aggregation Rules

### Minimum Threshold
- All aggregations require minimum **5 records**
- Prevents re-identification through small samples

### Data Granularity Limits
- **Time**: Minimum monthly (no daily for sensitive data)
- **Geography**: Minimum country-level (no facility-level)
- **HS Code**: Minimum 2-digit chapter level

### Privacy Controls
- No cell with < 5 records displayed
- Top-N queries limited to top 10/20
- Percentages shown instead of counts where appropriate

---

## 15.5 KPI Verification Table

| KPI | Aggregation | Threshold | Privacy Safe |
|-----|-------------|-----------|---------------|
| Total Revenue | SUM | N/A | ✅ |
| Revenue Growth | CALC | 5 records | ✅ |
| Trade Value | SUM | N/A | ✅ |
| Top Countries | TOP-N | 5 records | ✅ |
| Top HS Codes | TOP-N | 5 records | ✅ |
| Port Performance | GROUP BY | 5 records | ✅ |
| Effective Duty Rate | CALC | N/A | ✅ |

---

## Document Control

**Status**: APPROVED - Analytics definitions complete

**Version**: 1.0.0

**Date**: 2026-04-01

---

## Phase Completion

| Phase | Status |
|-------|--------|
| Phase 1-14 | ✅ Complete |
| Phase 15 - Analytics Definition | ✅ COMPLETE |

**All KPIs are aggregate-only and non-identifiable** ✅
