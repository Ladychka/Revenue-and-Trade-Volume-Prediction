#!/usr/bin/env python3
"""
ETL Transform - Normalize HS Codes
Phase 4 - Data Transformation
Validates and normalizes HS codes to standard format
"""

import csv
import os
import re
from typing import List, Dict, Tuple


def load_hs_reference(csv_path: str) -> Dict[str, Dict]:
    """Load HS code reference data"""
    reference = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hs_code = row['hs_code']
            reference[hs_code] = row
    return reference


def normalize_hs_code(hs_code: str) -> Tuple[str, bool]:
    """
    Normalize HS code to standard format (8-digit)
    Returns (normalized_code, is_valid)
    """
    if not hs_code:
        return '', False
    
    # Remove any whitespace and dashes
    hs_code = hs_code.strip().replace('-', '').replace(' ', '')
    
    # HS codes should be 4, 6, or 8 digits
    if not re.match(r'^\d+$', hs_code):
        return '', False
    
    # Pad to 8 digits with zeros
    if len(hs_code) <= 4:
        normalized = hs_code.ljust(8, '0')
    elif len(hs_code) <= 6:
        normalized = hs_code.ljust(8, '0')
    else:
        normalized = hs_code[:8]
    
    return normalized, True


def validate_hs_code(hs_code: str, reference: Dict[str, Dict]) -> Tuple[bool, str]:
    """
    Validate HS code against reference data
    Returns (is_valid, message)
    """
    if not hs_code:
        return False, "Empty HS code"
    
    # Check if exists in reference (exact match)
    if hs_code in reference:
        return True, "Valid"
    
    # Check if prefix exists in reference
    for ref_code in reference.keys():
        if hs_code.startswith(ref_code[:4]):
            return True, f"Valid prefix match with {ref_code}"
    
    return False, "HS code not found in reference"


def normalize_declaration_items(input_path: str, reference_path: str, 
                                 output_dir: str) -> Dict:
    """Normalize HS codes in declaration items"""
    print(f"Normalizing declaration items from: {input_path}")
    
    # Load HS reference
    print(f"  Loading HS reference from: {reference_path}")
    reference = load_hs_reference(reference_path)
    print(f"  Loaded {len(reference)} HS code definitions")
    
    # Load declaration items
    items = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)
    print(f"  Loaded {len(items)} declaration items")
    
    # Normalize HS codes
    normalized_items = []
    stats = {
        'total': len(items),
        'valid': 0,
        'invalid': 0,
        'normalized': 0
    }
    
    for item in items:
        normalized = item.copy()
        original_hs = item.get('hs_code', '')
        
        # Normalize
        normalized_hs, normalized_success = normalize_hs_code(original_hs)
        
        if normalized_success and normalized_hs != original_hs:
            stats['normalized'] += 1
            normalized['hs_code_normalized'] = normalized_hs
        else:
            normalized['hs_code_normalized'] = original_hs
        
        # Validate against reference
        is_valid, message = validate_hs_code(normalized_hs, reference)
        
        normalized['hs_code_valid'] = is_valid
        normalized['hs_code_validation_message'] = message
        
        if is_valid:
            stats['valid'] += 1
        else:
            stats['invalid'] += 1
        
        normalized_items.append(normalized)
    
    # Write normalized data to staging
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'normalized_items.csv')
    
    if normalized_items:
        fieldnames = list(normalized_items[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(normalized_items)
        
        print(f"  Written {len(normalized_items)} normalized items to: {output_path}")
    
    print(f"\n  Normalization Results:")
    print(f"    Total items: {stats['total']}")
    print(f"    Valid: {stats['valid']}")
    print(f"    Invalid: {stats['invalid']}")
    print(f"    Normalized (padded): {stats['normalized']}")
    
    return stats


def main():
    """Main transformation function"""
    input_path = 'data/raw/declarations/declaration_items.csv'
    reference_path = 'database/seed/hs_codes.csv'  # Adjust based on actual reference file
    output_dir = 'data/staging/cleaned_declarations'
    
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}")
        # Try alternative path
        print("  Checking for HS code reference in seed data...")
        return
    
    # Look for HS code reference in database seed
    seed_files = os.listdir('database/seed')
    hs_ref_file = None
    for f in seed_files:
        if 'hs' in f.lower() or 'tariff' in f.lower():
            hs_ref_file = f'database/seed/{f}'
            break
    
    if hs_ref_file:
        reference_path = hs_ref_file
    else:
        print("  WARNING: No HS code reference file found, skipping validation")
        reference_path = None
    
    if reference_path and os.path.exists(reference_path):
        results = normalize_declaration_items(input_path, reference_path, output_dir)
    else:
        print("  Skipping normalization - no reference file")


if __name__ == '__main__':
    main()