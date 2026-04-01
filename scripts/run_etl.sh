#!/bin/bash
# ============================================================================
# Run ETL Pipeline Script
# Phase 4 - ETL Execution
# ============================================================================

echo "Running ETL pipeline..."

# Generate synthetic data
echo "Step 1: Generating synthetic data..."
python scripts/generate_synthetic_data.py

# Generate exchange rates  
echo "Step 2: Generating exchange rates..."
python scripts/generate_exchange_rates.py

# Load data into database (requires PostgreSQL)
echo "Step 3: Loading data into database..."
# Note: This requires a running PostgreSQL instance
# psql -h localhost -U postgres -d customs_analytics -c "\COPY declarations FROM data/raw/declarations/declarations.csv CSV HEADER"
# psql -h localhost -U postgres -d customs_analytics -c "\COPY declaration_items FROM data/raw/declarations/declaration_items.csv CSV HEADER"
# psql -h localhost -U postgres -d customs_analytics -c "\COPY payments FROM data/raw/payments/payments.csv CSV HEADER"

# Refresh materialized views
echo "Step 4: Refreshing materialized views..."
bash scripts/refresh_materialized_views.sh

echo "ETL pipeline complete!"
