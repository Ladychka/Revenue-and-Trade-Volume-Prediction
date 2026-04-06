#!/bin/bash
# ============================================================================
# Database Backup Script
# Phase 13 - Database Operations
# ============================================================================

# Configuration
DB_NAME="${DB_NAME:-customs_analytics}"
DB_USER="${DB_USER:-postgres}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql"

echo "=========================================="
echo "Database Backup - Customs Analytics"
echo "=========================================="

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Check if pg_dump is available
if ! command -v pg_dump &> /dev/null; then
    echo "ERROR: pg_dump not found. Please install PostgreSQL client."
    exit 1
fi

# Perform backup
echo "Starting backup of database: ${DB_NAME}"
echo "Backup file: ${BACKUP_FILE}"

pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -F c -b -v -f "${BACKUP_FILE}" "${DB_NAME}"

if [ $? -eq 0 ]; then
    # Get file size
    FILE_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo ""
    echo "Backup completed successfully!"
    echo "File: ${BACKUP_FILE}"
    echo "Size: ${FILE_SIZE}"
    
    # Create a latest symlink
    ln -sf "${BACKUP_FILE}" "${BACKUP_DIR}/${DB_NAME}_latest.dump"
    echo "Latest backup linked to: ${BACKUP_DIR}/${DB_NAME}_latest.dump"
    
    # Cleanup old backups (keep last 7)
    echo ""
    echo "Cleaning up old backups (keeping last 7)..."
    cd "${BACKUP_DIR}"
    ls -t "${DB_NAME}"_*.sql 2>/dev/null | tail -n +8 | xargs -r rm -f
    ls -t "${DB_NAME}"_*.dump 2>/dev/null | tail -n +8 | xargs -r rm -f
    
    echo "Done!"
else
    echo ""
    echo "ERROR: Backup failed!"
    exit 1
fi