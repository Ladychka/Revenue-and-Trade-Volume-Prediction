#!/usr/bin/env python3
"""
Unit Tests - Revenue Calculations
Phase 10 - Testing

Tests for revenue calculation modules.
Matches actual function signatures in core/revenue/*.py
"""

import unittest
from decimal import Decimal
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from core.revenue.duty_calculator import (
    calculate_duty, DutyCalculator, DutyCalculationInput
)
from core.revenue.vat_calculator import (
    calculate_vat, VATCalculator, VATCalculationInput
)
from core.revenue.excise_calculator import (
    calculate_excise, ExciseCalculator, ExciseCalculationInput
)
from core.revenue.total_revenue import (
    calculate_total_revenue, TotalRevenueCalculator, TotalRevenueInput
)
from core.common.rounding_rules import round_currency, round_duty, round_vat


class TestDutyCalculation(unittest.TestCase):
    """Test cases for customs duty calculation"""
    
    def test_standard_duty_calculation(self):
        """Test standard MFN duty calculation"""
        # calculate_duty(customs_value, duty_rate, preferential, preferential_rate)
        result = calculate_duty(
            customs_value=1000.00,
            duty_rate=0.25,
        )
        self.assertEqual(result, 250.00)
    
    def test_preferential_duty_calculation(self):
        """Test preferential duty rate"""
        result = calculate_duty(
            customs_value=1000.00,
            duty_rate=0.25,
            preferential=True,
            preferential_rate=0.15,
        )
        self.assertEqual(result, 150.00)
    
    def test_zero_duty_rate(self):
        """Test zero duty rate (exempt goods)"""
        result = calculate_duty(
            customs_value=5000.00,
            duty_rate=0.0,
        )
        self.assertEqual(result, 0.00)
    
    def test_duty_rounding(self):
        """Test duty amount rounding (ROUND_HALF_UP)"""
        result = calculate_duty(
            customs_value=123.45,
            duty_rate=0.1675,
        )
        # 123.45 * 0.1675 = 20.677875 → rounded to 20.68
        self.assertEqual(result, 20.68)

    def test_class_based_calculation(self):
        """Test DutyCalculator class directly"""
        input_data = DutyCalculationInput(
            customs_value=Decimal('1000.00'),
            hs_code='8471300000',
            duty_rate=Decimal('0.0500')
        )
        result = DutyCalculator.calculate(input_data)
        self.assertEqual(result.customs_duty, Decimal('50.00'))
        self.assertEqual(result.rate_type, 'MFN')
        self.assertEqual(result.calculation_method, 'AD_VALOREM')

    def test_negative_value_raises(self):
        """Test that negative customs value raises ValueError"""
        with self.assertRaises(ValueError):
            DutyCalculator.calculate(DutyCalculationInput(
                customs_value=Decimal('-100'),
                hs_code='8471300000',
                duty_rate=Decimal('0.05')
            ))


class TestVATCalculation(unittest.TestCase):
    """Test cases for VAT calculation"""
    
    def test_standard_vat_calculation(self):
        """Test standard VAT calculation"""
        # calculate_vat(customs_value, customs_duty, vat_rate, excise)
        result = calculate_vat(
            customs_value=1000.00,
            customs_duty=100.00,
            vat_rate=0.17,
        )
        # VAT base = 1000 + 100 = 1100
        # VAT = 1100 * 0.17 = 187.00
        self.assertEqual(result, 187.00)
    
    def test_vat_on_zero_duty(self):
        """Test VAT calculation when duty is zero"""
        result = calculate_vat(
            customs_value=5000.00,
            customs_duty=0.00,
            vat_rate=0.17,
        )
        # VAT base = 5000 + 0 = 5000
        # VAT = 5000 * 0.17 = 850.00
        self.assertEqual(result, 850.00)
    
    def test_vat_with_duty(self):
        """Test VAT on customs value plus duty"""
        result = calculate_vat(
            customs_value=1000.00,
            customs_duty=250.00,
            vat_rate=0.17,
        )
        # VAT base = 1000 + 250 = 1250
        # VAT = 1250 * 0.17 = 212.50
        self.assertEqual(result, 212.50)

    def test_vat_with_excise(self):
        """Test VAT includes excise in base"""
        result = calculate_vat(
            customs_value=1000.00,
            customs_duty=50.00,
            vat_rate=0.17,
            excise=200.00,
        )
        # VAT base = 1000 + 50 + 200 = 1250
        # VAT = 1250 * 0.17 = 212.50
        self.assertEqual(result, 212.50)

    def test_vat_reduced_rate(self):
        """Test reduced 7% VAT rate"""
        result = calculate_vat(
            customs_value=2000.00,
            customs_duty=100.00,
            vat_rate=0.07,
        )
        # VAT base = 2100, VAT = 2100 * 0.07 = 147.00
        self.assertEqual(result, 147.00)


