#!/usr/bin/env python3
"""
Synthetic Data Generator for Customs Revenue Analytics
Phase 4 - Data Loading
Generates synthetic declarations, items, and payments
"""

# Note: we use random (not secrets) for synthetic IDs to ensure
# full reproducibility via random.seed(42)
import random
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

# Configuration
NUM_DECLARATIONS = 50000
ITEMS_PER_DECLARATION_MIN = 1
ITEMS_PER_DECLARATION_MAX = 5
DATE_START = datetime(2024, 1, 1)
DATE_END = datetime(2025, 12, 31)

# Synthetic ID Generators
def generate_declaration_id(date: datetime) -> str:
    """Generate synthetic declaration ID: DEC-YYYYMMDD-XXXXXXX"""
    date_str = date.strftime("%Y%m%d")
    seq = random.randint(1000000, 9999999)
    return f"DEC-{date_str}-{seq}"

def generate_importer_id() -> str:
    """Generate synthetic importer ID: IMP-XXXXX-XXXXXXX"""
    region = random.randint(10000, 99999)
    entity = random.randint(1000000, 9999999)
    return f"IMP-{region}-{entity}"

def generate_payment_id(date: datetime) -> str:
    """Generate synthetic payment ID: PMT-YYYYMMDD-XXXXXXXX"""
    date_str = date.strftime("%Y%m%d")
    ref = random.randint(10000000, 99999999)
    return f"PMT-{date_str}-{ref}"

# HS Codes from reference data
HS_CODES = [
    ('8471300000', 0.0000, 0.1700, False),
    ('8517120000', 0.0000, 0.1700, False),
    ('8703235010', 0.2500, 0.1700, False),
    ('6204620000', 0.1675, 0.0700, False),
    ('6203420000', 0.1675, 0.0700, False),
    ('3002150000', 0.0000, 0.0000, False),
    ('3004900000', 0.0000, 0.0000, False),
    ('3926900000', 0.0650, 0.1700, False),
    ('9403610000', 0.0000, 0.1700, False),
    ('8541400000', 0.0000, 0.1700, False),
]

# Countries with distribution weights
COUNTRIES = [
    ('CN', 0.35), ('JP', 0.15), ('US', 0.12), ('KR', 0.10),
    ('TH', 0.08), ('ID', 0.05), ('MY', 0.05), ('AU', 0.03),
    ('DE', 0.02), ('SG', 0.02), ('VN', 0.02), ('TW', 0.01),
]

# Ports with weights
PORTS = [
    ('PORT001', 0.20), ('PORT002', 0.18), ('PORT003', 0.15),
    ('PORT004', 0.12), ('PORT005', 0.10), ('PORT006', 0.08),
    ('PORT007', 0.06), ('PORT008', 0.05), ('PORT009', 0.04), ('PORT010', 0.02),
]

# Status distribution
STATUSES = [
    ('CLEARED', 0.85), ('PROCESSED', 0.10), ('LODGED', 0.04), ('REJECTED', 0.01),
]

# Currencies (original declaration currency)
CURRENCIES = ['USD', 'EUR', 'JPY', 'CNY', 'GBP', 'THB', 'KRW']

def weighted_choice(choices: List[Tuple]) -> str:
    """Select weighted random choice"""
    items, weights = zip(*choices)
    return random.choices(items, weights=weights, k=1)[0]

def generate_customs_value() -> float:
    """Generate customs value using log-normal distribution"""
    return round(random.lognormvariate(10, 1.5), 2)

def generate_quantity(hs_code: str) -> Tuple[float, str]:
    """Generate quantity based on HS code chapter"""
    chapter = hs_code[:2]
    if chapter in ['28', '29', '30', '31', '32']:  # Chemicals
        return round(random.uniform(10, 5000), 3), 'KGM'
    elif chapter in ['84', '85']:  # Machinery/Electronics
        return round(random.uniform(1, 100), 3), 'PCE'
    elif chapter in ['62', '63']:  # Textiles
        return round(random.uniform(10, 500), 3), 'KGM'
    elif chapter in ['87']:  # Vehicles
        return round(random.uniform(1, 10), 3), 'PCE'
    else:
        return round(random.uniform(1, 1000), 3), 'KGM'

def calculate_taxes(customs_value: float, duty_rate: float, vat_rate: float, 
                   excise_applicable: bool = False) -> Tuple[float, float, float]:
    """Calculate customs duty, VAT, and optionally excise"""
    customs_duty = round(customs_value * duty_rate, 2)
    vat_base = customs_value + customs_duty
    vat_amount = round(vat_base * vat_rate, 2)
    excise_amount = 0.0
    return customs_duty, vat_amount, excise_amount

def generate_declarations() -> List[Dict]:
    """Generate synthetic declarations"""
    declarations = []
    current_date = DATE_START
    declarations_per_day = NUM_DECLARATIONS // ((DATE_END - DATE_START).days)
    
    for i in range(NUM_DECLARATIONS):
        # Distribute over date range
        days_offset = i // declarations_per_day
        current_date = DATE_START + timedelta(days=min(days_offset, 729))
        
        # Skip weekends for more realistic distribution
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)
        
        # Generate declaration
        declaration = {
            'declaration_id': generate_declaration_id(current_date),
            'declaration_date': current_date.date(),
            'declaration_type': 'IMPORT',
            'status': weighted_choice(STATUSES),
            'declarant_id': generate_importer_id(),
            'office_code': weighted_choice(PORTS),
            'currency_code': random.choice(CURRENCIES),
            'total_items': 0,
            'total_customs_value': 0.0,
            'total_customs_duty': 0.0,
            'total_excise': 0.0,
            'total_vat': 0.0,
            'total_tax_liability': 0.0,
        }
        declarations.append(declaration)
    
    return declarations

