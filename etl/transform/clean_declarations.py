#!/usr/bin/env python3
"""
ETL Transform - Clean Declarations
Phase 4 - Data Transformation
Cleans and validates declaration data
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Tuple


def load_declarations(csv_path: str) -> List[Dict]:
    """Load declarations from CSV"""
    declarations = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            declarations.append(row)
    return declarations


def validate_declaration(declaration: Dict) -> Tuple[bool, List[str]]:
    """Validate a single declaration"""
    errors = []
    
    # Check required fields
    if not declaration.get('declaration_id'):
        errors.append("Missing declaration_id")
    
    if not declaration.get('declaration_date'):
        errors.append("Missing declaration_date")
    else:
        # Validate date format
        try:
            datetime.strptime(declaration['declaration_date'], '%Y-%m-%d')
        except ValueError:
            errors.append(f"Invalid date format: {declaration['declaration_date']}")
    
    # Validate numeric fields
    numeric_fields = ['total_items', 'total_customs_value', 'total_customs_duty', 
                      'total_excise', 'total_vat', 'total_tax_liability']
    
    for field in numeric_fields:
        value = declaration.get(field)
        if value is None or value == '':
            errors.append(f"Missing {field}")
        else:
            try:
                float(value)
            except ValueError:
                errors.append(f"Invalid numeric value for {field}: {value}")
    
    # Validate status
    valid_statuses = ['CLEARED', 'PROCESSED', 'LODGED', 'REJECTED']
    if declaration.get('status') not in valid_statuses:
        errors.append(f"Invalid status: {declaration.get('status')}")
    
    return len(errors) == 0, errors


def clean_declaration(declaration: Dict) -> Dict:
    """Clean and normalize a declaration"""
    cleaned = declaration.copy()
    
    # Trim whitespace from string fields
    string_fields = ['declaration_id', 'declaration_type', 'status', 
                     'declarant_id', 'office_code', 'currency_code']
    
    for field in string_fields:
        if field in cleaned and cleaned[field]:
            cleaned[field] = cleaned[field].strip()
    
    # Normalize status
    if cleaned.get('status'):
        cleaned['status'] = cleaned['status'].upper().strip()
    
    # Convert numeric fields
    numeric_fields = ['total_items', 'total_customs_value', 'total_customs_duty', 
                      'total_excise', 'total_vat', 'total_tax_liability']
    
    for field in numeric_fields:
        if field in cleaned and cleaned[field]:
            cleaned[field] = float(cleaned[field])
    
    return cleaned


def clean_declarations(input_path: str, output_dir: str) -> Dict:
    """Clean declarations and write to staging"""
    print(f"Cleaning declarations from: {input_path}")
    
    declarations = load_declarations(input_path)
    print(f"  Loaded {len(declarations)} declarations")
    
    cleaned_declarations = []
    validation_results = {'valid': 0, 'invalid': 0, 'errors': []}
    
    for declaration in declarations:
        is_valid, errors = validate_declaration(declaration)
        
        if is_valid:
            cleaned = clean_declaration(declaration)
            cleaned_declarations.append(cleaned)
            validation_results['valid'] += 1
        else:
            validation_results['invalid'] += 1
            validation_results['errors'].append({
                'declaration_id': declaration.get('declaration_id', 'UNKNOWN'),
                'errors': errors
            })
    
    # Write cleaned data to staging
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'cleaned_declarations.csv')
    
    if cleaned_declarations:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=cleaned_declarations[0].keys())
            writer.writeheader()
            writer.writerows(cleaned_declarations)
        
        print(f"  Written {len(cleaned_declarations)} cleaned declarations to: {output_path}")
    
    print(f"\n  Validation Results:")
    print(f"    Valid: {validation_results['valid']}")
    print(f"    Invalid: {validation_results['invalid']}")
    
    return validation_results


def main():
    """Main transformation function"""
    input_path = 'data/raw/declarations/declarations.csv'
    output_dir = 'data/staging/cleaned_declarations'
    
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}")
        return
    
    results = clean_declarations(input_path, output_dir)
    
    if results['invalid'] > 0:
        print(f"\n  Warning: {results['invalid']} declarations had validation errors")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"    {error['declaration_id']}: {error['errors']}")


if __name__ == '__main__':
    main()