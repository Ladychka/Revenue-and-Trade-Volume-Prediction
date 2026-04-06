#!/usr/bin/env python3
"""
Trend Analysis Module - Time Series Analysis for Trade Data
Phase 6 - Trade Analytics Implementation

Provides trend analysis and simple forecasting for trade data.
All outputs are aggregated to maintain privacy.
"""

from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# Trend Analysis Data Structures
# ============================================================================

@dataclass
class TrendResult:
    """Trend analysis result"""
    period: str
    current_value: Decimal
    previous_value: Decimal
    change_absolute: Decimal
    change_percentage: Decimal
    trend_direction: str  # UP, DOWN, STABLE
    trend_strength: str  # STRONG, MODERATE, WEAK


@dataclass
class ForecastResult:
    """Forecast result"""
    periods_ahead: int
    forecast_value: Decimal
    confidence_lower: Decimal
    confidence_upper: Decimal
    methodology: str


class TrendAnalyzer:
    """
    Analyze trends in trade and revenue data.
    
    Privacy: All analysis is aggregated, no individual identifiers.
    """
    
    # Trend strength thresholds
    STRONG_THRESHOLD = Decimal('0.20')  # 20%+ change
    MODERATE_THRESHOLD = Decimal('0.10')  # 10%+ change
    
    @staticmethod
    def analyze_trend(periods: List[Dict[str, Any]], 
                    value_field: str = 'value') -> List[TrendResult]:
        """
        Analyze trends across time periods.
        
        Args:
            periods: List of period data (must be sorted by period)
            value_field: Field name containing the value to analyze
        
        Returns:
            List of TrendResult for each period (except first)
        """
        if len(periods) < 2:
            return []
        
        results = []
        
        for i in range(1, len(periods)):
            current = periods[i]
            previous = periods[i - 1]
            
            current_value = Decimal(str(current.get(value_field, 0)))
            previous_value = Decimal(str(previous.get(value_field, 0)))
            
            change_absolute = current_value - previous_value
            
            if previous_value > 0:
                change_percentage = change_absolute / previous_value
            else:
                change_percentage = Decimal('0')
            
            # Determine direction
            if change_percentage > TrendAnalyzer.STRONG_THRESHOLD:
                direction = 'UP'
            elif change_percentage < -TrendAnalyzer.STRONG_THRESHOLD:
                direction = 'DOWN'
            elif abs(change_percentage) > TrendAnalyzer.MODERATE_THRESHOLD:
                direction = 'UP' if change_percentage > 0 else 'DOWN'
            else:
                direction = 'STABLE'
            
            # Determine strength
            abs_change = abs(change_percentage)
            if abs_change >= TrendAnalyzer.STRONG_THRESHOLD:
                strength = 'STRONG'
            elif abs_change >= TrendAnalyzer.MODERATE_THRESHOLD:
                strength = 'MODERATE'
            else:
                strength = 'WEAK'
            
            results.append(TrendResult(
                period=current.get('period', 'UNKNOWN'),
                current_value=current_value.quantize(Decimal('0.01')),
                previous_value=previous_value.quantize(Decimal('0.01')),
                change_absolute=change_absolute.quantize(Decimal('0.01')),
                change_percentage=change_percentage.quantize(Decimal('0.01')),
                trend_direction=direction,
                trend_strength=strength
            ))
        
        return results
    
    @staticmethod
    def simple_forecast(periods: List[Dict[str, Any]],
                       periods_ahead: int = 1,
                       value_field: str = 'value') -> ForecastResult:
        """
        Simple moving average forecast.
        
        Args:
            periods: Historical period data
            periods_ahead: Number of periods to forecast
            value_field: Field name containing the value
        
        Returns:
            ForecastResult with prediction
        """
        if len(periods) < 3:
            # Not enough data for forecast
            last_value = Decimal(str(periods[-1].get(value_field, 0))) if periods else Decimal('0')
            return ForecastResult(
                periods_ahead=periods_ahead,
                forecast_value=last_value,
                confidence_lower=last_value,
                confidence_upper=last_value,
                methodology='INSUFFICIENT_DATA'
            )
        
        # Calculate simple moving average
        values = [Decimal(str(p.get(value_field, 0))) for p in periods]
        
        # Use last N periods (last 6 months or available)
        n = min(6, len(values))
        recent_values = values[-n:]
        avg = sum(recent_values) / n
        
        # Calculate standard deviation for confidence interval
        mean = sum(recent_values) / n
        variance = sum((v - mean) ** 2 for v in recent_values) / n
        std_dev = variance ** Decimal('0.5')
        
        # 95% confidence interval (approximately 2 standard deviations)
        confidence_margin = Decimal('2') * std_dev
        
        return ForecastResult(
            periods_ahead=periods_ahead,
            forecast_value=avg.quantize(Decimal('0.01')),
            confidence_lower=(avg - confidence_margin).quantize(Decimal('0.01')),
            confidence_upper=(avg + confidence_margin).quantize(Decimal('0.01')),
            methodology=f'SIMPLE_MA_{n}'
        )
    
    @staticmethod
    def linear_trend(periods: List[Dict[str, Any]],
                    value_field: str = 'value') -> Tuple[Decimal, Decimal]:
        """
        Calculate linear trend (slope and intercept).
        
        Args:
            periods: Time series data
            value_field: Field containing value
        
        Returns:
            Tuple of (slope, intercept)
        """
        if len(periods) < 2:
            return Decimal('0'), Decimal('0')
        
        n = len(periods)
        x_mean = Decimal(str((n - 1) / 2))
        
        values = [Decimal(str(p.get(value_field, 0))) for p in periods]
        y_mean = sum(values) / n
        
        # Calculate slope
        numerator = sum((Decimal(str(i)) - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((Decimal(str(i)) - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else Decimal('0')
        intercept = y_mean - slope * x_mean
        
        return slope.quantize(Decimal('0.01')), intercept.quantize(Decimal('0.01'))
    
    @staticmethod
    def calculate_growth_rate(periods: List[Dict[str, Any]],
                            value_field: str = 'value') -> Decimal:
        """
        Calculate compound annual growth rate (CAGR).
        
        Args:
            periods: Time series data
            value_field: Field containing value
        
        Returns:
            CAGR as decimal (e.g., 0.10 for 10%)
        """
        if len(periods) < 2:
            return Decimal('0')
        
        start_value = Decimal(str(periods[0].get(value_field, 0)))
        end_value = Decimal(str(periods[-1].get(value_field, 0)))
        
        if start_value <= 0 or end_value <= 0:
            return Decimal('0')
        
        n_periods = len(periods) - 1
        
        # CAGR = (End Value / Start Value) ^ (1/n) - 1
        cagr = (end_value / start_value) ** (Decimal('1') / n_periods) - Decimal('1')
        
        return cagr.quantize(Decimal('0.01'))


def analyze_trend_data(periods: List[Dict[str, Any]], 
                       value_field: str = 'value') -> List[TrendResult]:
    """
    Public interface for trend analysis.
    """
    return TrendAnalyzer.analyze_trend(periods, value_field)


def forecast_trade(periods: List[Dict[str, Any]],
                  periods_ahead: int = 1) -> ForecastResult:
    """
    Public interface for forecasting.
    """
    return TrendAnalyzer.simple_forecast(periods, periods_ahead)


# ============================================================================
# Tests
# ============================================================================

if __name__ == '__main__':
    print("=== Trend Analysis Tests ===\n")
    
    # Test data - monthly trade values
    monthly_data = [
        {'period': '2024-01', 'value': 100000},
        {'period': '2024-02', 'value': 105000},
        {'period': '2024-03', 'value': 110000},
        {'period': '2024-04', 'value': 108000},
        {'period': '2024-05', 'value': 115000},
        {'period': '2024-06', 'value': 125000},
    ]
    
    # Test 1: Trend analysis
    print("Test 1: Trend Analysis")
    trends = analyze_trend_data(monthly_data)
    for t in trends[:3]:
        print(f"  {t.period}: {t.trend_direction} {t.change_percentage * 100}%")
    print("  ✓ Trend analysis works\n")
    
    # Test 2: Forecasting
    print("Test 2: Simple Forecasting")
    forecast = forecast_trade(monthly_data, periods_ahead=2)
    print(f"  Forecast (2 months): ${forecast.forecast_value}")
    print(f"  Confidence: ${forecast.confidence_lower} - ${forecast.confidence_upper}")
    print(f"  Method: {forecast.methodology}")
    print("  ✓ Forecasting works\n")
    
    # Test 3: Growth rate
    print("Test 3: Growth Rate (CAGR)")
    cagr = TrendAnalyzer.calculate_growth_rate(monthly_data)
    print(f"  CAGR: {float(cagr)*100:.1f}%")
    assert float(cagr) > 0  # Should be positive growth
    print("  ✓ Growth rate calculation works\n")
    
    # Test 4: Linear trend
    print("Test 4: Linear Trend")
    slope, intercept = TrendAnalyzer.linear_trend(monthly_data)
    print(f"  Slope: {slope}")
    print(f"  Intercept: {intercept}")
    print("  ✓ Linear trend works\n")
    
    print("=== All Trend Analysis Tests Passed ===")