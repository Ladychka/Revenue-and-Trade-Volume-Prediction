#!/usr/bin/env python3
"""
ETL Extract - Exchange Rates Data Loader
Phase 4 - Data Extraction
Loads exchange rates from CSV into database
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


def load_exchange_rates_from_csv(csv_path: str) -> list:
    """Load exchange rates from CSV file"""
    rates = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rates.append({
                'exchange_date': datetime.strptime(row['exchange_date'], '%Y-%m-%d').date(),
                'currency_code': row['currency_code'],
                'rate_to_usd': float(row['rate_to_usd']),
            })
    return rates


def insert_exchange_rates(conn, rates: list):
    """Insert exchange rates into database"""
    sql = """
        INSERT INTO exchange_rates (
            exchange_date, currency_code, rate_to_usd
        ) VALUES (
            %(exchange_date)s, %(currency_code)s, %(rate_to_usd)s
        )
        ON CONFLICT (exchange_date, currency_code) DO UPDATE SET
            rate_to_usd = EXCLUDED.rate_to_usd
    """
    
    execute_batch(conn, sql, rates, page_size=1000)
    conn.commit()
    print(f"  Loaded {len(rates)} exchange rates")


def main():
    """Main loader function"""
    print("Loading exchange rates data...")
    
    csv_path = 'data/raw/exchange_rates/exchange_rates.csv'
    if not os.path.exists(csv_path):
        print(f"  ERROR: File not found: {csv_path}")
        return
    
    rates = load_exchange_rates_from_csv(csv_path)
    print(f"  Found {len(rates)} records in CSV")
    
    try:
        conn = get_db_connection()
        insert_exchange_rates(conn, rates)
        conn.close()
        print("  Exchange rates loaded successfully!")
    except Exception as e:
        print(f"  ERROR: {e}")


if __name__ == '__main__':
    main()