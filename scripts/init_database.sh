#!/bin/bash
# ============================================================================
# Initialize Database Script
# Phase 4 - Database Setup
# ============================================================================

echo "Initializing Customs Analytics Database..."

# Run schema scripts in order
echo "Creating schema..."
psql -h localhost -U postgres -d customs_analytics -f database/schema/001_core_tables.sql
psql -h localhost -U postgres -d customs_analytics -f database/schema/002_reference_tables.sql
psql -h localhost -U postgres -d customs_analytics -f database/schema/003_constraints.sql

# Load reference data
echo "Loading reference data..."
psql -h localhost -U postgres -d customs_analytics -f database/seed/reference_data.sql

# Create views
echo "Creating views..."
psql -h localhost -U postgres -d customs_analytics -f database/views/revenue_views.sql
psql -h localhost -U postgres -d customs_analytics -f database/views/trade_views.sql
psql -h localhost -U postgres -d customs_analytics -f database/views/compliance_views.sql

# Create materialized views
echo "Creating materialized views..."
psql -h localhost -U postgres -d customs_analytics -f database/materialized_views/mv_monthly_revenue.sql
psql -h localhost -U postgres -d customs_analytics -f database/materialized_views/mv_trade_by_country.sql
psql -h localhost -U postgres -d customs_analytics -f database/materialized_views/mv_trade_by_hs.sql

echo "Database initialization complete!"
