# Customs Revenue & Trade Volume Prediction Analytics Platform
## Project Architecture Overview

---

## 1. System Classification

| Attribute | Value |
|-----------|-------|
| **Project Type** | Analytics Demonstration System |
| **Data Status** | 100% Synthetic - No Real Data |
| **Operational Status** | Non-Production - Portfolio Ready |
| **Version** | 1.0-FINAL |
| **Last Updated** | 2026-04-02 |

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CUSTOMS REVENUE ANALYTICS PLATFORM                             │
│                              (Demo System - Pure Synthetic Data)                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
              ┌──────────────────────────────┼──────────────────────────────┐
              │                              │                              │
        GOVERNANCE                        DATA LAYER                      ACCESS
        LAYER                              │                              LAYER
              │                     ┌──────┴──────┐                       │
    ┌─────────┴─────────┐           │ SYNTHETIC   │              ┌───────┴───────┐
    │ PROJECT_          │           │ DATA        │              │   API         │
    │ DECLARATION       │           │ GENERATOR   │              │   (Read-Only) │
    └───────────────────┘           └──────┬──────┘              └───────┬───────┘
            │                              │                              │
    ┌───────┴───────┐                ┌──────▼──────┐                ┌──────▼──────┐
    │ DATA_         │                │ STAGING     │                │  POWER BI   │
    │ PRIVACY_      │                │ DATA        │                │  DASHBOARDS │
    │ POLICY        │                └──────┬──────┘                └─────────────┘
    └───────────────┘                       │
    ┌───────────────┐                 ┌──────▼──────┐
    │ SYSTEM_       │                 │ CURATED     │
    │ FREEZE        │                 │ DATA        │
    └───────────────┘                 └─────────────┘
