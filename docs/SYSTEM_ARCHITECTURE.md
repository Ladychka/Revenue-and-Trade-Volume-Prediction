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

CLASSIFICATION: Non-Production - 100% Synthetic Data
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