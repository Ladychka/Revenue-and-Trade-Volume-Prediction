# ⚠️ DEMONSTRATION / NON-PRODUCTION SYSTEM

**THIS IS A DEMONSTRATION SYSTEM FOR ANALYTICS PURPOSES ONLY**

This system is designed and intended for:
- Proof of concept demonstrations
- Analytics methodology testing
- Reporting and dashboard prototyping
- Training and educational purposes
- Technical architecture validation

**This system is NOT production-ready and should NOT be used for:**
- Actual customs revenue collection
- Real trade volume monitoring for operational decisions
- Regulatory compliance verification
- Official statistical reporting
- Any operational customs processes

---

# Customs Revenue and Trade Volume Prediction Analytics Platform

## Overview

This project provides a comprehensive analytics platform for customs revenue analysis and trade volume prediction. The system includes ETL pipelines, analytical queries, API endpoints, and visualization dashboards.

## ⚡ Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.9+ (for local development)
- PostgreSQL database

### Setup

```bash
# Initialize the database
bash scripts/init_database.sh

# Run ETL pipelines
bash scripts/run_etl.sh

# Start the API server
python -m api.main
```

### Access Points
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
customs-revenue-trade/
├── analytics/           # SQL analytics queries
├── api/                # REST API endpoints
├── core/               # Business logic (calculations, aggregations)
├── dashboards/         # Power BI dashboard files
├── database/           # Schema, views, materialized views
├── docs/               # Documentation
├── etl/                # Extract, Transform, Load pipelines
├── governance/         # Policies, security, compliance
├── reports/            # Report templates
├── scripts/            # Automation scripts
└── tests/              # Test suites
```

## 🔒 Governance

All governance policies are documented in the [`governance/`](governance/) folder:
- **PROJECT_DECLARATION.md** - Project classification (Analytics-only, Read-only, Non-operational)
- **DATA_PRIVACY_POLICY.md** - Data privacy rules and prohibited data types
- **security_guidelines.md** - Security implementation details
- **data_retention_policy.md** - Data retention rules

## 📊 Key Features

### Revenue Analytics
- Monthly revenue trends
- Revenue by port analysis
- Revenue by tax type breakdown
- Duty, VAT, and excise calculations

### Trade Analytics
- Trade volume by country
- Trade by HS code classification
- Top importers analysis
- Trend analysis and forecasting

### Compliance Monitoring
- Revenue variance detection
- Risk scoring for entities
- Under-declaration flags
- High-risk entity identification

## 🔐 Data Privacy

This system only processes:
- ✅ Synthetic data (generated test data)
- ✅ Anonymized data (PII removed)
- ✅ Aggregated data (grouped summaries)
- ✅ Reference data (public tariff codes, country codes)

This system strictly prohibits:
- ❌ Real personal identifiable information (PII)
- ❌ Actual entity identifiers
- ❌ Real financial transaction details
- ❌ Operational customs data
- ❌ Sensitive business information

See [`governance/DATA_PRIVACY_POLICY.md`](governance/DATA_PRIVACY_POLICY.md) for full details.

## 📝 License

For demonstration purposes only. Not for production use.

---

**Version:** 1.0.0  
**Status:** Phase 0 Complete - Privacy Rules Locked  
**Last Updated:** 2026-03-31