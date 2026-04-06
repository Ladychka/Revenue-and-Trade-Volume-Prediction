#!/usr/bin/env python3
"""
Unit Tests - Revenue Calculations
Phase 10 - Testing

Tests for revenue calculation modules.
"""

import unittest
from decimal import Decimal
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.revenue.duty_calculator import calculate_duty
from core.revenue.vat_calculator import calculate_vat
from core.revenue.excise_calculator import calculate_excise
from core.revenue.total_revenue import calculate_total_revenue
from core.common.rounding_rules import round_currency, round_duty, round_vat


class TestDutyCalculation(unittest.TestCase):
    """Test cases for customs duty calculation"""
    
    def test_standard_duty_calculation(self):
        """Test standard duty calculation"""
        result = calculate_duty(
            customs_value=1000.00,
            hs_code='8703235010',
            origin_country='US',
            preferential=False
        )
        self.assertEqual(result['duty_rate'], 0.25)
        self.assertEqual(result['customs_duty'], Decimal('250.00'))
    
    def test_preferential_duty_calculation(self):
        """Test preferential duty rate (50% reduction)"""
        result = calculate_duty(
            customs_value=1000.00,
            hs_code='8703235010',
            origin_country='TH',
            preferential=True
        )
        self.assertEqual(result['duty_rate'], 0.125)  # 0.25 * 0.5
        self.assertEqual(result['customs_duty'], Decimal('125.00'))
    
    def test_zero_duty_rate(self):
        """Test zero duty rate (exempt goods)"""
        result = calculate_duty(
            customs_value=5000.00,
            hs_code='8471300000',
            origin_country='CN',
            preferential=False
        )
        self.assertEqual(result['duty_rate'], 0.0)
        self.assertEqual(result['customs_duty'], Decimal('0.00'))
    
    def test_duty_rounding(self):
        """Test duty amount rounding"""
        # Test rounding to 2 decimal places
        result = calculate_duty(
            customs_value=123.45,
            hs_code='6204620000',
            origin_country='IN',
            preferential=False
        )
        self.assertIsNotNone(result['customs_duty'])


class TestVATCalculation(unittest.TestCase):
    """Test cases for VAT calculation"""
    
    def test_standard_vat_calculation(self):
        """Test standard VAT calculation"""
        result = calculate_vat(
            customs_value=1000.00,
            duty_amount=100.00,
            hs_code='8703235010'
        )
        # VAT base = 1000 + 100 = 1100
        # VAT = 1100 * 0.17 = 187
        self.assertEqual(result['vat_rate'], 0.17)
        self.assertEqual(result['vat_amount'], Decimal('187.00'))
    
    def test_vat_on_zero_duty(self):
        """Test VAT calculation when duty is zero"""
        result = calculate_vat(
            customs_value=5000.00,
            duty_amount=0.00,
            hs_code='8471300000'
        )
        self.assertEqual(result['vat_amount'], Decimal('850.00'))  # 5000 * 0.17
    
    def test_vat_with_duty(self):
        """Test VAT on customs value plus duty"""
        result = calculate_vat(
            customs_value=1000.00,
            duty_amount=250.00,
            hs_code='8703235010'
        )
        # VAT base = 1000 + 250 = 1250
        # VAT = 1250 * 0.17 = 212.50
        self.assertEqual(result['vat_amount'], Decimal('212.50'))


class TestExciseCalculation(unittest.TestCase):
    """Test cases for excise tax calculation"""
    
    def test_excise_on_vehicles(self):
        """Test excise tax on vehicles"""
        result = calculate_excise(
            customs_value=30000.00,
            hs_code='8703235010',
            quantity=1
        )
        self.assertIsNotNone(result)
        self.assertIn('excise_rate', result)
    
    def test_no_excise_on_non_excisable(self):
        """Test no excise on non-excisable goods"""
        result = calculate_excise(
            customs_value=1000.00,
            hs_code='8471300000',
            quantity=10
        )
        self.assertEqual(result.get('excise_amount', Decimal('0')), Decimal('0'))


class TestTotalRevenue(unittest.TestCase):
    """Test cases for total revenue calculation"""
    
    def test_total_revenue_calculation(self):
        """Test total revenue (duty + VAT + excise)"""
        result = calculate_total_revenue(
            customs_value=10000.00,
            hs_code='8703235010',
            origin_country='US',
            quantity=1
        )
        
        self.assertIn('total_revenue', result)
        self.assertIn('customs_duty', result)
        self.assertIn('vat_amount', result)
        
        # Total should be sum of components
        expected_total = (
            result.get('customs_duty', 0) + 
            result.get('vat_amount', 0) + 
            result.get('excise_amount', 0)
        )
        self.assertEqual(result['total_revenue'], expected_total)
    
    def test_total_revenue_zero_duty(self):
        """Test total revenue with zero duty goods"""
        result = calculate_total_revenue(
            customs_value=5000.00,
            hs_code='8471300000',
            origin_country='CN',
            quantity=5
        )
        
        # Duty should be 0, but VAT still applies
        self.assertEqual(result.get('customs_duty', 0), Decimal('0'))
        self.assertGreater(result.get('vat_amount', 0), 0)


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
    
    def test_duty_rounding(self):
        """Test duty rounding"""
        self.assertEqual(round_duty(123.456, 'USD'), Decimal('123.46'))
    
    def test_vat_rounding(self):
        """Test VAT rounding"""
        self.assertEqual(round_vat(187.001, 'USD'), Decimal('187.00'))


if __name__ == '__main__':
    unittest.main()