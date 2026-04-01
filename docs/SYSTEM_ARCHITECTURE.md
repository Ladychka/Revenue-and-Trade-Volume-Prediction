# Customs Revenue Analytics Platform - System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                    CUSTOMS REVENUE ANALYTICS PLATFORM                     │
│              (100% Synthetic Data - Demo System)                 │
└──────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                             │
              GOVERNANCE                    DATA LAYER
              LAYER                          │
     ┌──────────────┐                ┌──────────────┐
     │ PROJECT_    │                │ RAW DATA    │
     │ DECLARATION │                │            │
     └──────────────┘                │ Synthetic │
              │                     │ Generator  │
     ┌──────────────┐                │            │
     │ DATA_       │                └──────┬─────┘
     │ PRIVACY_    │                     │
     │ POLICY     │                ┌────▼─────┐
     └─────────────┘                │ STAGING  │
              │                     │ DATA     │
     ┌──────────────┐                └────┬─────┘
     │ SCOPE_       │                     │
     │ FREEZE      │                ┌──────▼──────┐
     └─────────────┘                │  CURATED   │
                                    │  DATA      │
                                    └──────┬─────┘
                                           │
┌──────────────────────────────────────────┴────────────────────────┐
│                         CORE LAYER                                       │
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │    REVENUE        │  │    TRADE        │  │  COMPLIANCE       │ │
│  │    CALCULATOR    │  │    AGGREGATOR   │  │  ANALYTICS      │ │
│  │                 │  │                 │  │                 │ │
│  │ Duty Calc      │  │ Trade by HS    │  │ Risk Scoring   │ │
│  │ VAT Calc       │  │ Trade by Country│ │ Variance Detect│ │
│  │ Excise Calc    │  │ Trade by Month  │  │ Under-decl.    │ │
│  │ Total Revenue │  │ Volume Metrics │  │ Flags         │ │
│  └──────┬───────┘  └───────┬────────┘  └──────┬────────┘ │
│         │                  │                   │           │
└─────────┼──────────────────┼───────────────────┼───────────┘
          │                  │                   │
