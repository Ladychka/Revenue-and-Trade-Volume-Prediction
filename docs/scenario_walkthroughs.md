# Phase 16 - Scenario & Use-Case Walkthroughs (Synthetic)

## Purpose
This document demonstrates the value of the Customs Revenue Analytics Platform through 
realistic synthetic scenarios. All data shown is artificial and for demonstration only.

---

## 16.1 Scenario Design

### Scenario A: Revenue Trend Analysis

**Context:** Policy makers need to understand monthly revenue trends to budget effectively.

**Dashboard:** Revenue Overview (Executive)

**Synthetic Data Observation:**
| Month | Total Revenue (KHR) | vs Previous Month |
|-------|---------------------|-------------------|
| 2024-01 | 85,400,000,000 | - |
| 2024-02 | 82,100,000,000 | -3.9% |
| 2024-03 | 91,500,000,000 | +11.5% |
| 2024-04 | 88,900,000,000 | -2.8% |
| 2024-05 | 94,200,000,000 | +6.0% |
| 2024-06 | 97,800,000,000 | +3.8% |

**Analysis:**
- Strong growth in Q1-Q2 2024 (+14.5% overall)
- Seasonal spike in March due to imported goods cycle
- Steady improvement in duty collection

**Policy Insight:**
> "Revenue collection shows positive trend with 14.5% growth in H1 2024, suggesting tariff policy is effective. Recommend monitoring Q3 for seasonal adjustments."

**Visualization Mapping:**
- Line chart: Monthly revenue trend
- KPI card: Total revenue YTD
- Pie chart: Revenue by tax type (Duty, VAT, Excise)

---

### Scenario B: Policy Change Simulation - Preferential Tariff

**Context:** Government is considering extending RCEP preferential rates to more trading partners.

**Dashboard:** Trade Summary + Revenue by Tax Type

**Synthetic Scenario:**
Current RCEP-eligible imports: $2.5 billion (25% of total)
Proposed expansion to ASEAN+6: $3.2 billion (32% of total)

**Impact Projection:**
| Scenario | Trade Value | Duty Revenue | VAT Revenue |
|----------|-------------|--------------|-------------|
| Current (RCEP only) | $10.0B | $620M | $1.25B |
| Expanded (ASEAN+6) | $10.7B | $580M | $1.32B |
| Change | +7% | -6.5% | +5.6% |

**Analysis:**
- Lower duty revenue due to preferential rates
- Higher total trade volume compensates partially
- Net tax impact: Slight decrease (-1.2%)

**Policy Insight:**
> "Expanding preferential trade agreements may increase trade volume by 7% but reduce duty collection by 6.5%. Net effect is minimal revenue change but improved trade balance. Recommend proceeding with careful monitoring."

**Visualization Mapping:**
- Bar chart: Trade by country (before/after)
- KPI: Effective duty rate comparison

---

### Scenario C: Commodity Shift Analysis

**Context:** Understanding how import composition is changing over time.

**Dashboard:** Trade by HS Code

**Synthetic Data Observation:**
| HS Chapter | 2024 Share | 2025 Share | Change |
|------------|------------|------------|--------|
| 84 (Machinery) | 28% | 32% | +4% |
| 85 (Electronics) | 22% | 24% | +2% |
| 62 (Textiles) | 15% | 12% | -3% |
| 87 (Vehicles) | 10% | 11% | +1% |
| Other | 25% | 21% | -4% |

**Analysis:**
- Shift toward electronics and machinery (+6% combined)
- Decline in textile imports (-3%)
- Overall modernization of import basket

**Policy Insight:**
> "Import composition shifting toward higher-value electronics. This supports national industrial diversification goals. Consider targeted incentives for machinery sector growth."

**Visualization Mapping:**
- Stacked bar: Trade by HS chapter (2024 vs 2025)
- Treemap: Top 20 HS codes

---

### Scenario D: Geographic Trade Distribution

**Context:** Identifying key trading partners and regional dependencies.

**Dashboard:** Trade by Country

**Synthetic Data Observation:**
| Country | Trade Value (KHR) | Share | YoY Growth |
|---------|-------------------|-------|-------------|
| China | 3.5 trillion | 35% | +8% |
| Japan | 1.5 trillion | 15% | +3% |
| USA | 1.2 trillion | 12% | +5% |
| South Korea | 1.0 trillion | 10% | +12% |
| Thailand | 0.8 trillion | 8% | +2% |

**Analysis:**
- China dominant (35% share)
- Strong growth from Korea (+12%)
- Diversified trading partner base