```

---

## 3. Layer-by-Layer Architecture

### 3.1 Governance Layer
```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GOVERNANCE LAYER                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐  ┌──────────────────────┐                   │
│  │ PROJECT_             │  │ DATA_                │                   │
│  │ DECLARATION          │  │ PRIVACY_             │                   │
│  │                      │  │ POLICY               │                   │
│  │ • Classification     │  │ • No PII             │                   │
│  │ • Use Cases          │  │ • No Real IDs        │                   │
│  │ • Limitations        │  │ • Aggregate Only     │                   │
│  └──────────────────────┘  └──────────────────────┘                   │
│  ┌──────────────────────┐  ┌──────────────────────┐                   │
│  │ SCOPE_               │  │ SYSTEM_              │                   │
│  │ FREEZE               │  │ FREEZE               │                   │
│  │                      │  │                      │                   │
│  │ • Feature Lock       │  │ • Version Lock       │                   │
│  │ • Change Control     │  │ • No Modifications   │                   │
│  └──────────────────────┘  └──────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Data Layer
```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ RAW DATA (CSV Files)                                            │   │
│  │ ├── declarations.csv         (~6.2 MB - Main declarations)      │   │
│  │ ├── declaration_items.csv    (~26 MB - Line items)              │   │
│  │ ├── payments.csv             (~5.3 MB - Payment records)         │   │
│  │ └── exchange_rates.csv       (~109 KB - Currency rates)          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ STAGING DATA                                                    │   │
│  │ ├── cleaned_declarations/                                        │   │
│  │ └── validated_payments/                                          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ CURATED DATA                                                    │   │
│  │ ├── revenue/                                                     │   │
│  │ └── trade_volume/                                                │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Core Business Logic Layer
```
┌─────────────────────────────────────────────────────────────────────────┐
│                      CORE BUSINESS LOGIC LAYER                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌───────────────┐  │
│  │    REVENUE          │  │    TRADE            │  │  COMPLIANCE   │  │
│  │    CALCULATOR       │  │    AGGREGATOR       │  │  ANALYTICS    │  │
│  ├─────────────────────┤  ├─────────────────────┤  ├───────────────┤  │
│  │ duty_calculator.py │  │ trade_aggregation.py│  │ risk_scoring.py│  │
│  │ vat_calculator.py  │  │ volume_metrics.py   │  │ variance_     │  │
│  │ excise_calculator.py│  │ trend_analysis.py  │  │ detection.py   │  │
│  │ total_revenue.py   │  │                     │  │ under_declara-│  │
│  │                    │  │                     │  │ tion_flags.py │  │
│  └─────────┬──────────┘  └─────────┬──────────┘  └───────┬───────┘  │
│            │                      │                      │           │
│  ┌─────────▼──────────────────────▼──────────────────────▼─────────┐ │
│  │                    SHARED COMPONENTS                             │ │
│  │  ├── common/constants.py     (HS codes, tax rates, regions)    │ │
│  │  ├── common/time_utils.py    (Date handling, periods)          │ │
│  │  └── common/rounding_rules.py (Currency rounding rules)         │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.4 Database Layer (PostgreSQL)
```
┌─────────────────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER (PostgreSQL)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ CORE TABLES                                                      │   │
│  │ ├── declarations          (declaration_id, date, port, trader) │   │
│  │ ├── declaration_items    (item_id, hs_code, qty, value, duty)  │   │
│  │ ├── payments             (payment_id, amount, tax_type, date)    │   │
│  │ └── exchange_rates      (date, currency_code, rate)             │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ REFERENCE TABLES                                                 │   │
│  │ ├── hs_code_reference  (hs_code, description, duty_rate, etc)  │   │
│  │ ├── port_reference     (port_code, name, region, type)         │   │
│  │ ├── country_reference  (country_code, name, region)            │   │
│  │ ├── currency_reference  (currency_code, name, symbol)           │   │
│  │ └── trader_reference   (trader_id, type, category)              │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ VIEWS                                                            │   │
│  │ ├── revenue_views.sql     (Monthly revenue summaries)           │   │
│  │ ├── trade_views.sql       (Trade volume by dimension)           │   │
│  │ └── compliance_views.sql (Risk indicators)                     │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ MATERIALIZED VIEWS                                              │   │
│  │ ├── mv_monthly_revenue    (Pre-aggregated monthly totals)       │   │
│  │ ├── mv_trade_by_country  (Pre-aggregated by country)            │   │
│  │ └── mv_trade_by_hs       (Pre-aggregated by HS code)            │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.5 API Layer (FastAPI)
```
┌─────────────────────────────────────────────────────────────────────────┐
│                         API LAYER (FastAPI)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  BASE URL: /api/v1                                                      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ REVENUE ENDPOINTS                                               │   │
│  │ GET /revenue/summary          - Overall revenue summary         │   │
│  │ GET /revenue/monthly         - Monthly revenue trends           │   │
│  │ GET /revenue/by-port         - Revenue breakdown by port        │   │
│  │ GET /revenue/by-tax-type     - Revenue by tax type (D/VAT/E)    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ TRADE ENDPOINTS                                                 │   │
│  │ GET /trade/summary           - Overall trade summary            │   │
│  │ GET /trade/by-country        - Trade volume by country          │   │
│  │ GET /trade/by-hs             - Trade by HS code classification  │   │
│  │ GET /trade/time-series       - Trade trends over time           │   │
│  │ GET /trade/top-importers     - Top importers ranking            │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ COMPLIANCE ENDPOINTS                                            │   │
│  │ GET /compliance/risk           - Risk scoring for entities       │   │
│  │ GET /compliance/variance      - Revenue variance detection      │   │
│  │ GET /compliance/high-risk     - High-risk entity list           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ METADATA ENDPOINTS                                              │   │
│  │ GET /metadata/ports           - Available ports                 │   │
│  │ GET /metadata/countries      - Available countries              │   │
│  │ GET /metadata/hs-codes       - HS code reference               │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  SECURITY: All endpoints are READ-ONLY, responses are AGGREGATED      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.6 Dashboard Layer (Power BI)
```
┌─────────────────────────────────────────────────────────────────────────┐
│                      DASHBOARD LAYER (Power BI)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ EXECUTIVE DASHBOARDS                                             │   │
│  │ ├── revenue_overview.pbix     - Revenue KPIs and trends          │   │
│  │ └── trade_summary.pbix        - Trade volume overview            │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ OPERATIONS DASHBOARDS                                            │   │
│  │ ├── daily_collections.pbix    - Daily collection tracking       │   │
│  │ └── port_performance.pbix     - Port efficiency metrics          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ COMPLIANCE DASHBOARDS                                            │   │
│  │ ├── revenue_variance.pbix     - Variance analysis               │   │
│  │ └── risk_monitoring.pbix      - Risk indicator tracking         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ⚠️ ALL DASHBOARDS LABELED "SYNTHETIC DATA ONLY"                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Technology Stack

| Layer | Technology | Version/Notes |
|-------|------------|---------------|
| **Database** | PostgreSQL | Primary data store |
| **API Framework** | FastAPI | Python-based REST API |
| **Core Logic** | Python 3.9+ | Tax calculations, aggregations |
| **ETL** | Python Scripts | Data generation & loading |
| **Visualization** | Power BI | Dashboard reports |
| **Orchestration** | Docker Compose | Container management |
| **Documentation** | Markdown | Project documentation |

---

## 5. Data Flow Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  SYNTHETIC  │───▶│    ETL      │───▶│  DATABASE   │───▶│   AGGREGATE │
│  GENERATOR  │    │  PIPELINE   │    │  (PostgreSQL)│    │    LAYER    │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                  │
                                                                  ▼
                                              ┌─────────────────────────────────┐
                                              │         ACCESS LAYER           │
                                              │                                 │
                                              │   ┌───────────┐    ┌─────────┐ │
                                              │   │   API     │    │DASHBOARD│ │
                                              │   │ (GET only)│    │ (View)  │ │
                                              │   └───────────┘    └─────────┘ │
                                              └─────────────────────────────────┘
```

