#!/usr/bin/env python3
"""
ETL Transform - Currency Conversion
Phase 4 - Data Transformation
Converts declaration values to base currency (USD) using exchange rates
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Tuple


def load_exchange_rates(csv_path: str) -> Dict[Tuple[str, str], float]:
    """Load exchange rates into a lookup dictionary"""
    rates = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['exchange_date']
            currency = row['currency_code']
            rate = float(row['rate_to_usd'])
            rates[(date, currency)] = rate
    return rates


def convert_currency(amount: float, from_currency: str, date: str, 
                     rates: Dict[Tuple[str, str], float]) -> Tuple[float, float]:
    """
    Convert amount from source currency to USD
    Returns (converted_amount, exchange_rate_used)
    """
    if from_currency == 'USD':
        return amount, 1.0
    
    # Try to find rate for the exact date
    key = (date, from_currency)
    if key in rates:
        rate = rates[key]
        return amount / rate, rate
    
    # Fallback: try to find any rate for that currency (approximate)
    for (d, c), r in rates.items():
        if c == from_currency:
            return amount / r, r
    
    # No rate found - return original with warning
    return amount, 0.0


def convert_declarations(declarations_path: str, exchange_rates_path: str, 
                         output_dir: str) -> Dict:
    """Convert declaration values to base currency"""
    print(f"Converting declarations from: {declarations_path}")
    
    # Load exchange rates
    print(f"  Loading exchange rates from: {exchange_rates_path}")
    rates = load_exchange_rates(exchange_rates_path)
    print(f"  Loaded {len(rates)} exchange rates")
    
    # Load declarations
    declarations = []
    with open(declarations_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            declarations.append(row)
    print(f"  Loaded {len(declarations)} declarations")
    
    # Convert currencies
    converted_declarations = []
    no_rate_count = 0
    
    for decl in declarations:
        converted = decl.copy()
        date = decl.get('declaration_date', '')
        currency = decl.get('currency_code', 'USD')
        
        # Convert each monetary field
        fields_to_convert = [
            'total_customs_value', 'total_customs_duty', 
            'total_excise', 'total_vat', 'total_tax_liability'
        ]
        
        for field in fields_to_convert:
            value = float(decl.get(field, 0) or 0)
            converted_value, rate = convert_currency(value, currency, date, rates)
            
            if rate == 0:
                no_rate_count += 1
            
            converted[f'{field}_usd'] = round(converted_value, 2)
            converted[f'{field}_exchange_rate'] = rate
        
        converted_declarations.append(converted)
    
    # Write converted data to staging
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'converted_declarations.csv')
    
    if converted_declarations:
        # Add USD columns to header
        fieldnames = list(converted_declarations[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(converted_declarations)
        
        print(f"  Written {len(converted_declarations)} converted declarations to: {output_path}")
    
    print(f"\n  Conversion Results:")
    print(f"    Total: {len(converted_declarations)}")
    print(f"    Missing exchange rates: {no_rate_count}")
    
    return {'total': len(converted_declarations), 'missing_rates': no_rate_count}


def main():
    """Main transformation function"""
    declarations_path = 'data/raw/declarations/declarations.csv'
    exchange_rates_path = 'data/raw/exchange_rates/exchange_rates.csv'
    output_dir = 'data/staging/cleaned_declarations'
    
    if not os.path.exists(declarations_path):
        print(f"ERROR: Declarations file not found: {declarations_path}")
        return
    
    if not os.path.exists(exchange_rates_path):
        print(f"ERROR: Exchange rates file not found: {exchange_rates_path}")
        return
    
    results = convert_declarations(declarations_path, exchange_rates_path, output_dir)


if __name__ == '__main__':
    main()