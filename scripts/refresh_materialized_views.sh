#!/bin/bash
# ============================================================================
# Phase 7: Materialized View Refresh Script
# Purpose: Refresh analytics materialized views on schedule
# Schedule: Daily at 2:00 AM UTC
# ============================================================================

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-customs_analytics}"
DB_USER="${DB_USER:-etl_user}"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Error handler
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Check database connectivity
check_db() {
    log "Checking database connectivity..."
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        error_exit "Cannot connect to database"
    fi
    log "Database connection OK"
}

# Refresh materialized views with concurrency support
refresh_views() {
    log "Starting materialized view refresh..."
    
    # Monthly revenue
    log "Refreshing mv_monthly_revenue..."
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
        REFRESH MATERIALIZED VIEW CONCURRENTLY mv_monthly_revenue;
EOF
    if [ $? -ne 0 ]; then
        log "WARNING: mv_monthly_revenue refresh failed, retrying without concurrency..."
        PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
            REFRESH MATERIALIZED VIEW mv_monthly_revenue;
EOF
    fi
    
    # Trade by country
    log "Refreshing mv_trade_by_country..."
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
        REFRESH MATERIALIZED VIEW CONCURRENTLY mv_trade_by_country;
EOF
    if [ $? -ne 0 ]; then
        log "WARNING: mv_trade_by_country refresh failed, retrying without concurrency..."
        PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
            REFRESH MATERIALIZED VIEW mv_trade_by_country;
EOF
    fi
    
    # Trade by HS
    log "Refreshing mv_trade_by_hs..."
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
        REFRESH MATERIALIZED VIEW CONCURRENTLY mv_trade_by_hs;
EOF
    if [ $? -ne 0 ]; then
        log "WARNING: mv_trade_by_hs refresh failed, retrying without concurrency..."
        PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
            REFRESH MATERIALIZED VIEW mv_trade_by_hs;
EOF
    fi
    
    log "Materialized view refresh complete"
}

# Log refresh timestamps
log_timestamps() {
    log "Recording refresh timestamps..."
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
        INSERT INTO audit_log (event_type, event_time, details)
        VALUES ('MV_REFRESH', NOW(), 'Materialized views refreshed');
EOF
}

# Main execution
main() {
    log "=== Materialized View Refresh Job Started ==="
    
    check_db
    refresh_views
    log_timestamps
    
    log "=== Materialized View Refresh Job Completed ==="
}

main "$@"