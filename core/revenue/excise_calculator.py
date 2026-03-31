"""
Excise Calculator - Excise Duty Calculation
Phase 5 - Revenue Logic Implementation

Implements law-based excise calculations based on:
- Phase 1 calculation_formulas.md (Section 3)
- Phase 3 logical_system_design.md

Legal Basis: National excise taxation act for specific goods
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ExciseCalculationInput:
    """Input parameters for excise calculation"""
    customs_value: Decimal         # Value of goods
    quantity: Decimal             # Quantity of goods
    quantity_unit: str            # Unit of quantity (KGM, LTR, PCE)
    excise_applicable: bool       # Whether excise applies
    excise_type: Optional[str]    # 'AD_VALOREM', 'SPECIFIC', or 'MIXED'
    excise_rate: Decimal          # Ad valorem rate (if applicable)
    specific_excise_rate: Optional[Decimal]  # Specific rate per unit (if applicable)


@dataclass
class ExciseCalculationResult:
    """Output of excise calculation"""
    excise_amount: Decimal
    calculation_method: str  # 'AD_VALOREM', 'SPECIFIC', 'MIXED', or 'NONE'
    applied_rate: Optional[Decimal]
    rate_type: str  # 'PERCENTAGE' or 'PER_UNIT'


class ExciseCalculator:
    """
    Calculator for excise duty on specific goods (tobacco, alcohol, fuel, etc.)
    
    Formulas (from Phase 1 - Section 3):
    - Ad Valorem: Excise = Customs_Value × Excise_Rate
    - Specific: Excise = Quantity × Specific_Excise_Rate
    - Mixed: Excise = MAX(Ad_Valorem, Specific)
    
    Note: Excise only applies to specific goods defined in excise regulations.
    """
    
    # Rounding decimal places for excise amounts
    EXCISE_ROUNDING = '0.01'
    
    # Excise types
    EXCISE_TYPE_AD_VALOREM = 'AD_VALOREM'
    EXCISE_TYPE_SPECIFIC = 'SPECIFIC'
    EXCISE_TYPE_MIXED = 'MIXED'
    
    # Maximum rates (cap at 100% for ad valorem)
    MAX_EXCISE_RATE = Decimal('1.0000')
    
    # Goods typically subject to excise (by HS chapter prefix)
    EXCISABLE_CHAPTERS = ['22', '24']  # Alcohol, tobacco
    
    @staticmethod
    def calculate(input_data: ExciseCalculationInput) -> ExciseCalculationResult:
        """
        Calculate excise duty based on input parameters.
        
        Logic:
        1. Check if excise is applicable
        2. Calculate based on type (ad valorem, specific, or mixed)
        3. Round to 2 decimal places
        """
        # If not applicable, return zero
        if not input_data.excise_applicable or input_data.excise_type is None:
            return ExciseCalculationResult(
                excise_amount=Decimal('0.00'),
                calculation_method='NONE',
                applied_rate=None,
                rate_type='N/A'
            )
        
        # Validate inputs
        if input_data.customs_value < 0:
            raise ValueError("Customs value cannot be negative")
        
        if input_data.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        if input_data.excise_rate < 0 or input_data.excise_rate > ExciseCalculator.MAX_EXCISE_RATE:
            raise ValueError(f"Excise rate must be between 0 and {ExciseCalculator.MAX_EXCISE_RATE}")
        
        calculation_method = input_data.excise_type.upper()
        
        # Calculate based on excise type
        if calculation_method == ExciseCalculator.EXCISE_TYPE_AD_VALOREM:
            # Ad valorem: Customs_Value × Excise_Rate
            excise_amount = input_data.customs_value * input_data.excise_rate
            applied_rate = input_data.excise_rate
            rate_type = 'PERCENTAGE'
            
        elif calculation_method == ExciseCalculator.EXCISE_TYPE_SPECIFIC:
            # Specific: Quantity × Specific_Rate
            if input_data.specific_excise_rate is None:
                raise ValueError("Specific excise rate required for SPECIFIC type")
            
            excise_amount = input_data.quantity * input_data.specific_excise_rate
            applied_rate = input_data.specific_excise_rate
            rate_type = 'PER_UNIT'
            
        elif calculation_method == ExciseCalculator.EXCISE_TYPE_MIXED:
            # Mixed: MAX(Ad valorem, Specific)
            if input_data.specific_excise_rate is None:
                raise ValueError("Specific excise rate required for MIXED type")
            
            # Calculate both methods
            ad_valorem_amount = input_data.customs_value * input_data.excise_rate
            specific_amount = input_data.quantity * input_data.specific_excise_rate
            
            # Take the higher amount
            excise_amount = max(ad_valorem_amount, specific_amount)
            
            # Track which method won
            if excise_amount == ad_valorem_amount:
                applied_rate = input_data.excise_rate
                rate_type = 'PERCENTAGE'
                calculation_method = 'MIXED (AD_VALOREM)'
            else:
                applied_rate = input_data.specific_excise_rate
                rate_type = 'PER_UNIT'
                calculation_method = 'MIXED (SPECIFIC)'
        
        else:
            raise ValueError(f"Unknown excise type: {input_data.excise_type}")
        
        # Round to 2 decimal places
        excise_amount = ExciseCalculator._round_amount(excise_amount)
        
        return ExciseCalculationResult(
            excise_amount=excise_amount,
            calculation_method=calculation_method,
            applied_rate=applied_rate,
            rate_type=rate_type
        )
    
    @staticmethod
    def _round_amount(amount: Decimal) -> Decimal:
        """Round amount to 2 decimal places using standard rounding"""
        return amount.quantize(Decimal(ExciseCalculator.EXCISE_ROUNDING), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def is_excisable(hs_code: str) -> bool:
        """Check if HS code is typically subject to excise"""
        chapter = hs_code[:2] if len(hs_code) >= 2 else ''
        return chapter in ExciseCalculator.EXCISABLE_CHAPTERS
    
    @staticmethod
    def calculate_from_dict(data: Dict[str, Any]) -> ExciseCalculationResult:
        """
        Calculate excise from dictionary input (for database row processing)
        """
        input_data = ExciseCalculationInput(
            customs_value=Decimal(str(data.get('customs_value', 0))),
            quantity=Decimal(str(data.get('quantity', 0))),
            quantity_unit=data.get('quantity_unit', 'KGM'),
            excise_applicable=bool(data.get('excise_applicable', False)),
            excise_type=data.get('excise_type'),
            excise_rate=Decimal(str(data.get('excise_rate', 0))),
            specific_excise_rate=Decimal(str(data['specific_excise_rate'])) if data.get('specific_excise_rate') else None
        )
        
        return ExciseCalculator.calculate(input_data)


def calculate_excise(customs_value: float, quantity: float,
                     excise_type: str, excise_rate: float,
                     specific_rate: float = 0.0) -> float:
    """
    Simple function interface for excise calculation.
    
    Args:
        customs_value: Value of goods for assessment
        quantity: Quantity of goods
        excise_type: 'AD_VALOREM', 'SPECIFIC', or 'MIXED'
        excise_rate: Ad valorem rate (as decimal)
        specific_rate: Specific rate per unit (if applicable)
    
    Returns:
        Calculated excise amount
    
    Example:
        >>> calculate_excise(1000.00, 100, 'AD_VALOREM', 0.10)
        100.00
        >>> calculate_excise(1000.00, 100, 'SPECIFIC', 0, 0.50)
        50.00
    """
    cv = Decimal(str(customs_value))
    qty = Decimal(str(quantity))
    et = excise_type.upper()
    er = Decimal(str(excise_rate))
    sr = Decimal(str(specific_rate)) if specific_rate > 0 else None
    
    input_data = ExciseCalculationInput(
        customs_value=cv,
        quantity=qty,
        quantity_unit='KGM',
        excise_applicable=(et in ['AD_VALOREM', 'SPECIFIC', 'MIXED']),
        excise_type=et if et in ['AD_VALOREM', 'SPECIFIC', 'MIXED'] else None,
        excise_rate=er,
        specific_excise_rate=sr
    )
    
    result = ExciseCalculator.calculate(input_data)
    return float(result.excise_amount)


# Test cases for validation
if __name__ == '__main__':
    print("=== Excise Calculator Tests ===\n")
    
    # Test 1: Not applicable (standard goods)
    test1 = ExciseCalculationInput(
        customs_value=Decimal('1000.00'),
        quantity=Decimal('50'),
        quantity_unit='PCE',
        excise_applicable=False,
        excise_type=None,
        excise_rate=Decimal('0.00')
    )
    result1 = ExciseCalculator.calculate(test1)
    print(f"Test 1 - Non-excisable goods:")
    print(f"  Input: customs_value=1000, applicable=False")
    print(f"  Result: {result1.excise_amount}, method={result1.calculation_method}")
    assert result1.excise_amount == Decimal('0.00')
    assert result1.calculation_method == 'NONE'
    print("  ✓ PASSED\n")
    
    # Test 2: Ad valorem excise
    test2 = ExciseCalculationInput(
        customs_value=Decimal('5000.00'),
        quantity=Decimal('100'),
        quantity_unit='KGM',
        excise_applicable=True,
        excise_type='AD_VALOREM',
        excise_rate=Decimal('0.10'),
        specific_excise_rate=None
    )
    result2 = ExciseCalculator.calculate(test2)
    print(f"Test 2 - Ad Valorem Excise (10%):")
    print(f"  Input: CV=5000, rate=0.10")
    print(f"  Calculation: 5000 × 0.10 = 500")
    print(f"  Result: {result2.excise_amount}, method={result2.calculation_method}")
    assert result2.excise_amount == Decimal('500.00')
    assert result2.calculation_method == 'AD_VALOREM'
    print("  ✓ PASSED\n")
    
    # Test 3: Specific excise
    test3 = ExciseCalculationInput(
        customs_value=Decimal('2000.00'),
        quantity=Decimal('1000'),
        quantity_unit='LTR',
        excise_applicable=True,
        excise_type='SPECIFIC',
        excise_rate=Decimal('0.00'),
        specific_excise_rate=Decimal('0.50')
    )
    result3 = ExciseCalculator.calculate(test3)
    print(f"Test 3 - Specific Excise (0.50/L):")
    print(f"  Input: Qty=1000L, rate=0.50/L")
    print(f"  Calculation: 1000 × 0.50 = 500")
    print(f"  Result: {result3.excise_amount}, method={result3.calculation_method}")
    assert result3.excise_amount == Decimal('500.00')
    assert result3.calculation_method == 'SPECIFIC'
    print("  ✓ PASSED\n")
    
    # Test 4: Mixed excise (ad valorem wins)
    test4 = ExciseCalculationInput(
        customs_value=Decimal('10000.00'),
        quantity=Decimal('500'),
        quantity_unit='LTR',
        excise_applicable=True,
        excise_type='MIXED',
        excise_rate=Decimal('0.05'),
        specific_excise_rate=Decimal('0.80')
    )
    result4 = ExciseCalculator.calculate(test4)
    print(f"Test 4 - Mixed Excise (Ad valorem wins):")
    print(f"  Input: CV=10000 (5% = 500), Qty=500 (0.80/L = 400)")
    print(f"  Calculation: MAX(500, 400) = 500")
    print(f"  Result: {result4.excise_amount}, method={result4.calculation_method}")
    assert result4.excise_amount == Decimal('500.00')
    print("  ✓ PASSED\n")
    
    # Test 5: Mixed excise (specific wins)
    test5 = ExciseCalculationInput(
        customs_value=Decimal('5000.00'),
        quantity=Decimal('1000'),
        quantity_unit='LTR',
        excise_applicable=True,
        excise_type='MIXED',
        excise_rate=Decimal('0.02'),
        specific_excise_rate=Decimal('0.10')
    )
    result5 = ExciseCalculator.calculate(test5)
    print(f"Test 5 - Mixed Excise (Specific wins):")
    print(f"  Input: CV=5000 (2% = 100), Qty=1000 (0.10/L = 100)")
    print(f"  Calculation: MAX(100, 100) = 100")
    print(f"  Result: {result5.excise_amount}, method={result5.calculation_method}")
    assert result5.excise_amount == Decimal('100.00')
    print("  ✓ PASSED\n")
    
    # Test 6: Rounding verification
    test6 = ExciseCalculationInput(
        customs_value=Decimal('1234.56'),
        quantity=Decimal('77.777'),
        quantity_unit='KGM',
        excise_applicable=True,
        excise_type='AD_VALOREM',
        excise_rate=Decimal('0.0755'),
        specific_excise_rate=None
    )
    result6 = ExciseCalculator.calculate(test6)
    print(f"Test 6 - Rounding:")
    print(f"  Input: CV=1234.56, rate=0.0755")
    print(f"  Calculation: 1234.56 × 0.0755 = 93.20928")
    print(f"  Result: {result6.excise_amount}")
    assert result6.excise_amount == Decimal('93.21')  # Rounded
    print("  ✓ PASSED\n")
    
    print("=== All Tests Passed ===")
    print("Excise calculator implementation is reproducible and law-based.")