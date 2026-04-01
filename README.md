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
**Status:** Phase 18 Complete - Portfolio Ready  
**Last Updated:** 2026-04-01

---

## Phase 18: Portfolio & Proposal Packaging

This project is designed to be publicly shareable. Here's how to use it:

### Use Contexts

| Context | Description | How to Present |
|---------|-------------|----------------|
| **Academic** | Research on analytics methodology | Focus on technical architecture, data flow |
| **Policy Demo** | Government decision-makers | Use executive materials, scenario walkthroughs |
| **Engineering Portfolio** | Technical job applications | Show code, API design, database schema |

### Sharing Guidelines

When sharing this project:

✅ **DO:**
- Emphasize synthetic data only
- Mention privacy-by-design approach
- Highlight technical achievements
- Provide context about demo-only status

❌ **DO NOT:**
- Claim it's a production system
- Present as operational customs system
- Use real entity names or data
- Imply it processes real tax payments

### Key Selling Points

1. **Privacy-First Design** - 100% synthetic, no PII
2. **Complete Analytics Pipeline** - ETL to visualization
3. **Modern Tech Stack** - FastAPI, PostgreSQL, Power BI
4. **Well Documented** - 18 phases of methodology
5. **Production-Ready Code** - Clean, modular, testable

---

## Quick Reference

| Component | Location |
|-----------|----------|
| Project Declaration | [`governance/PROJECT_DECLARATION.md`](governance/PROJECT_DECLARATION.md) |
| Privacy Policy | [`governance/DATA_PRIVACY_POLICY.md`](governance/DATA_PRIVACY_POLICY.md) |
| Privacy Certification | [`governance/PRIVACY_CERTIFICATION.md`](governance/PRIVACY_CERTIFICATION.md) |
| System Freeze | [`governance/SYSTEM_FREEZE.md`](governance/SYSTEM_FREEZE.md) |
| Architecture | [`docs/SYSTEM_ARCHITECTURE.md`](docs/SYSTEM_ARCHITECTURE.md) |
| Revenue Logic | [`docs/calculation_formulas.md`](docs/calculation_formulas.md) |
| Analytics KPIs | [`docs/analytics_definitions.md`](docs/analytics_definitions.md) |
| Executive Materials | [`docs/executive_materials.md`](docs/executive_materials.md) |
| Scenarios | [`docs/scenario_walkthroughs.md`](docs/scenario_walkthroughs.md) |