#!/usr/bin/env python3
"""
Rounding Rules Module - Currency Rounding Utilities
Phase 5 - Core Business Logic

Provides currency rounding rules for customs revenue calculations.
Ensures consistent rounding across duty, VAT, and excise calculations.
"""

from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN
from typing import Dict


# ============================================================================
# Rounding Configuration by Currency
# ============================================================================

ROUNDING_CONFIG: Dict[str, Dict] = {
    'USD': {
        'decimal_places': 2,
        'method': 'ROUND_HALF_UP',
        'min_amount': 0.01,
    },
    'EUR': {
        'decimal_places': 2,
        'method': 'ROUND_HALF_UP',
        'min_amount': 0.01,
    },
    'KHR': {
        'decimal_places': 0,
        'method': 'ROUND_HALF_UP',
        'min_amount': 100,  # Cambodian Riel - no decimals
    },
    'THB': {
        'decimal_places': 2,
        'method': 'ROUND_HALF_UP',
        'min_amount': 0.01,
    },
    'JPY': {
        'decimal_places': 0,
        'method': 'ROUND_HALF_UP',
        'min_amount': 1,
    },
    'CNY': {
        'decimal_places': 2,
        'method': 'ROUND_HALF_UP',
        'min_amount': 0.01,
    },
    'GBP': {
        'decimal_places': 2,
        'method': 'ROUND_HALF_UP',
        'min_amount': 0.01,
    },
    'KRW': {
        'decimal_places': 0,
        'method': 'ROUND_HALF_UP',
        'min_amount': 1,
    },
}


# ============================================================================
# Rounding Functions
# ============================================================================

def get_rounding_config(currency_code: str) -> Dict:
    """Get rounding configuration for a currency"""
    return ROUNDING_CONFIG.get(currency_code, ROUNDING_CONFIG['USD'])


def round_currency(amount: float, currency_code: str = 'USD') -> Decimal:
    """
    Round amount according to currency-specific rules.
    
    Args:
        amount: The amount to round
        currency_code: ISO 4217 currency code
    
    Returns:
        Rounded Decimal amount
    """
    config = get_rounding_config(currency_code)
    decimal_places = config['decimal_places']
    
    # Convert to Decimal for precision
    decimal_amount = Decimal(str(amount))
    
    # Create quantize parameter
    quantize_str = '0.' + '0' * decimal_places if decimal_places > 0 else '1'
    quantize_param = Decimal(quantize_str)
    
    # Apply rounding
    if config['method'] == 'ROUND_HALF_UP':
        return decimal_amount.quantize(quantize_param, rounding=ROUND_HALF_UP)
    elif config['method'] == 'ROUND_HALF_DOWN':
        return decimal_amount.quantize(quantize_param, rounding=ROUND_HALF_DOWN)
    else:
        return decimal_amount.quantize(quantize_param, rounding=ROUND_HALF_UP)


def round_duty(amount: float, currency_code: str = 'USD') -> Decimal:
    """
    Round customs duty amount.
    
    Customs duty is typically rounded to 2 decimal places
    for most currencies.
    """
    return round_currency(amount, currency_code)


def round_vat(amount: float, currency_code: str = 'USD') -> Decimal:
    """
    Round VAT amount.
    
    VAT is typically rounded to 2 decimal places.
    """
    return round_currency(amount, currency_code)


def round_excise(amount: float, currency_code: str = 'USD') -> Decimal:
    """
    Round excise tax amount.
    
    Excise tax follows the same rounding rules as VAT.
    """
    return round_currency(amount, currency_code)


def round_total_tax(amount: float, currency_code: str = 'USD') -> Decimal:
    """
    Round total tax liability.
    
    Total tax (duty + VAT + excise) follows standard rounding.
    """
    return round_currency(amount, currency_code)


def round_customs_value(amount: float, currency_code: str = 'USD') -> Decimal:
    """
    Round customs value.
    
    Customs value is typically rounded to 2 decimal places.
    """
    return round_currency(amount, currency_code)


def round_exchange_rate(rate: float) -> Decimal:
    """
    Round exchange rate.
    
    Exchange rates are typically rounded to 6 decimal places
    for precision in currency conversion.
    """
    decimal_rate = Decimal(str(rate))
    return decimal_rate.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)


# ============================================================================
# Validation Functions
# ============================================================================

def validate_rounded_amount(amount: float, currency_code: str = 'USD') -> bool:
    """
    Validate that amount follows proper rounding for currency.
    
    Args:
        amount: The amount to validate
        currency_code: The currency code
    
    Returns:
        True if amount is properly rounded, False otherwise
    """
    config = get_rounding_config(currency_code)
    decimal_places = config['decimal_places']
    
    # Convert to string and check decimal places
    amount_str = f"{amount:.{decimal_places}f}"
    rounded_amount = float(amount_str)
    
    return abs(amount - rounded_amount) < 0.0001


def get_minimum_amount(currency_code: str) -> float:
    """Get minimum taxable amount for a currency"""
    config = get_rounding_config(currency_code)
    return config['min_amount']


# ============================================================================
# Tax Calculation Helpers
# ============================================================================

def calculate_tax_base(customs_value: float, duty: float) -> Decimal:
    """
    Calculate VAT base (customs value + duty).
    
    In most jurisdictions, VAT is calculated on:
    Customs Value + Customs Duty
    """
    base = Decimal(str(customs_value)) + Decimal(str(duty))
    return base.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def apply_percentage_rate(amount: float, rate: float, currency_code: str = 'USD') -> Decimal:
    """
    Apply a percentage rate to an amount and round the result.
    
    Args:
        amount: Base amount
        rate: Percentage rate (e.g., 0.17 for 17%)
        currency_code: Currency for rounding
    
    Returns:
        Calculated tax amount
    """
    calculated = Decimal(str(amount)) * Decimal(str(rate))
    return round_currency(float(calculated), currency_code)


# ============================================================================
# Tests
# ============================================================================

if __name__ == '__main__':
    print("=== Rounding Rules Tests ===\n")
    
    # Test USD rounding
    print("Test 1: USD Rounding")
    assert round_currency(100.125, 'USD') == Decimal('100.13')
    assert round_currency(100.124, 'USD') == Decimal('100.12')
    print("  ✓ USD rounding correct")
    
    # Test KHR rounding (no decimals)
    print("Test 2: KHR Rounding (no decimals)")
    assert round_currency(1000.5, 'KHR') == Decimal('1001')
    assert round_currency(1000.4, 'KHR') == Decimal('1000')
    print("  ✓ KHR rounding correct")
    
    # Test JPY rounding (no decimals)
    print("Test 3: JPY Rounding")
    assert round_currency(1000.5, 'JPY') == Decimal('1001')
    print("  ✓ JPY rounding correct")
    
    # Test exchange rate
    print("Test 4: Exchange Rate Rounding")
    assert round_exchange_rate(0.1234567) == Decimal('0.123457')
    assert round_exchange_rate(1.23456789) == Decimal('1.234568')
    print("  ✓ Exchange rate rounding correct")
    
    # Test tax base calculation
    print("Test 5: Tax Base Calculation")
    base = calculate_tax_base(1000.00, 100.00)
    assert base == Decimal('1100.00')
    print("  ✓ Tax base calculation correct")
    
    # Test percentage rate application
    print("Test 6: Apply Percentage Rate")
    vat = apply_percentage_rate(1100.00, 0.17, 'USD')
    assert vat == Decimal('187.00')
    print("  ✓ Percentage rate correct")
    
    print("\n=== All Rounding Tests Passed ===")