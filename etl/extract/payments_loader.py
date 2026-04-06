#!/usr/bin/env python3
"""
ETL Extract - Payments Data Loader
Phase 4 - Data Extraction
Loads payments from CSV into database
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


def load_payments_from_csv(csv_path: str) -> list:
    """Load payments from CSV file"""
    payments = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            payments.append({
                'payment_id': row['payment_id'],
                'declaration_id': row['declaration_id'],
                'payment_date': datetime.strptime(row['payment_date'], '%Y-%m-%d').date(),
                'payment_amount': float(row['payment_amount']),
                'payment_method': row['payment_method'],
                'currency_code': row['currency_code'],
                'exchange_rate': float(row['exchange_rate']),
                'bank_reference': row['bank_reference'],
                'batch_reference': row['batch_reference'],
                'payment_status': row['payment_status'],
            })
    return payments


def insert_payments(conn, payments: list):
    """Insert payments into database"""
    sql = """
        INSERT INTO payments (
            payment_id, declaration_id, payment_date, payment_amount,
            payment_method, currency_code, exchange_rate, bank_reference,
            batch_reference, payment_status
        ) VALUES (
            %(payment_id)s, %(declaration_id)s, %(payment_date)s, %(payment_amount)s,
            %(payment_method)s, %(currency_code)s, %(exchange_rate)s, %(bank_reference)s,
            %(batch_reference)s, %(payment_status)s
        )
        ON CONFLICT (payment_id) DO UPDATE SET
            payment_amount = EXCLUDED.payment_amount,
            payment_status = EXCLUDED.payment_status,
            payment_date = EXCLUDED.payment_date
    """
    
    execute_batch(conn, sql, payments, page_size=1000)
    conn.commit()
    print(f"  Loaded {len(payments)} payments")


def main():
    """Main loader function"""
    print("Loading payments data...")
    
    csv_path = 'data/raw/payments/payments.csv'
    if not os.path.exists(csv_path):
        print(f"  ERROR: File not found: {csv_path}")
        return
    
    payments = load_payments_from_csv(csv_path)
    print(f"  Found {len(payments)} records in CSV")
    
    try:
        conn = get_db_connection()
        insert_payments(conn, payments)
        conn.close()
        print("  Payments loaded successfully!")
    except Exception as e:
        print(f"  ERROR: {e}")


if __name__ == '__main__':
    main()