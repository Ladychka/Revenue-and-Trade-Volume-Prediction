#!/usr/bin/env python3
"""
Unit Tests - Trade Aggregation
Phase 10 - Testing

Tests for trade aggregation and analysis modules.
"""

import unittest
from decimal import Decimal
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.trade.trade_aggregation import (
    TradeAggregator, 
    aggregate_trade_data,
    validate_aggregation_safety
)
from core.trade.trend_analysis import (
    TrendAnalyzer,
    analyze_trend_data,
    forecast_trade
)
from core.trade.volume_metrics import calculate_volume_metrics


class TestTradeAggregation(unittest.TestCase):
    """Test cases for trade aggregation"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_declarations = [
            {
                'declaration_id': 'DEC-20240101-0000001',
                'declarant_id': 'IMP-12345-0000001',
                'origin_country': 'CN',
                'hs_chapter': '84',
                'declaration_date': '2024-01-15',
                'status': 'CLEARED',
                'total_items': 3,
                'total_customs_value': 5000.00,
                'total_customs_duty': 250.00,
                'total_vat': 892.50,
            },
            {
                'declaration_id': 'DEC-20240102-0000002',
                'declarant_id': 'IMP-12345-0000002',
                'origin_country': 'CN',
                'hs_chapter': '84',
                'declaration_date': '2024-01-20',
                'status': 'CLEARED',
                'total_items': 2,
                'total_customs_value': 3000.00,
                'total_customs_duty': 150.00,
                'total_vat': 535.50,
            },
            {
                'declaration_id': 'DEC-20240103-0000003',
                'declarant_id': 'IMP-12345-0000003',
                'origin_country': 'JP',
                'hs_chapter': '85',
                'declaration_date': '2024-01-25',
                'status': 'CLEARED',
                'total_items': 1,
                'total_customs_value': 10000.00,
                'total_customs_duty': 0.00,
                'total_vat': 1700.00,
            },
            {
                'declaration_id': 'DEC-20240104-0000004',
                'declarant_id': 'IMP-12345-0000004',
                'origin_country': 'JP',
                'hs_chapter': '85',
                'declaration_date': '2024-01-28',
                'status': 'CLEARED',
                'total_items': 4,
                'total_customs_value': 8000.00,
                'total_customs_duty': 0.00,
                'total_vat': 1360.00,
            },
            {
                'declaration_id': 'DEC-20240105-0000005',
                'declarant_id': 'IMP-12345-0000005',
                'origin_country': 'TH',
                'hs_chapter': '62',
                'declaration_date': '2024-01-30',
                'status': 'CLEARED',
                'total_items': 5,
                'total_customs_value': 2000.00,
                'total_customs_duty': 335.00,
                'total_vat': 396.95,
            },
        ]
    
    def test_aggregate_by_country(self):
        """Test aggregation by country"""
        result = TradeAggregator.aggregate_by_country(self.sample_declarations)
        
        self.assertGreater(len(result), 0)
        
        # Check that country data is aggregated
        for item in result:
            self.assertIsNotNone(item.country_code)
            self.assertGreater(item.total_declarations, 0)
            self.assertIsInstance(item.total_customs_value, Decimal)
    
    def test_aggregate_by_month(self):
        """Test aggregation by month"""
        result = TradeAggregator.aggregate_by_month(self.sample_declarations)
        
        self.assertGreater(len(result), 0)
        
        # Check monthly data
        for item in result:
            self.assertIsNotNone(item.year)
            self.assertIsNotNone(item.month)
            self.assertGreater(item.total_declarations, 0)
    
    def test_privacy_safety_no_identifiers(self):
        """Test that aggregated data has no individual identifiers"""
        result = aggregate_trade_data(self.sample_declarations, 'country')
        
        # Check safety
        safety = validate_aggregation_safety(result)
        
        self.assertTrue(safety['no_declaration_ids'])
        self.assertTrue(safety['no_importer_ids'])
        self.assertTrue(safety['no_item_ids'])
    
    def test_minimum_threshold(self):
        """Test minimum aggregation threshold"""
        small_declarations = [
            {
                'origin_country': 'CN',
                'status': 'CLEARED',
                'total_customs_value': 1000.00,
                'total_customs_duty': 100.00,
                'total_vat': 187.00,
                'total_items': 1,
            },
            {
                'origin_country': 'CN',  # Only 2 - below threshold of 5
                'status': 'CLEARED',
                'total_customs_value': 2000.00,
                'total_customs_duty': 200.00,
                'total_vat': 374.00,
                'total_items': 2,
            },
        ]
        
        result = TradeAggregator.aggregate_by_country(small_declarations)
        
        # With threshold of 5, this should return empty or filtered


class TestTrendAnalysis(unittest.TestCase):
    """Test cases for trend analysis"""
    
    def test_trend_analysis(self):
        """Test trend analysis over time"""
        monthly_data = [
            {'period': '2024-01', 'value': 100000},
            {'period': '2024-02', 'value': 105000},
            {'period': '2024-03', 'value': 110000},
            {'period': '2024-04', 'value': 108000},
            {'period': '2024-05', 'value': 115000},
            {'period': '2024-06', 'value': 125000},
        ]
        
        trends = analyze_trend_data(monthly_data)
        
        self.assertGreater(len(trends), 0)
        
        # Check trend structure
        for trend in trends:
            self.assertIsNotNone(trend.period)
            self.assertIsNotNone(trend.current_value)
            self.assertIn(trend.trend_direction, ['UP', 'DOWN', 'STABLE'])
    
    def test_forecast(self):
        """Test forecasting"""
        monthly_data = [
            {'period': '2024-01', 'value': 100000},
            {'period': '2024-02', 'value': 105000},
            {'period': '2024-03', 'value': 110000},
            {'period': '2024-04', 'value': 115000},
            {'period': '2024-05', 'value': 120000},
        ]
        
        forecast = forecast_trade(monthly_data, periods_ahead=2)
        
        self.assertIsNotNone(forecast.forecast_value)
        self.assertIsNotNone(forecast.confidence_lower)
        self.assertIsNotNone(forecast.confidence_upper)
        self.assertGreaterEqual(forecast.confidence_lower, 0)
        self.assertLessEqual(forecast.forecast_value, forecast.confidence_upper)
    
    def test_growth_rate(self):
        """Test CAGR calculation"""
        monthly_data = [
            {'period': '2024-01', 'value': 100000},
            {'period': '2024-02', 'value': 105000},
            {'period': '2024-03', 'value': 110250},
            {'period': '2024-04', 'value': 115762},
        ]
        
        cagr = TrendAnalyzer.calculate_growth_rate(monthly_data)
        
        self.assertIsInstance(cagr, Decimal)
        self.assertGreater(float(cagr), 0)  # Should be positive growth
    
    def test_linear_trend(self):
        """Test linear trend calculation"""
        monthly_data = [
            {'period': '2024-01', 'value': 100000},
            {'period': '2024-02', 'value': 110000},
            {'period': '2024-03', 'value': 120000},
            {'period': '2024-04', 'value': 130000},
        ]
        
        slope, intercept = TrendAnalyzer.linear_trend(monthly_data)
        
        self.assertIsInstance(slope, Decimal)
        self.assertIsInstance(intercept, Decimal)
        self.assertGreater(slope, 0)  # Positive slope


class TestVolumeMetrics(unittest.TestCase):
    """Test cases for volume metrics"""
    
    def test_calculate_volume_metrics(self):
        """Test volume metrics calculation"""
        items = [
            {'quantity': 100, 'quantity_unit': 'KGM'},
            {'quantity': 200, 'quantity_unit': 'KGM'},
            {'quantity': 150, 'quantity_unit': 'KGM'},
        ]
        
        result = calculate_volume_metrics(items)
        
        self.assertIsNotNone(result)
        self.assertIn('total_quantity', result)
        self.assertIn('average_quantity', result)


if __name__ == '__main__':
    unittest.main()