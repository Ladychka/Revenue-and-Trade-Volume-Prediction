#!/usr/bin/env python3
"""
Synthetic Exchange Rate Generator
Generates daily exchange rates for currency conversion
Base currency: KHR (Cambodian Riel)
"""

import csv
import random
from datetime import datetime, timedelta
from typing import Dict, List

# Configuration
DATE_START = datetime(2024, 1, 1)
DATE_END = datetime(2025, 12, 31)

# Base rates (approximate 2024-2025 rates to USD)
# These will be the KHR rates per 1 USD
BASE_RATES_TO_USD = {
    'USD': 1.0,
    'EUR': 0.92,      # 1 EUR ≈ 4100 KHR
    'JPY': 149.50,    # 1 JPY ≈ 6.69 KHR
    'CNY': 7.24,      # 1 CNY ≈ 1380 KHR
    'GBP': 0.79,      # 1 GBP ≈ 5050 KHR
    'THB': 35.50,     # 1 THB ≈ 282 KHR
    'KRW': 1320.00,   # 1 KRW ≈ 0.76 KHR
    'KHR': 4100.00,   # Base currency
}

# Volatility for realistic fluctuation
VOLATILITY = {
    'USD': 0.001,
    'EUR': 0.005,
    'JPY': 0.008,
    'CNY': 0.004,
    'GBP': 0.006,
    'THB': 0.003,
    'KRW': 0.007,
    'KHR': 0.0,
}

def generate_daily_rates(base_rates: Dict[str, float], date: datetime) -> Dict[str, float]:
    """Generate daily rates with slight fluctuations"""
    rates = {}
    for currency, base_rate in base_rates.items():
        if currency == 'KHR':
            rates[currency] = base_rate
        else:
            # Add random fluctuation
            fluctuation = 1 + random.gauss(0, VOLATILITY[currency])
            rates[currency] = round(base_rate * fluctuation, 6)
    return rates

def generate_exchange_rates() -> List[Dict]:
    """Generate exchange rate data"""
    exchange_rates = []
    current_date = DATE_START
    
    # Set seed for reproducibility
    random.seed(42)
    
    while current_date <= DATE_END:
        # Skip weekends for exchange rates (more realistic)
        if current_date.weekday() < 5:
            daily_rates = generate_daily_rates(BASE_RATES_TO_USD, current_date)
            
            # Store rates relative to KHR (base currency)
            for currency, rate in daily_rates.items():
                if currency != 'KHR':
                    exchange_rates.append({
                        'rate_date': current_date.date(),
                        'from_currency': currency,
                        'to_currency': 'KHR',
                        'rate_value': round(rate, 6),
                    })
        
        current_date += timedelta(days=1)
    
    return exchange_rates

def write_csv(data: List[Dict], filename: str):
    """Write data to CSV file"""
    if not data:
        return
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    print("Generating synthetic exchange rates...")
    print(f"  Date Range: {DATE_START.date()} to {DATE_END.date()}")
    print(f"  Base Currency: KHR (Cambodian Riel)")
    
    # Generate exchange rates
    rates = generate_exchange_rates()
    
    # Write to CSV
    print(f"  Writing to data/raw/exchange_rates/exchange_rates.csv...")
    write_csv(rates, 'data/raw/exchange_rates/exchange_rates.csv')
    
    print(f"\n=== Summary ===")
    print(f"  Total Rate Records: {len(rates):,}")
    print(f"  Currencies: {', '.join(BASE_RATES_TO_USD.keys())}")
    print("\nExchange rate generation complete!")
    print("\nNote: These are synthetic rates for demonstration.")
    print("Replace with real MEF API rates when available.")

if __name__ == '__main__':
    main()
