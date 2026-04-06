#!/usr/bin/env python3
"""
ETL Load - Load Reference Tables
Phase 4 - Data Loading
Loads reference data from database seed files
"""

import psycopg2
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


def load_reference_data_sql(conn):
    """Load reference data from SQL seed file"""
    seed_file = 'database/seed/reference_data.sql'
    
    if not os.path.exists(seed_file):
        print(f"  ERROR: Seed file not found: {seed_file}")
        return False
    
    with open(seed_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Split into individual statements
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    
    cursor = conn.cursor()
    for i, statement in enumerate(statements):
        if statement:
            try:
                cursor.execute(statement)
                if (i + 1) % 100 == 0:
                    print(f"    Processed {i + 1} statements...")
            except Exception as e:
                print(f"  Warning: Statement {i + 1} failed: {e}")
    
    conn.commit()
    cursor.close()
    return True


def verify_reference_tables(conn):
    """Verify reference tables have data"""
    tables = [
        'hs_code_reference',
        'port_reference', 
        'country_reference',
        'currency_reference',
        'trader_reference'
    ]
    
    cursor = conn.cursor()
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count:,} records")
    cursor.close()


def main():
    """Main load function"""
    print("Loading reference tables...")
    
    try:
        conn = get_db_connection()
        
        print("  Loading reference data from seed file...")
        success = load_reference_data_sql(conn)
        
        if success:
            print("\n  Verifying reference tables...")
            verify_reference_tables(conn)
        
        conn.close()
        print("\n  Reference tables loaded successfully!")
    except Exception as e:
        print(f"  ERROR: {e}")


if __name__ == '__main__':
    main()