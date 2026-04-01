# Dashboard Specification - Power BI Dashboards
# Phase 9 - Dashboards & Reports (POLICY VIEW)

This document specifies the Power BI dashboard designs for the Customs Revenue Analytics platform.
All dashboards use synthetic data only and include appropriate disclaimers.

---

## Dashboard Structure

```
dashboards/
├── executive/
│   ├── revenue_overview.pbix      # Executive Revenue Dashboard
│   └── trade_summary.pbix         # Trade Composition Dashboard
├── operations/
│   ├── daily_collections.pbix     # Daily Collections
│   └── port_performance.pbix      # Port Performance
└── compliance/
    ├── revenue_variance.pbix      # Trend Analysis
    └── risk_monitoring.pbix       # Risk Monitoring
```

---

## 9.1 Dashboard Specifications

### Executive Dashboard 1: Revenue Overview

**Purpose:** Executive-level revenue summary for decision-makers

**Visualizations:**
- Total Revenue KPI card (with trend indicator)
- Monthly Revenue line chart (24-month trend)
- Revenue by Tax Type pie chart (Duty, VAT, Excise)
- Revenue by Port horizontal bar chart (top 10 ports)
- Year-over-Year comparison table

**Data Source:** mv_monthly_revenue (aggregated)

**Safety Features:**
- No drill-down to declaration level
- No individual importer identifiers
- Minimum 5 records per visual

---

### Executive Dashboard 2: Trade Summary

**Purpose:** Trade composition analysis at aggregate level

**Visualizations:**
- Total Trade Value KPI card
- Trade by Country treemap (top 20 countries)
- Trade by HS Chapter bar chart (top 10 chapters)
- Monthly Trade Volume area chart
- Top Importers summary table (aggregated rankings only)

**Data Source:** mv_trade_by_country, mv_trade_by_hs (aggregated)

**Safety Features:**
- Country-level aggregation only
- HS chapter-level aggregation (no tariff lines)
- No drill-down to individual shipments

---

### Operations Dashboard 1: Daily Collections

**Purpose:** Operational view of daily revenue collections

**Visualizations:**
- Daily Collections bar chart
- Collections by Payment Method pie chart
- Clearance Rate trend line
- Port Activity heatmap

**Data Source:** Aggregated from declarations (daily level)

**Safety Features:**
- Daily aggregates only (no individual records)
- Port-level aggregation (no shipment details)

---

### Operations Dashboard 2: Port Performance

**Purpose:** Port-level performance metrics

**Visualizations:**
- Port Rankings table (by value, volume, duty)
- Port Comparison scatter plot
- Average Clearance Time by Port
- Declaration Count by Port

**Data Source:** Aggregated by port

**Safety Features:**
- Port-level aggregation only
- No individual declaration drill-down

---

### Compliance Dashboard 1: Revenue Variance

**Purpose:** Trend analysis for compliance monitoring

**Visualizations:**
- Variance trend line
- Top Variance Items table (aggregated)
- Variance by HS Chapter bar chart
- Alert summary KPI cards

**Data Source:** Aggregated variance metrics

**Safety Features:**
- Aggregated variance data only
- No individual declaration exposure

---

### Compliance Dashboard 2: Risk Monitoring

**Purpose:** Risk assessment dashboard

**Visualizations:**
- Risk Distribution pie chart
- High-Risk Entities summary
- Risk Score trend
- Risk by Country heatmap

**Data Source:** Aggregated risk metrics

**Safety Features:**
- Aggregated risk counts only
- No individual entity identification

---

## 9.2 Labeling Requirements

### Header Banner (All Dashboards)

```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️ SYNTHETIC DATA ONLY - DEMONSTRATION PURPOSES          │
│                                                             │
│  This dashboard displays synthetic data generated for      │
│  analytics methodology testing only. All figures are       │
│  fictional and do not represent real customs operations.   │
└─────────────────────────────────────────────────────────────┘
```

### Disclaimer Footer (All Dashboards)

```
┌─────────────────────────────────────────────────────────────┐
│  DISCLAIMER: This is a demonstration system using synthetic │
│  data. Not for production use. Data is purely illustrative. │
│  No real revenue, trade, or entity information is shown.   │
└─────────────────────────────────────────────────────────────┘
```

### Report-Level Notes

Each dashboard footer must include:
1. "Data Source: Synthetic Generator v1.0"
2. "Generation Date: [Date]"
3. "Privacy Status: No PII - All Data Synthetic"
4. "Aggregation: Minimum threshold: 5 records"

---

## 9.3 Validation Checklist

### Data Integrity
- [ ] All KPI values match API response values (±0.1%)
- [ ] Charts aggregate correctly from source
- [ ] Time periods consistent across all visuals
- [ ] Currency formatting consistent

### Safety Verification
- [ ] No raw declaration IDs visible
- [ ] No individual importer identifiers
- [ ] No drill-through to detail tables possible
- [ ] Minimum threshold applied (5 records)
- [ ] All labels and disclaimers present

### Visual Verification
- [ ] All titles clearly indicate "Synthetic" or "Demonstration"
- [ ] Color scheme indicates non-production status
- [ ] Tooltips do not expose individual records

---

## Dashboard Metadata

| Dashboard | Source View | Update Frequency | Safety Level |
|-----------|-------------|------------------|--------------|
| Revenue Overview | mv_monthly_revenue | Daily | Aggregated |
| Trade Summary | mv_trade_by_* | Daily | Aggregated |
| Daily Collections | mv_monthly_revenue | Daily | Aggregated |
| Port Performance | mv_trade_by_* | Daily | Aggregated |
| Revenue Variance | Compliance Views | Daily | Aggregated |
| Risk Monitoring | Compliance Views | Daily | Aggregated |

---

## Implementation Notes

1. **Power BI Connection:** Connect to PostgreSQL views (not base tables)
2. **RLS Implementation:** Not required (data is already aggregated)
3. **Export Restrictions:** Disable export of underlying data
4. **Sharing:** Share only via read-only Power BI workspace

---

**Status:** Dashboard specifications complete

**Verification:**
- ✅ Executive dashboards defined (revenue overview, trade composition)
- ✅ Trend analysis dashboard defined
- ✅ Labeling specifications added (Synthetic Data banner, disclaimer footer)
- ✅ Validation checklist provided
- ✅ No drill-down to raw data possible (connected to views only)  
  
## Phase 11: Dashboard Freeze  
  
**Status:** FROZEN as of 2026-04-01 (v1.0-demo) 