def generate_items(declarations: List[Dict]) -> List[Dict]:
    """Generate declaration items"""
    items = []
    
    for declaration in declarations:
        num_items = random.randint(ITEMS_PER_DECLARATION_MIN, ITEMS_PER_DECLARATION_MAX)
        
        for seq in range(1, num_items + 1):
            # Select HS code
            hs_code, base_duty_rate, base_vat_rate, excise_app = random.choice(HS_CODES)
            
            # Generate values
            customs_value = generate_customs_value()
            quantity, unit = generate_quantity(hs_code)
            
            # Apply preferential treatment occasionally
            preferential = random.random() < 0.15
            duty_rate = base_duty_rate * 0.5 if preferential else base_duty_rate
            origin_country = weighted_choice(COUNTRIES)
            
            # Calculate taxes
            customs_duty, vat_amount, excise_amount = calculate_taxes(
                customs_value, duty_rate, base_vat_rate, excise_app
            )
            
            # Generate item
            item = {
                'item_id': f"ITM-{declaration['declaration_date'].strftime('%Y%m%d')}-{declaration['declaration_id'].split('-')[2]}-{seq:03d}",
                'declaration_id': declaration['declaration_id'],
                'item_sequence': seq,
                'hs_code': hs_code,
                'goods_description': f"Synthetic product - HS {hs_code}",
                'origin_country': origin_country,
                'quantity': quantity,
                'quantity_unit': unit,
                'statistical_quantity': quantity,
                'customs_value': customs_value,
                'duty_rate': duty_rate,
                'customs_duty': customs_duty,
                'excise_applicable': excise_app,
                'excise_type': None,
                'excise_rate': 0.0,
                'excise_amount': excise_amount,
                'vat_rate': base_vat_rate,
                'vat_amount': vat_amount,
                'preferential_indicator': preferential,
                'preferential_rate': base_duty_rate * 0.5 if preferential else 0.0,
                'preferential_country': origin_country if preferential else None,
            }
            items.append(item)
            
            # Update declaration totals
            declaration['total_items'] += 1
            declaration['total_customs_value'] += customs_value
            declaration['total_customs_duty'] += customs_duty
            declaration['total_excise'] += excise_amount
            declaration['total_vat'] += vat_amount
    
    # Calculate total tax liability
    for declaration in declarations:
        declaration['total_tax_liability'] = (
            declaration['total_customs_duty'] + 
            declaration['total_excise'] + 
            declaration['total_vat']
        )
    
    return items

def generate_payments(declarations: List[Dict]) -> List[Dict]:
    """Generate synthetic payments"""
    payments = []
    
    for declaration in declarations:
        # Payment date within 7 days of declaration
        days_offset = random.randint(0, 7)
        payment_date = declaration['declaration_date'] + timedelta(days=days_offset)
        
        payment = {
            'payment_id': generate_payment_id(payment_date),
            'declaration_id': declaration['declaration_id'],
            'payment_date': payment_date,
            'payment_amount': declaration['total_tax_liability'],
            'payment_method': random.choice(['WIRE', 'CASH', 'CARD']),
            'currency_code': declaration['currency_code'],
            'exchange_rate': 1.0,
            'bank_reference': f"BK{random.randint(0, 999999):06d}",
            'batch_reference': f"BT{random.randint(0, 999999):06d}",
            'payment_status': 'COMPLETED' if declaration['status'] == 'CLEARED' else 'PENDING',
        }
        payments.append(payment)
    
    return payments

def write_csv(data: List[Dict], filename: str):
    """Write data to CSV file"""
    if not data:
        return
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    print("Generating synthetic data...")
    print(f"  Declarations: {NUM_DECLARATIONS}")
    
    # Set random seed for reproducibility (optional)
    random.seed(42)
    
    # Generate data
    print("  Generating declarations...")
    declarations = generate_declarations()
    
    print("  Generating declaration items...")
    items = generate_items(declarations)
    
    print("  Generating payments...")
    payments = generate_payments(declarations)
    
    # Write to CSV files
    print("  Writing declaration data...")
    write_csv(declarations, 'data/raw/declarations/declarations.csv')
    
    print("  Writing item data...")
    write_csv(items, 'data/raw/declarations/declaration_items.csv')
    
    print("  Writing payment data...")
    write_csv(payments, 'data/raw/payments/payments.csv')
    
    # Summary
    total_value = sum(d['total_customs_value'] for d in declarations)
    total_duty = sum(d['total_customs_duty'] for d in declarations)
    total_vat = sum(d['total_vat'] for d in declarations)
    
    print("\n=== Summary ===")
    print(f"  Declarations: {len(declarations):,}")
    print(f"  Items: {len(items):,}")
    print(f"  Payments: {len(payments):,}")
    print(f"  Total Customs Value: ${total_value:,.2f}")
    print(f"  Total Customs Duty: ${total_duty:,.2f}")
    print(f"  Total VAT: ${total_vat:,.2f}")
    print("\nData generation complete!")

if __name__ == '__main__':
    main()