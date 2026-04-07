import pytest
from decimal import Decimal
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.calculations.excise import ExciseCalculator, ExciseCategory

def test_excise_ad_valorem_basic():
    """Test standard ad valorem (percentage) tax application"""
    customs_value = Decimal('1000.00')
    
    # default alcohol is 35% -> 350.00
    excise = ExciseCalculator.calculate_excise(customs_value, ExciseCategory.ALCOHOL)
    assert excise == Decimal('350.00')

def test_excise_with_specific_rate():
    """Test mixed ad valorem and specific rate application (e.g. tobacco)"""
    customs_value = Decimal('1000.00')
    
    # 40% default + $1.50 per unit on 100 units
    excise = ExciseCalculator.calculate_excise(
        customs_value, 
        ExciseCategory.TOBACCO,
        specific_rate_amount=Decimal('1.50'),
        volume_units=Decimal('100')
    )
    
    # 400 + 150 = 550
    assert excise == Decimal('550.00')

def test_excise_scenario_override():
    """Test what-if scenario custom rate overriding"""
    customs_value = Decimal('500.00')
    
    # Override fuel from 25% down to 10%
    excise = ExciseCalculator.calculate_excise(
        customs_value, 
        ExciseCategory.FUEL,
        custom_rate=Decimal('0.10')
    )
    assert excise == Decimal('50.00')

def test_excise_exempt():
    """Test exempt goods properly return 0 without math errors"""
    excise = ExciseCalculator.calculate_excise(Decimal('9999999.00'), ExciseCategory.EXEMPT)
    assert excise == Decimal('0.00')

def test_excise_negative_validation():
    """Test defensive boundary logic against illegal negative values"""
    with pytest.raises(ValueError):
        ExciseCalculator.calculate_excise(Decimal('-100.00'), ExciseCategory.ALCOHOL)
