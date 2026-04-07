# Customs Revenue & Trade Analytics System (Version 2)

## Project Overview
This repository contains Version 2 of the Customs Analytics Platform. V2 focuses on robust deterministic forecasting (SARIMA, Holt-Winters), granular declarative scenario simulation ("What-if" analysis), and reliable tracking of excise revenue gaps natively, using SQLAlchemy and a React frontend.

## 🛑 Governance Boundaries (Non-Negotiable)

1. **Complete Isolation from V1**: This project is architecturally and operationally distinct from Version 1. Do NOT import, reference, or cross-pollinate files from the V1 repository.
2. **Analytics & Aggregate Scope Only**: This platform is explicitly designed for aggregated insights and synthetic models. **No real, operational, or PII-laden customs records are to be loaded into this environment.**
3. **Deterministic Math**: Scenario engines and forecasting models must be cleanly explainable. All algorithms must be seeded and reproducible.

## Development Environment
- **Python**: >= 3.11
- **Database**: PostgreSQL 16
- **Frontend**: Node.js >= 20, React + Vite

## Repository Structure
- `/backend`: Core Python FastAPI server, SQLALchemy Data Layer, and Forecasting Engine.
- `/frontend`: React/Vite dashboard.
- `/scripts`: Synthetic data generation and database seeding utilities.

## General Assumptions & Operating Limitations
> **Disclaimer:** This system is formulated under strict determinism requirements. As a result, the following assumptions are permanently enforced:
> - **Synthetic Seed Only:** Standard statutory rates (e.g. 35% Alcohol Excise) are hardcoded for modeling baselines. Real-world tax tables are volatile and must not substitute these in V2.
> - **Inclusive Customs Value:** Our scenario engine assumes the `customs_value` in the aggregation pipeline already accounts for levied duties when calculating subsequent ad valorem excise taxes.
> - **Zero Latency Forecasting:** We do not compute `SARIMA` daily. Models are designed to run on the 1st of every month. Any simulation delta is executed procedurally over the pre-cached statistical forecast array.