┌────────▼──────────────────▼───────────────────▼──────────┐
│                   LOGICAL LAYER                            │
│                                                      │
│     ┌─────────┐    ┌──────────┐    ┌──────────┐    │
│     │Declarat-│    │Declarat-│    │ Payment │    │
│     │ ions   │    │ ion_    │    │        │    │
│     │        │    │ Items   │    │        │    │
│     └────────┘    └────┬───┘    └────────┘    │
│                       │                        │
│              ┌────────▼───────┐    ┌──────▼──────┐
│              │ HS_CODE_      │    │ EXCHANGE_   │
│              │ REFERENCE    │    │ RATE       │
│              └──────────────┘    └────────────┘
│                                                      │
│              PORT_     COUNTRY_    TRADER_            │
│              REFERENCE REFERENCE  REFERENCE         │
│                                                      │
└──────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────┐
│               PHYSICAL LAYER (PostgreSQL)                │
│                                                      │
│  ┌──────────────────────────────────────────────┐     │
│  │  CORE TABLES                                 │     │
│  │  ├── declarations                           │     │
│  │  ├── declaration_items                    │     │
│  │  ├── payments                            │     │
│  │  └── exchange_rates                      │     │
│  └──────────────────────────────────────────────┘     │
│                                                      │
│  ┌──────────────────────────────────────────────┐     │
│  │  REFERENCE TABLES                         │     │
│  │  ├── hs_code_reference                    │     │
│  │  ├── port_reference                     │     │
│  │  ├── country_reference                 │     │
│  │  ├── currency_reference              │     │
│  │  └── trader_reference                 │     │
│  └──────────────────────────────────────────────┘     │
│                                                      │
│  ┌──────────────────────────────────────────────┐     │
│  │  MATERIALIZED VIEWS                       │     │
│  │  ├── mv_monthly_revenue                   │     │
│  │  ├── mv_trade_by_country                 │     │
│  │  └── mv_trade_by_hs                     │     │
│  └──────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────┐
│                  ANALYTICS LAYER                       │
│                                                      │
│    ┌─────────────────────────────────────────┐       │
│    │         ANALYTICS QUERIES                 │       │
│    │    monthly_revenue.sql                   │       │
│    │    revenue_by_port.sql                 │       │
│    │    revenue_by_tax_type.sql             │       │
│    │    trade_by_country.sql               │       │
│    │    trade_by_hs.sql                   │       │
│    │    top_importers.sql                 │       │
│    └─────────────────────────────────────────┘       │
│                                                      │
│    ┌─────────────────────────────────────────┐       │
│    │        ANALYTICS QUERIES                │       │
│    │    high_risk_entities.sql              │       │
│    │    variance_summary.sql               │       │
│    └─────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────┐
│                    API LAYER                            │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │              FASTAPI SERVER                  │   │
│  │                                              │   │
│  │  GET /api/v1/revenue/summary        [AGGR]     │   │
│  │  GET /api/v1/revenue/monthly       [AGGR]      │   │
│  │  GET /api/v1/revenue/by-port       [AGGR]      │   │
│  │  GET /api/v1/revenue/by-tax-type  [AGGR]      │   │
│  │  GET /api/v1/trade/summary         [AGGR]     │   │
│  │  GET /api/v1/trade/by-country    [AGGR]       │   │
│  │  GET /api/v1/trade/by-hs         [AGGR]       │   │
│  │  GET /api/v1/trade/time-series   [AGGR]       │   │
│  │  GET /api/v1/compliance/risk    [AGGR]       │   │
│  │  GET /api/v1/compliance/variance[AGGR]      │   │
│  │                                              │   │
│  │  🔒 All endpoints READ-ONLY                │   │
│  │  📊 All responses AGGREGATED only          │   │
│  │  📝 All access LOGGED                     │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────┐
│               DASHBOARD LAYER                           │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │           POWER BI DASHBOARDS                │   │
│  │                                              │   │
│  │  EXECUTIVE DASHBOARDS:                       │   │
│  │  ├── Revenue Overview                       │   │
│  │  └── Trade Summary                          │   │
│  │                                              │   │
│  │  OPERATIONS DASHBOARDS:                      │   │
│  │  ├── Daily Collections                      │   │
│  │  └── Port Performance                      │   │
│  │                                              │   │
│  │  COMPLIANCE DASHBOARDS:                      │   │
│  │  ├── Revenue Variance                      │   │
│  │  └── Risk Monitoring                       │   │
│  │                                              │   │
│  │  ⚠️  ALL LABELED 'SYNTHETIC DATA ONLY'     │   │
│  │  📝  DISCLAIMER ON ALL DASHBOARDS            │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘


==================================================================
                          DATA FLOW
==================================================================

┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ SYNTHETIC│────▶│  LOAD   │────▶│TRANSFORM│────▶│ VERIFY  │
│ GENERAT │     │  (ETL)  │     │        │     │        │
│   OR    │     │         │     │        │     │        │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                                              │
                                              ▼
┌──────────────────────────────────────────────────────────┐
│                   STORAGE LAYER                         │
│         PostgreSQL (Materialized Views)                │
└──────────────────────────────────────────────────────────┘
                                              │
                                              ▼
┌──────────────────────────────────────────────────────────┐
│                   ACCESS LAYER                         │
│         API (Read-Only)  +  Dashboards (View)           │
└──────────────────────────────────────────────────────────┘


==================================================================
                    PRIVACY BY DESIGN
==================================================================

