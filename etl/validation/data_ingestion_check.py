"""
Data Ingestion Validation Module

This module provides validation functions to ensure only allowed data types
(synthetic, anonymized, aggregated) enter the system, blocking real/prohibited data.

Usage:
    from etl.validation.data_ingestion_check import validate_data_source
    
    # Validate data before ETL processing
    result = validate_data_source(data_df)
    if not result['is_valid']:
        raise ValueError(f"Prohibited data detected: {result['violations']}")
"""

import re
from typing import Dict, List, Any
import pandas as pd


# Prohibited data patterns - regex patterns for PII and sensitive data
PROHIBITED_PATTERNS = {
    'personal_names': r'^[A-Z][a-z]+(\s+[A-Z][a-z]+)+$',  # Two+ word names
    'email_address': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'phone_number': r'\d{10,}',  # 10+ digit phone numbers
    'national_id': r'\d{6,12}',  # 6-12 digit ID numbers
    'passport_number': r'[A-Z]{1,2}\d{6,9}',  # Passport format
    'bank_account': r'\d{8,17}',  # Bank account numbers
    'credit_card': r'\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}',  # Credit card format
    'tax_id_individual': r'\d{2}-\d{7}',  # Individual tax ID format
    'ip_address': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
}

# Prohibited column names
PROHIBITED_COLUMNS = [
    'full_name', 'first_name', 'last_name', 'surname',
    'email', 'phone', 'telephone', 'mobile',
    'address', 'residential_address', 'postal_address',
    'national_id', 'passport', 'id_number', 'ssn',
    'bank_account', 'iban', 'swift', 'payment_method',
    'tax_id', 'vat_number', 'tin',
    'date_of_birth', 'dob', 'birth_date',
    'gender', 'ethnicity', 'religion',
    'employer', 'occupation',
]


class DataIngestionValidator:
    """
    Validates data before ingestion to ensure compliance with privacy policy.
    """
    
    def __init__(self):
        self.violations: List[Dict[str, str]] = []
        
    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate a pandas DataFrame for prohibited data types.
        
        Args:
            df: Input DataFrame to validate
            
        Returns:
            Dict with 'is_valid' (bool), 'violations' (list), 'warnings' (list)
        """
        self.violations = []
        warnings = []
        
        # 1. Check for prohibited column names
        self._check_column_names(df.columns)
        
        # 2. Check for prohibited patterns in string columns
        self._check_data_patterns(df)
        
        # 3. Check for minimum aggregation level
        self._check_aggregation_level(df)
        
        # 4. Check for real entity identifiers
        self._check_entity_identifiers(df)
        
        return {
            'is_valid': len(self.violations) == 0,
            'violations': self.violations,
            'warnings': warnings
        }
    
    def _check_column_names(self, columns) -> None:
        """Check for prohibited column names."""
        for col in columns:
            col_lower = col.lower()
            for prohibited in PROHIBITED_COLUMNS:
                if prohibited in col_lower:
                    self.violations.append({
                        'type': 'prohibited_column',
                        'column': col,
                        'reason': f'Column contains prohibited data type: {prohibited}'
                    })
    
    def _check_data_patterns(self, df: pd.DataFrame) -> None:
        """Check for prohibited patterns in string data."""
        for col in df.select_dtypes(include=['object']).columns:
            sample = df[col].dropna().head(100)  # Sample first 100 non-null values
            for idx, value in sample.items():
                if pd.isna(value):
                    continue
                value_str = str(value)
                
                # Check against prohibited patterns
                for pattern_name, pattern_regex in PROHIBITED_PATTERNS.items():
                    if re.search(pattern_regex, value_str):
                        self.violations.append({
                            'type': 'prohibited_pattern',
                            'column': col,
                            'row': idx,
                            'value_preview': value_str[:50],
                            'reason': f'Detected prohibited pattern: {pattern_name}'
                        })
                        break  # Only report first violation per cell
    
    def _check_aggregation_level(self, df: pd.DataFrame) -> None:
        """Check if data is properly aggregated (minimum monthly granularity)."""
        # Check for daily/individual-level data
        date_columns = [col for col in df.columns if any(
            keyword in col.lower() for keyword in ['date', 'datetime', 'timestamp']
        )]
        
        if date_columns:
            # Warn if dates are at daily granularity (not aggregated to month+)
            warnings.append({
                'type': 'aggregation_warning',
                'reason': 'Date columns detected - ensure data is aggregated to monthly or higher'
            })
    
    def _check_entity_identifiers(self, df: pd.DataFrame) -> None:
        """Check for real entity identifiers."""
        # Check for company names, registration numbers, etc.
        entity_columns = [col for col in df.columns if any(
            keyword in col.lower() for keyword in 
            ['company', 'business', 'entity', 'registration', 'license']
        )]
        
        for col in entity_columns:
            sample = df[col].dropna().head(50)
            for idx, value in sample.items():
                if pd.isna(value):
                    continue
                # Check for realistic company names (not codes/hashes)
                value_str = str(value)
                if len(value_str) > 3 and not re.match(r'^[A-Z0-9-]+$', value_str):
                    # Likely a real company name, not a code
                    self.violations.append({
                        'type': 'real_entity_identifier',
                        'column': col,
                        'row': idx,
                        'value_preview': value_str[:50],
                        'reason': 'Possible real entity name detected - use anonymized codes instead'
                    })


def validate_data_source(data_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Main validation function for data ingestion.
    
    Args:
        data_df: pandas DataFrame to validate
        
    Returns:
        Dict with validation results
        
    Example:
        >>> result = validate_data_source(df)
        >>> if not result['is_valid']:
        >>>     print(f"Data rejected: {result['violations']}")
    """
    validator = DataIngestionValidator()
    return validator.validate_dataframe(data_df)


def validate_csv_file(file_path: str) -> Dict[str, Any]:
    """
    Validate a CSV file before ingestion.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Dict with validation results
    """
    df = pd.read_csv(file_path)
    return validate_data_source(df)


def validate_json_file(file_path: str) -> Dict[str, Any]:
    """
    Validate a JSON file before ingestion.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dict with validation results
    """
    df = pd.read_json(file_path)
    return validate_data_source(df)


# ETL Integration - Add to your ETL pipeline
def validate_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates data and transforms to ensure compliance.
    
    This function should be called in your ETL pipeline before
    loading data into the staging/curated layers.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Transformed DataFrame (with PII removed/masked)
        
    Raises:
        ValueError: If prohibited data is detected
    """
    # First validate
    result = validate_data_source(df)
    
    if not result['is_valid']:
        raise ValueError(
            f"Data ingestion blocked - prohibited data detected:\n"
            f"{result['violations']}"
        )
    
    # Transform: Mask/remove any remaining sensitive columns
    df_clean = df.copy()
    
    # Drop prohibited columns if they exist
    for col in df_clean.columns:
        col_lower = col.lower()
        for prohibited in PROHIBITED_COLUMNS:
            if prohibited in col_lower:
                df_clean = df_clean.drop(columns=[col])
                break
    
    return df_clean


if __name__ == "__main__":
    # Example usage and testing
    print("Data Ingestion Validation Module")
    print("=" * 50)
    print("\nThis module validates data before ETL ingestion.")
    print("Supported data types: Synthetic, Anonymized, Aggregated")
    print("Prohibited data types: PII, Real IDs, Financial details")
    print("\nImport and use: from etl.validation.data_ingestion_check import validate_data_source")