---

## 6. Project Directory Structure

```
customs-revenue-trade/
├── analytics/                    # SQL analytics queries
│   ├── compliance/               # Compliance-focused queries
│   ├── revenue/                  # Revenue analytics queries
│   └── trade/                    # Trade analytics queries
│
├── api/                          # FastAPI application
│   ├── main.py                   # API entry point
│   ├── routes/                   # API endpoint handlers
│   │   ├── compliance.py         # Compliance endpoints
│   │   ├── metadata.py           # Reference data endpoints
│   │   ├── revenue.py            # Revenue endpoints
│   │   └── trade.py              # Trade endpoints
│   ├── schemas/                  # Pydantic request/response models
│   ├── security/                 # Authentication & authorization
│   └── dependencies.py           # API dependencies
│
├── core/                         # Business logic (calculations)
│   ├── common/                   # Shared utilities
│   │   ├── constants.py          # Tax rates, regions
│   │   ├── rounding_rules.py     # Currency rounding
│   │   └── time_utils.py         # Date handling
│   ├── compliance/              # Compliance logic
│   │   ├── risk_scoring.py       # Entity risk scoring
│   │   ├── under_declaration_flags.py
│   │   └── variance_detection.py # Revenue variance detection
│   ├── revenue/                  # Revenue calculations
│   │   ├── duty_calculator.py     # Duty calculation
│   │   ├── excise_calculator.py  # Excise tax calculation
│   │   ├── total_revenue.py      # Total revenue aggregation
│   │   └── vat_calculator.py     # VAT calculation
│   └── trade/                     # Trade aggregation
│       ├── trade_aggregation.py   # Trade data aggregation
│       ├── trend_analysis.py     # Trend analysis
│       └── volume_metrics.py     # Volume calculations
│
├── dashboards/                   # Power BI dashboards
│   ├── compliance/              # Compliance dashboards
│   ├── executive/               # Executive dashboards
│   └── operations/              # Operations dashboards
│
├── database/                     # Database artifacts
│   ├── materialized_views/      # Pre-computed aggregations
│   ├── schema/                  # DDL statements
│   ├── seed/                    # Reference data
│   └── views/                   # Database views
│
├── data/                        # Data storage
│   ├── curated/                 # Processed data
│   │   ├── revenue/
│   │   └── trade_volume/
│   ├── raw/                     # Raw source data
│   │   ├── declarations/        # Declaration files
│   │   ├── exchange_rates/      # Currency rates
│   │   ├── payments/            # Payment records
│   │   └── reference/           # Reference data
│   └── staging/                 # Intermediate data
│       ├── cleaned_declarations/
│       └── validated_payments/
│
├── docs/                        # Documentation
│   ├── SYSTEM_ARCHITECTURE.md   # Detailed architecture
│   ├── calculation_formulas.md # Tax calculation formulas
│   ├── analytics_definitions.md # KPI definitions
│   └── ...                      # Other documentation
│
├── etl/                         # ETL pipelines
│   ├── extract/                 # Data extraction
│   ├── load/                    # Data loading
│   ├── transform/              # Data transformation
│   └── validation/             # Data validation
│
├── governance/                  # Governance policies
│   ├── PROJECT_DECLARATION.md  # Project classification
│   ├── DATA_PRIVACY_POLICY.md  # Privacy rules
│   ├── SYSTEM_FREEZE.md        # Version control
│   └── ...                      # Other policies
│
├── reports/                     # Report templates
│   ├── ad_hoc/                 # Ad-hoc reports
│   ├── annual/                 # Annual reports
│   └── monthly/                # Monthly reports
│
├── scripts/                     # Automation scripts
│   ├── generate_synthetic_data.py  # Data generation
│   ├── init_database.sh        # Database initialization
│   ├── run_etl.sh              # ETL execution
│   └── refresh_materialized_views.sh
│
└── tests/                       # Test suites
    ├── api_tests/              # API tests
    ├── etl_tests/              # ETL tests
    ├── revenue_calculation_tests/
    └── trade_aggregation_tests/
```