class TestExciseCalculation(unittest.TestCase):
    """Test cases for excise tax calculation"""
    
    def test_ad_valorem_excise(self):
        """Test ad valorem excise calculation"""
        # calculate_excise(customs_value, quantity, excise_type, excise_rate, specific_rate)
        result = calculate_excise(
            customs_value=5000.00,
            quantity=100,
            excise_type='AD_VALOREM',
            excise_rate=0.10,
        )
        # 5000 * 0.10 = 500.00
        self.assertEqual(result, 500.00)
    
    def test_specific_excise(self):
        """Test specific (per-unit) excise"""
        result = calculate_excise(
            customs_value=2000.00,
            quantity=1000,
            excise_type='SPECIFIC',
            excise_rate=0.0,
            specific_rate=0.50,
        )
        # 1000 * 0.50 = 500.00
        self.assertEqual(result, 500.00)

    def test_no_excise_on_non_excisable(self):
        """Test zero excise for non-applicable type"""
        result = calculate_excise(
            customs_value=1000.00,
            quantity=10,
            excise_type='NONE',
            excise_rate=0.0,
        )
        self.assertEqual(result, 0.0)


class TestTotalRevenue(unittest.TestCase):
    """Test cases for total revenue calculation"""
    
    def test_total_revenue_calculation(self):
        """Test total revenue (duty + VAT)"""
        # calculate_total_revenue(customs_value, duty_rate, vat_rate, ...)
        result = calculate_total_revenue(
            customs_value=1000.00,
            duty_rate=0.05,
            vat_rate=0.17,
        )
        
        self.assertIn('customs_duty', result)
        self.assertIn('vat', result)
        self.assertIn('total', result)
        
        # Duty = 1000 * 0.05 = 50
        self.assertEqual(result['customs_duty'], 50.00)
        # VAT base = 1000 + 50 = 1050, VAT = 1050 * 0.17 = 178.50
        self.assertEqual(result['vat'], 178.50)
        # Total = 50 + 0 + 178.50 = 228.50
        self.assertEqual(result['total'], 228.50)
    
    def test_total_revenue_zero_duty(self):
        """Test total revenue with zero duty goods"""
        result = calculate_total_revenue(
            customs_value=5000.00,
            duty_rate=0.0,
            vat_rate=0.17,
        )
        
        # Duty = 0
        self.assertEqual(result['customs_duty'], 0.00)
        # VAT = 5000 * 0.17 = 850
        self.assertEqual(result['vat'], 850.00)
        # Total = 0 + 850 = 850
        self.assertEqual(result['total'], 850.00)

    def test_total_revenue_with_preferential(self):
        """Test total revenue with preferential duty"""
        result = calculate_total_revenue(
            customs_value=5000.00,
            duty_rate=0.25,
            vat_rate=0.17,
            preferential=True,
            pref_rate=0.15,
        )
        # Duty = 5000 * 0.15 = 750 (preferential)
        self.assertEqual(result['customs_duty'], 750.00)


class TestRoundingRules(unittest.TestCase):
    """Test cases for currency rounding"""
    
    def test_usd_rounding(self):
        """Test USD rounding to 2 decimals"""
        self.assertEqual(round_currency(100.125, 'USD'), Decimal('100.13'))
        self.assertEqual(round_currency(100.124, 'USD'), Decimal('100.12'))
    
    def test_khr_rounding(self):
        """Test KHR rounding (no decimals)"""
        self.assertEqual(round_currency(1000.5, 'KHR'), Decimal('1001'))
        self.assertEqual(round_currency(1000.4, 'KHR'), Decimal('1000'))
    
    def test_jpy_rounding(self):
        """Test JPY rounding (no decimals)"""
        self.assertEqual(round_currency(1000.5, 'JPY'), Decimal('1001'))
    
    def test_duty_rounding(self):
        """Test duty rounding convenience function"""
        self.assertEqual(round_duty(123.456, 'USD'), Decimal('123.46'))
    
    def test_vat_rounding(self):
        """Test VAT rounding convenience function"""
        self.assertEqual(round_vat(187.001, 'USD'), Decimal('187.00'))

    def test_unknown_currency_defaults_to_usd(self):
        """Test unknown currency falls back to USD rules"""
        self.assertEqual(round_currency(100.125, 'XYZ'), Decimal('100.13'))


if __name__ == '__main__':
    unittest.main()