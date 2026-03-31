"""
Duty Calculator - Customs Duty Calculation
Phase 5 - Revenue Logic Implementation

Implements law-based customs duty calculations based on:
- Phase 1 calculation_formulas.md
- Phase 3 logical_system_design.md

Legal Basis: WTO Customs Valuation Agreement, National Tariff Schedule
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class DutyCalculationInput:
    """Input parameters for duty calculation"""
    customs_value: Decimal  # Value of goods for duty assessment
    hs_code: str           # HS code for classification
    duty_rate: Decimal    # Applicable duty rate (decimal, e.g., 0.05 for 5%)
    preferential_rate: Optional[Decimal] = None  # Preferential rate if applicable
    preferential_indicator: bool = False
    origin_country: Optional[str] = None
    preferential_country: Optional[str] = None


@dataclass
class DutyCalculationResult:
    """Output of duty calculation"""
    customs_duty: Decimal
    applied_rate: Decimal
    rate_type: str  # 'MFN' or 'PREFERENTIAL'
    calculation_method: str  # 'AD_VALOREM', 'SPECIFIC', 'COMPOUND'


class DutyCalculator:
    """
    Calculator for customs import duty based on HS classification and origin.
    
    Formulas (from Phase 1 - Section 1):
    - Ad Valorem: Duty = Customs_Value × Duty_Rate
    - Preferential: Duty = Customs_Value × Preferential_Rate (if eligible)
    """
    
    # Rounding decimal places for duty amounts
    DUTY_ROUNDING = '0.01'
    
    # Maximum duty rate (cap at 100%)
    MAX_DUTY_RATE = Decimal('1.0000')
    
    @staticmethod
    def calculate(input_data: DutyCalculationInput) -> DutyCalculationResult:
        """
        Calculate customs duty based on input parameters.
        
        Logic:
        1. Determine applicable rate (preferential vs MFN)
        2. Apply ad valorem formula
        3. Round to 2 decimal places
        """
        # Validate inputs
        if input_data.customs_value < 0:
            raise ValueError("Customs value cannot be negative")
        
        if input_data.duty_rate < 0 or input_data.duty_rate > DutyCalculator.MAX_DUTY_RATE:
            raise ValueError(f"Duty rate must be between 0 and {DutyCalculator.MAX_DUTY_RATE}")
        
        # Determine applicable rate
        if (input_data.preferential_indicator and 
            input_data.preferential_rate is not None and
            input_data.preferential_rate > 0):
            
            applied_rate = input_data.preferential_rate
            rate_type = 'PREFERENTIAL'
            calculation_method = 'AD_VALOREM'
        else:
            applied_rate = input_data.duty_rate
            rate_type = 'MFN'
            calculation_method = 'AD_VALOREM'
        
        # Calculate duty: Customs_Value × Applied_Rate
        customs_duty = input_data.customs_value * applied_rate
        
        # Round to 2 decimal places (standard rounding)
        customs_duty = DutyCalculator._round_amount(customs_duty)
        
        return DutyCalculationResult(
            customs_duty=customs_duty,
            applied_rate=applied_rate,
            rate_type=rate_type,
            calculation_method=calculation_method
        )
    
    @staticmethod
    def _round_amount(amount: Decimal) -> Decimal:
        """Round amount to 2 decimal places using standard rounding"""
        return amount.quantize(Decimal(DutyCalculator.DUTY_ROUNDING), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_from_dict(data: Dict[str, Any]) -> DutyCalculationResult:
        """
        Calculate duty from dictionary input (for database row processing)
        """
        input_data = DutyCalculationInput(
            customs_value=Decimal(str(data.get('customs_value', 0))),
            hs_code=data.get('hs_code', ''),
            duty_rate=Decimal(str(data.get('duty_rate', 0))),
            preferential_rate=Decimal(str(data['preferential_rate'])) if data.get('preferential_rate') else None,
            preferential_indicator=bool(data.get('preferential_indicator', False)),
            origin_country=data.get('origin_country'),
            preferential_country=data.get('preferential_country')
        )
        
        return DutyCalculator.calculate(input_data)


def calculate_duty(customs_value: float, duty_rate: float, 
                   preferential: bool = False, preferential_rate: float = 0.0) -> float:
    """
    Simple function interface for duty calculation.
    
    Args:
        customs_value: Value of goods for duty assessment
        duty_rate: MFN duty rate (as decimal, e.g., 0.05 for 5%)
        preferential: Whether preferential treatment applies
        preferential_rate: Preferential duty rate if applicable
    
    Returns:
        Calculated customs duty amount
    
    Example:
        >>> calculate_duty(1000.00, 0.05)
        50.00
        >>> calculate_duty(1000.00, 0.05, preferential=True, preferential_rate=0.02)
        20.00
    """
    cv = Decimal(str(customs_value))
    dr = Decimal(str(duty_rate))
    
    if preferential and preferential_rate > 0:
        pr = Decimal(str(preferential_rate))
        applied_rate = pr
    else:
        applied_rate = dr
    
    duty = cv * applied_rate
    return float(DutyCalculator._round_amount(duty))


# Test cases for validation
if __name__ == '__main__':
    print("=== Duty Calculator Tests ===\n")
    
    # Test 1: Standard MFN calculation
    test1 = DutyCalculationInput(
        customs_value=Decimal('1000.00'),
        hs_code='8471300000',
        duty_rate=Decimal('0.0500')
    )
    result1 = DutyCalculator.calculate(test1)
    print(f"Test 1 - Standard MFN 5%:")
    print(f"  Input: customs_value=1000.00, duty_rate=0.05")
    print(f"  Result: customs_duty={result1.customs_duty}, rate_type={result1.rate_type}")
    assert result1.customs_duty == Decimal('50.00')
    assert result1.rate_type == 'MFN'
    print("  ✓ PASSED\n")
    
    # Test 2: Preferential rate application
    test2 = DutyCalculationInput(
        customs_value=Decimal('5000.00'),
        hs_code='8703235010',
        duty_rate=Decimal('0.2500'),
        preferential_rate=Decimal('0.1500'),
        preferential_indicator=True
    )
    result2 = DutyCalculator.calculate(test2)
    print(f"Test 2 - Preferential Rate:")
    print(f"  Input: customs_value=5000.00, MFN=0.25, pref=0.15")
    print(f"  Result: customs_duty={result2.customs_duty}, rate_type={result2.rate_type}")
    assert result2.customs_duty == Decimal('750.00')
    assert result2.rate_type == 'PREFERENTIAL'
    print("  ✓ PASSED\n")
    
    # Test 3: Zero duty rate
    test3 = DutyCalculationInput(
        customs_value=Decimal('25000.00'),
        hs_code='3002150000',
        duty_rate=Decimal('0.0000')
    )
    result3 = DutyCalculator.calculate(test3)
    print(f"Test 3 - Zero Duty Rate:")
    print(f"  Input: customs_value=25000.00, duty_rate=0.00")
    print(f"  Result: customs_duty={result3.customs_duty}")
    assert result3.customs_duty == Decimal('0.00')
    print("  ✓ PASSED\n")
    
    # Test 4: Rounding verification
    test4 = DutyCalculationInput(
        customs_value=Decimal('123.45'),
        hs_code='6203420000',
        duty_rate=Decimal('0.1675')
    )
    result4 = DutyCalculator.calculate(test4)
    print(f"Test 4 - Rounding:")
    print(f"  Input: customs_value=123.45, duty_rate=0.1675")
    print(f"  Calculation: 123.45 × 0.1675 = 20.677875")
    print(f"  Result: customs_duty={result4.customs_duty}")
    assert result4.customs_duty == Decimal('20.68')  # Rounded
    print("  ✓ PASSED\n")
    
    print("=== All Tests Passed ===")
    print("Duty calculator implementation is reproducible and law-based.")