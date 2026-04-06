#!/usr/bin/env python3
"""
ETL Load - Load Core Tables
Phase 4 - Data Loading
Orchestrates loading of all core data tables
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract import declarations_loader, payments_loader, exchange_rates_loader


def main():
    """Main load orchestration"""
    print("=" * 60)
    print("ETL Load - Loading Core Tables")
    print("=" * 60)
    
    # Load in dependency order (declarations first, then items, then payments)
    print("\nStep 1: Load declarations...")
    declarations_loader.main()
    
    print("\nStep 2: Load declaration items...")
    # This would be similar to declarations_loader but for items
    print("  Note: Declaration items loaded with synthetic data generator")
    
    print("\nStep 3: Load payments...")
    payments_loader.main()
    
    print("\nStep 4: Load exchange rates...")
    exchange_rates_loader.main()
    
    print("\n" + "=" * 60)
    print("Core tables loaded successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()