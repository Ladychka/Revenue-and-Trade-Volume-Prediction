"""
VAT Calculator - Value-Added Tax Calculation
Phase 5 - Revenue Logic Implementation

Implements law-based VAT calculations based on:
- Phase 1 calculation_formulas.md (Section 4)
- Phase 3 logical_system_design.md

Legal Basis: VAT Act provisions for taxable imports
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class VATCalculationInput:
    """Input parameters for VAT calculation"""
    customs_value: Decimal        # Value of goods (duty-paid value)
    customs_duty: Decimal         # Customs duty amount
    excise_amount: Decimal        # Excise duty amount (if applicable)
    vat_rate: Decimal            # Applicable VAT rate (decimal, e.g., 0.17 for 17%)
    other_taxes: Decimal = Decimal('0.00')  # Other applicable taxes


@dataclass
class VATCalculationResult:
    """Output of VAT calculation"""
    vat_base: Decimal             # Base for VAT calculation
    vat_amount: Decimal           # Calculated VAT amount
    applied_rate: Decimal         # VAT rate applied
    calculation_breakdown: Dict[str, Decimal]


class VATCalculator:
    """
    Calculator for Value-Added Tax on imported goods.
    
    Formula (from Phase 1 - Section 4):
    VAT_Base = Customs_Value + Customs_Duty + Excise_Duty + Other_Taxes
    VAT_Amount = VAT_Base × VAT_Rate
    
    Note: VAT is calculated on the cumulative base including duty and excise.
    """
    
    # Rounding decimal places for VAT amounts
    VAT_ROUNDING = '0.01'
    
    # Standard VAT rate categories
    VAT_RATE_STANDARD = Decimal('0.1700')    # 17%
    VAT_RATE_REDUCED = Decimal('0.0700')     # 7%
    VAT_RATE_ZERO = Decimal('0.0000')       # 0%
    
    # VAT rate categories from reference data
    VAT_CATEGORIES = {
        'STANDARD': Decimal('0.1700'),
        'REDUCED': Decimal('0.0700'),
        'ZERO': Decimal('0.0000'),
        'EXEMPT': Decimal('0.0000'),
    }
    
    @staticmethod
    def calculate(input_data: VATCalculationInput) -> VATCalculationResult:
        """
        Calculate VAT based on input parameters.
        
        Logic:
        1. Calculate VAT base (customs value + duty + excise + other taxes)
        2. Apply VAT rate to base
        3. Round to 2 decimal places
        """
        # Validate inputs
        if input_data.customs_value < 0:
            raise ValueError("Customs value cannot be negative")
        
        if input_data.vat_rate < 0 or input_data.vat_rate > Decimal('0.2500'):
            raise ValueError("VAT rate must be between 0 and 25%")
        
        if input_data.customs_duty < 0:
            raise ValueError("Customs duty cannot be negative")
        
        if input_data.excise_amount < 0:
            raise ValueError("Excise amount cannot be negative")
        
        # Calculate VAT base
        vat_base = (
            input_data.customs_value + 
            input_data.customs_duty + 
            input_data.excise_amount + 
            input_data.other_taxes
        )
        
        # Calculate VAT amount: VAT_Base × VAT_Rate
        vat_amount = vat_base * input_data.vat_rate
        
        # Round to 2 decimal places
        vat_amount = VATCalculator._round_amount(vat_amount)
        
        # Build calculation breakdown
        breakdown = {
            'customs_value': input_data.customs_value,
            'customs_duty': input_data.customs_duty,
            'excise_amount': input_data.excise_amount,
            'other_taxes': input_data.other_taxes,
            'vat_base': vat_base,
            'vat_rate': input_data.vat_rate,
        }
        
        return VATCalculationResult(
            vat_base=vat_base,
            vat_amount=vat_amount,
            applied_rate=input_data.vat_rate,
            calculation_breakdown=breakdown
        )
    
    @staticmethod
    def _round_amount(amount: Decimal) -> Decimal:
        """Round amount to 2 decimal places using standard rounding"""
        return amount.quantize(Decimal(VATCalculator.VAT_ROUNDING), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_from_dict(data: Dict[str, Any]) -> VATCalculationResult:
        """
        Calculate VAT from dictionary input (for database row processing)
        """
        input_data = VATCalculationInput(
            customs_value=Decimal(str(data.get('customs_value', 0))),
            customs_duty=Decimal(str(data.get('customs_duty', 0))),
            excise_amount=Decimal(str(data.get('excise_amount', 0))),
            vat_rate=Decimal(str(data.get('vat_rate', 0.17))),
            other_taxes=Decimal(str(data.get('other_taxes', 0)))
        )
        
        return VATCalculator.calculate(input_data)
    
    @staticmethod
    def get_vat_rate(category: str) -> Decimal:
        """Get VAT rate by category"""
        return VATCalculator.VAT_CATEGORIES.get(category.upper(), VATCalculator.VAT_RATE_STANDARD)


def calculate_vat(customs_value: float, customs_duty: float, 
                  vat_rate: float, excise: float = 0.0) -> float:
    """
    Simple function interface for VAT calculation.
    
    Args:
        customs_value: Value of goods for duty assessment
        customs_duty: Calculated customs duty amount
        vat_rate: VAT rate (as decimal, e.g., 0.17 for 17%)
        excise: Excise duty amount (default 0)
    
    Returns:
        Calculated VAT amount
    
    Example:
        >>> calculate_vat(1000.00, 50.00, 0.17)
        178.50
        # VAT Base = 1000 + 50 + 0 = 1050
        # VAT = 1050 × 0.17 = 178.50
    """
    cv = Decimal(str(customs_value))
    cd = Decimal(str(customs_duty))
    vr = Decimal(str(vat_rate))
    ex = Decimal(str(excise))
    
    vat_base = cv + cd + ex
    vat_amount = vat_base * vr
    
    return float(VATCalculator._round_amount(vat_amount))


# Test cases for validation
if __name__ == '__main__':
    print("=== VAT Calculator Tests ===\n")
    
    # Test 1: Standard VAT calculation
    test1 = VATCalculationInput(
        customs_value=Decimal('1000.00'),
        customs_duty=Decimal('50.00'),
        excise_amount=Decimal('0.00'),
        vat_rate=Decimal('0.1700')
    )
    result1 = VATCalculator.calculate(test1)
    print(f"Test 1 - Standard 17% VAT:")
    print(f"  Input: CV=1000.00, Duty=50.00, Excise=0, Rate=0.17")
    print(f"  VAT Base: 1000 + 50 + 0 = {result1.vat_base}")
    print(f"  VAT Amount: {result1.vat_base} × 0.17 = {result1.vat_amount}")
    assert result1.vat_amount == Decimal('178.50')
    print("  ✓ PASSED\n")
    
    # Test 2: VAT with excise
    test2 = VATCalculationInput(
        customs_value=Decimal('5000.00'),
        customs_duty=Decimal('750.00'),
        excise_amount=Decimal('200.00'),
        vat_rate=Decimal('0.1700')
    )
    result2 = VATCalculator.calculate(test2)
    print(f"Test 2 - VAT with Excise:")
    print(f"  Input: CV=5000, Duty=750, Excise=200, Rate=0.17")
    print(f"  VAT Base: 5000 + 750 + 200 = {result2.vat_base}")
    print(f"  VAT Amount: {result2.vat_base} × 0.17 = {result2.vat_amount}")
    assert result2.vat_amount == Decimal('1006.50')
    print("  ✓ PASSED\n")
    
    # Test 3: Reduced VAT rate
    test3 = VATCalculationInput(
        customs_value=Decimal('2000.00'),
        customs_duty=Decimal('100.00'),
        excise_amount=Decimal('0.00'),
        vat_rate=Decimal('0.0700')
    )
    result3 = VATCalculator.calculate(test3)
    print(f"Test 3 - Reduced 7% VAT:")
    print(f"  Input: CV=2000, Duty=100, Rate=0.07")
    print(f"  VAT Base: 2000 + 100 = {result3.vat_base}")
    print(f"  VAT Amount: {result3.vat_base} × 0.07 = {result3.vat_amount}")
    assert result3.vat_amount == Decimal('147.00')
    print("  ✓ PASSED\n")
    
    # Test 4: Zero VAT
    test4 = VATCalculationInput(
        customs_value=Decimal('10000.00'),
        customs_duty=Decimal('0.00'),
        excise_amount=Decimal('0.00'),
        vat_rate=Decimal('0.0000')
    )
    result4 = VATCalculator.calculate(test4)
    print(f"Test 4 - Zero VAT:")
    print(f"  Input: CV=10000, Rate=0.00")
    print(f"  Result: {result4.vat_amount}")
    assert result4.vat_amount == Decimal('0.00')
    print("  ✓ PASSED\n")
    
    # Test 5: Rounding verification
    test5 = VATCalculationInput(
        customs_value=Decimal('1234.56'),
        customs_duty=Decimal('98.76'),
        excise_amount=Decimal('0.00'),
        vat_rate=Decimal('0.1700')
    )
    result5 = VATCalculator.calculate(test5)
    print(f"Test 5 - Rounding:")
    print(f"  Input: CV=1234.56, Duty=98.76, Rate=0.17")
    print(f"  VAT Base: 1333.32")
    print(f"  Calculation: 1333.32 × 0.17 = 226.6644")
    print(f"  Result: {result5.vat_amount}")
    assert result5.vat_amount == Decimal('226.66')  # Rounded
    print("  ✓ PASSED\n")
    
    print("=== All Tests Passed ===")
    print("VAT calculator implementation is reproducible and law-based.")