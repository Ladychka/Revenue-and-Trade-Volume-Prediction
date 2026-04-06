#!/usr/bin/env python3
"""
ETL Extract - Declarations Data Loader
Phase 4 - Data Extraction
Loads declarations from CSV into database
"""

import csv
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
import os


def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'customs_analytics'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )


def load_declarations_from_csv(csv_path: str) -> list:
    """Load declarations from CSV file"""
    declarations = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            declarations.append({
                'declaration_id': row['declaration_id'],
                'declaration_date': datetime.strptime(row['declaration_date'], '%Y-%m-%d').date(),
                'declaration_type': row['declaration_type'],
                'status': row['status'],
                'declarant_id': row['declarant_id'],
                'office_code': row['office_code'],
                'currency_code': row['currency_code'],
                'total_items': int(row['total_items']),
                'total_customs_value': float(row['total_customs_value']),
                'total_customs_duty': float(row['total_customs_duty']),
                'total_excise': float(row['total_excise']),
                'total_vat': float(row['total_vat']),
                'total_tax_liability': float(row['total_tax_liability']),
            })
    return declarations


def insert_declarations(conn, declarations: list):
    """Insert declarations into database"""
    sql = """
        INSERT INTO declarations (
            declaration_id, declaration_date, declaration_type, status,
            declarant_id, office_code, currency_code, total_items,
            total_customs_value, total_customs_duty, total_excise,
            total_vat, total_tax_liability
        ) VALUES (
            %(declaration_id)s, %(declaration_date)s, %(declaration_type)s, %(status)s,
            %(declarant_id)s, %(office_code)s, %(currency_code)s, %(total_items)s,
            %(total_customs_value)s, %(total_customs_duty)s, %(total_excise)s,
            %(total_vat)s, %(total_tax_liability)s
        )
        ON CONFLICT (declaration_id) DO UPDATE SET
            status = EXCLUDED.status,
            total_items = EXCLUDED.total_items,
            total_customs_value = EXCLUDED.total_customs_value,
            total_customs_duty = EXCLUDED.total_customs_duty,
            total_excise = EXCLUDED.total_excise,
            total_vat = EXCLUDED.total_vat,
            total_tax_liability = EXCLUDED.total_tax_liability
    """
    
    execute_batch(conn, sql, declarations, page_size=1000)
    conn.commit()
    print(f"  Loaded {len(declarations)} declarations")


def main():
    """Main loader function"""
    print("Loading declarations data...")
    
    csv_path = 'data/raw/declarations/declarations.csv'
    if not os.path.exists(csv_path):
        print(f"  ERROR: File not found: {csv_path}")
        return
    
    declarations = load_declarations_from_csv(csv_path)
    print(f"  Found {len(declarations)} records in CSV")
    
    try:
        conn = get_db_connection()
        insert_declarations(conn, declarations)
        conn.close()
        print("  Declarations loaded successfully!")
    except Exception as e:
        print(f"  ERROR: {e}")


if __name__ == '__main__':
    main()