---

## 7. Key Design Principles

### 7.1 Privacy-by-Design
- ✅ No PII in schema
- ✅ No real identifiers (DEC-*, IMP-*, PMT-* synthetic format only)
- ✅ No external data connections
- ✅ Minimum threshold: 5 records per aggregation
- ✅ All data is synthetic
- ✅ All access is logged

### 7.2 Safety-by-Design
- ✅ API is READ-ONLY
- ✅ All responses are AGGREGATED only
- ✅ No drill-down to individual records
- ✅ No export capabilities in dashboards

### 7.3 Architecture Boundaries
- ✅ Clear separation of concerns
- ✅ Layered architecture (Governance → Data → Core → API → Dashboard)
- ✅ Stateless API design
- ✅ Pre-aggregated materialized views for performance

---

## 8. API Endpoint Summary

### Revenue Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/revenue/summary` | Overall revenue summary |
| `GET /api/v1/revenue/monthly` | Monthly revenue trends |
| `GET /api/v1/revenue/by-port` | Revenue by port |
| `GET /api/v1/revenue/by-tax-type` | Revenue by tax type |

### Trade Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/trade/summary` | Overall trade summary |
| `GET /api/v1/trade/by-country` | Trade by country |
| `GET /api/v1/trade/by-hs` | Trade by HS code |
| `GET /api/v1/trade/time-series` | Trade trends |
| `GET /api/v1/trade/top-importers` | Top importers |

### Compliance Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/compliance/risk` | Risk scoring |
| `GET /api/v1/compliance/variance` | Revenue variance |
| `GET /api/v1/compliance/high-risk` | High-risk entities |

---

## 9. Governance Artifacts

| Document | Purpose |
|----------|---------|
| `PROJECT_DECLARATION.md` | Project classification and use cases |
| `DATA_PRIVACY_POLICY.md` | Privacy rules and prohibited data types |
| `SYSTEM_FREEZE.md` | Version control and change management |
| `PRIVACY_CERTIFICATION.md` | Privacy compliance certification |
| `APPROVAL_GATE_CHECKLIST.md` | Phase gate approval criteria |

---

## 10. Status & Classification

**Project Status:** ✅ COMPLETE - Version 1.0-FINAL

**Classification:**
- Non-Production System
- 100% Synthetic Data
- Portfolio/Demonstration Purpose
- Privacy-by-Design Certified

**Use Cases:**
- Proof of concept demonstrations
- Analytics methodology testing
- Reporting and dashboard prototyping
- Training and educational purposes
- Technical architecture validation

---

*Document Version: 1.0*  
*Generated: 2026-04-02*  
*Project: Customs Revenue & Trade Volume Prediction Analytics Platform*