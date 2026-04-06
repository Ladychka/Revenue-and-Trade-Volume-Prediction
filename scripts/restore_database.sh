#!/bin/bash
# ============================================================================
# Database Restore Script
# Phase 13 - Database Operations
# ============================================================================

# Configuration
DB_NAME="${DB_NAME:-customs_analytics}"
DB_USER="${DB_USER:-postgres}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"

echo "=========================================="
echo "Database Restore - Customs Analytics"
echo "=========================================="

# Check if backup file is provided
if [ -z "$1" ]; then
    echo ""
    echo "Usage: $0 <backup_file>"
    echo ""
    echo "Available backups:"
    ls -lh "${BACKUP_DIR}"/*.{sql,dump} 2>/dev/null || echo "  No backups found"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "ERROR: Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

echo "Restore database: ${DB_NAME}"
echo "From backup: ${BACKUP_FILE}"
echo ""
read -p "This will replace all data in the database. Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled."
    exit 0
fi

# Check if psql/pg_restore is available
if command -v pg_restore &> /dev/null; then
    RESTORE_CMD="pg_restore"
elif command -v psql &> /dev/null; then
    RESTORE_CMD="psql"
else
    echo "ERROR: Neither pg_restore nor psql found. Please install PostgreSQL client."
    exit 1
fi

echo "Starting restore..."

if [ "${RESTORE_CMD}" = "pg_restore" ]; then
    # Drop existing connections and restore
    psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_database WHERE datname = '${DB_NAME}';" 2>/dev/null
    pg_restore -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" -c "${BACKUP_FILE}"
else
    # Use psql to restore SQL dump
    psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" -f "${BACKUP_FILE}"
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "Restore completed successfully!"
    echo ""
    echo "Refreshing materialized views..."
    bash scripts/refresh_materialized_views.sh 2>/dev/null || true
else
    echo ""
    echo "ERROR: Restore failed!"
    exit 1
fi