┌─────────────────────────────────────────────────────────────┐
│  ✓ No PII in schema                                       │
│  ✓ No real identifiers (DEC-*, IMP-*, PMT-* format only)  │
│  ✓ No external data connections                          │
│  ✓ Minimum threshold: 5 records per aggregation          │
│  ✓ All identifiers SYNTHETIC                            │
│  ✓ All access LOGGED                                  │
│  ✓ Aggregate-only outputs                             │
└─────────────────────────────────────────────────────────────┘


==================================================================
                    STACK COMPONENTS
==================================================================

┌─────────────────────────────────────────────────────────────┐
│  FRONTEND     │  Power BI Dashboards                      │
├──────────────┼────────────────────────────────────────────┤
│  API         │  FastAPI (Python)                         │
├──────────────┼────────────────────────────────────────────┤
│  CORE LOGIC  │  Python Revenue & Trade Calculators       │
├──────────────┼────────────────────────────────────────────┤
│  DATABASE   │  PostgreSQL                               │
├──────────────┼────────────────────────────────────────────┤
│  ORCHESTRA  │  Docker Compose                          │
└──────────────┴────────────────────────────────────────────┘


==================================================================
                         STATUS
==================================================================

✅ Phase 1  - Domain Understanding
✅ Phase 2  - Synthetic Data Design
✅ Phase 3  - Logical System Design
✅ Phase 4  - Physical Schema
✅ Phase 5  - Revenue Logic
✅ Phase 6  - Trade Analytics
✅ Phase 7  - Analytics Optimization
✅ Phase 8  - API (Read-Only, Safe)
✅ Phase 9  - Dashboards & Reports
✅ Phase 10 - Privacy Audit
✅ Phase 11 - System Freeze & Baseline Control
✅ Phase 12 - Architecture Documentation

CLASSIFICATION: Non-Production - 100% Synthetic Data

---

## 12.1 High-Level System Architecture

The Customs Revenue Analytics Platform is a demonstration system that provides aggregated 
analytics on customs revenue and trade volume. All data is synthetic - no real trade 
information is stored or processed.

### Data Flow

```
SYNTHETIC DATA → ETL → DATABASE → AGGREGATION → API → DASHBOARD
```

### What This System Does

1. **Generates** synthetic customs declarations, payments, and trade data
2. **Calculates** duty, VAT, and excise taxes based on HS codes
3. **Aggregates** trade and revenue by country, port, and time period
4. **Serves** aggregated data through read-only APIs
5. **Displays** analytics in Power BI dashboards

### What This System Cannot Do

- ❌ Cannot access real customs declarations
- ❌ Cannot identify real importers or traders
- ❌ Cannot process actual payment transactions
- ❌ Cannot connect to government systems
- ❌ Cannot generate official tax documents

---

## 12.2 Component Descriptions

| Layer | Component | Responsibility | Limitation |
|-------|-----------|----------------|------------|
| Data Generation | generate_synthetic_data.py | Create fake declarations/payments | Cannot access real data |
| Database | PostgreSQL | Store and query data | Cannot store PII |
| Core Logic | revenue/*, trade/* | Tax calculations, aggregations | Cannot process real taxes |
| API | FastAPI | Serve aggregated data | Cannot modify data |
| Visualization | Power BI | Display dashboards | Cannot drill-down |

---

## 12.3 Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Database | PostgreSQL | Store synthetic data & views |
| ETL | Python scripts | Generate & load data |
| Core Logic | Python | Tax calculations |
| API | FastAPI | Read-only REST endpoints |
| Visualization | Power BI | Dashboards |
| Orchestration | Docker Compose | Container management |
APPROVED FOR:   Demo / Portfolio / Proposal Use


==================================================================
                    VERSION INFO
==================================================================

Project:    Customs Revenue & Trade Volume Prediction Analytics
Version:    1.0.0
Date:       2026-03-31
Status:    COMPLETE
Repository: https://github.com/Ladychka/Revenue-and-Trade-Volume-Prediction


==================================================================  
  
==================================================================  
PHASE 12 - ARCHITECTURE DOCUMENTATION  
==================================================================  
 