**Policy Insight:**
> "Trade heavily concentrated in China (35%). Recommend trade diversification strategy focusing on emerging markets. Positive sign: strong growth from Korea indicates successful recent trade agreements."

**Visualization Mapping:**
- Treemap: Trade by country
- Bar chart: Top 10 countries

---

### Scenario E: Port Performance Review

**Context:** Evaluating operational efficiency across customs ports.

**Dashboard:** Port Performance

**Synthetic Data Observation:**
| Port | Declarations | Avg Processing Time | Revenue (KHR) |
|------|--------------|---------------------|---------------|
| PORT001 | 12,500 | 2.1 hours | 28.5B |
| PORT002 | 10,200 | 2.8 hours | 22.1B |
| PORT003 | 8,900 | 1.5 hours | 18.4B |
| PORT004 | 7,100 | 3.2 hours | 14.2B |
| PORT005 | 5,800 | 2.4 hours | 11.8B |

**Analysis:**
- PORT003 fastest (1.5 hours) but not highest volume
- PORT001 highest volume and good processing time
- PORT004 needs attention (high volume, slow processing)

**Policy Insight:**
> "PORT004 shows processing bottleneck with 3.2-hour average. Recommend staffing review. PORT003 could serve as best practice model for process optimization."

**Visualization Mapping:**
- Bar chart: Declarations by port
- KPI: Average processing time
- Map: Port locations (if available)

---

### Scenario F: Risk Monitoring Dashboard

**Context:** Identifying potential compliance risks.

**Dashboard:** Risk Monitoring

**Synthetic Data Observation:**
| Risk Indicator | Threshold | Actual | Status |
|-----------------|------------|--------|--------|
| Duty under-declaration | >5% variance | 2.1% | ✅ Normal |
| High-risk HS codes | >10% of total | 8.5% | ✅ Normal |
| Suspicious country pairs | >3 | 1 | ✅ Normal |
| Declared value vs market | >15% variance | 4.2% | ✅ Normal |

**Analysis:**
- All risk indicators within normal ranges
- No significant compliance issues detected
- System functioning as expected

**Policy Insight:**
> "Compliance metrics show stable pattern. No high-priority risks identified. Continue monitoring quarterly for anomalies."

**Visualization Mapping:**
- Gauge charts: Risk indicators
- Alert badges: Status indicators

---

## 16.2 Narrative Templates

### Template 1: Monthly Review
```
OBSERVATION: [Metric] shows [increase/decrease] of [X]% compared to [period]
ANALYSIS: This is attributed to [seasonal factors/policy changes/market conditions]
RECOMMENDATION: [Specific action or continued monitoring]
```

### Template 2: Policy Impact
```
PROPOSAL: [Policy change description]
ANALYSIS: Expected impact on revenue: [increase/decrease of X%]
RECOMMENDATION: [Proceed with caution/Proceed/Do not proceed]
```

### Template 3: Trend Analysis
```
TREND: [Metric] has [improved/declined] over [time period]
INSIGHT: This indicates [market shift/policy effectiveness/economic condition]
ACTION: Consider [specific intervention or continued observation]
```

---

## 16.3 Dashboard Mapping

| Scenario | Primary Dashboard | Supporting KPIs |
|----------|-------------------|------------------|
| Revenue Trend | revenue_overview.pbix | Total Revenue, Growth Rate |
| Policy Simulation | trade_summary.pbix | Trade by Country, Duty Rate |
| Commodity Shift | trade_summary.pbix | Trade by HS, Top Commodities |
| Geographic Distribution | trade_summary.pbix | Trade by Country |
| Port Performance | port_performance.pbix | Declarations, Processing Time |
| Risk Monitoring | risk_monitoring.pbix | All risk indicators |

---

## 16.4 Synthetic Labels

All dashboards include the following mandatory labels:

```
┌─────────────────────────────────────────────────────────┐
│  ⚠️ SYNTHETIC DATA ONLY - DEMO SYSTEM                   │
│  Data Source: Synthetic Generator v1.0                  │
│  Privacy Status: No PII - All Data Synthetic            │
│  Not for production use                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Document Control

**Status**: APPROVED - Scenarios complete

**Version**: 1.0.0

**Date**: 2026-04-01

---

## Exit Criteria Verification

| Requirement | Status |
|-------------|--------|
| Revenue trend scenario | ✅ Complete |
| Policy change simulation | ✅ Complete |
| Commodity shift scenario | ✅ Complete |
| Narrative creation | ✅ Complete |
| Visualization mapping | ✅ Complete |
| Understandable without technical explanation | ✅ Verified |

**Phase 16 Complete** - All scenarios are understandable without technical explanation.
