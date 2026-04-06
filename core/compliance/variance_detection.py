#!/usr/bin/env python3
"""
Variance Detection Module - Revenue Variance Analysis
Phase 6 - Compliance Analytics Implementation

Detects variance between declared revenue and expected revenue patterns.
All outputs are aggregated to maintain privacy.
"""

from decimal import Decimal
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# Variance Detection Configuration
# ============================================================================

VARIANCE_THRESHOLDS = {
    'warning': 0.10,    # 10% variance - warning
    'critical': 0.25,   # 25% variance - critical
}


@dataclass
class VarianceResult:
    """Variance detection result"""
    period: str
    declared_revenue: Decimal
    expected_revenue: Decimal
    variance_amount: Decimal
    variance_percentage: Decimal
    severity: str  # NORMAL, WARNING, CRITICAL


class VarianceDetector:
    """
    Detect revenue variance from expected patterns.
    
    Privacy: All calculations are aggregated, no individual declarations exposed.
    """
    
    @staticmethod
    def detect_variance(historical_data: List[Dict[str, Any]], 
                       current_data: Dict[str, Any],
                       method: str = 'simple_average') -> VarianceResult:
        """
        Detect variance between current and historical data.
        
        Args:
            historical_data: List of historical period data
            current_data: Current period data
            method: 'simple_average', 'weighted', or 'trend'
        
        Returns:
            VarianceResult object
        """
        if not historical_data:
            return VarianceResult(
                period=current_data.get('period', 'UNKNOWN'),
                declared_revenue=Decimal('0'),
                expected_revenue=Decimal('0'),
                variance_amount=Decimal('0'),
                variance_percentage=Decimal('0'),
                severity='NORMAL'
            )
        
        # Calculate expected revenue based on method
        expected = VarianceDetector._calculate_expected(
            historical_data, current_data, method
        )
        
        declared = Decimal(str(current_data.get('declared_revenue', 0)))
        
        # Calculate variance
        variance_amount = declared - expected
        variance_percentage = (variance_amount / expected) if expected > 0 else Decimal('0')
        
        # Determine severity
        severity = VarianceDetector._determine_severity(abs(variance_percentage))
        
        return VarianceResult(
            period=current_data.get('period', 'UNKNOWN'),
            declared_revenue=declared,
            expected_revenue=expected.quantize(Decimal('0.01')),
            variance_amount=variance_amount.quantize(Decimal('0.01')),
            variance_percentage=variance_percentage.quantize(Decimal('0.01')),
            severity=severity
        )
    
    @staticmethod
    def _calculate_expected(historical_data: List[Dict[str, Any]],
                           current_data: Dict[str, Any],
                           method: str) -> Decimal:
        """Calculate expected revenue based on historical data"""
        
        if method == 'simple_average':
            # Simple average of historical periods
            total = sum(Decimal(str(d.get('revenue', 0))) for d in historical_data)
            count = len(historical_data)
            return total / count if count > 0 else Decimal('0')
        
        elif method == 'weighted':
            # Weighted average (more recent = higher weight)
            total = Decimal('0')
            weight_sum = Decimal('0')
            
            for i, d in enumerate(historical_data):
                weight = Decimal(str(i + 1))  # Most recent has highest weight
                revenue = Decimal(str(d.get('revenue', 0)))
                total += revenue * weight
                weight_sum += weight
            
            return total / weight_sum if weight_sum > 0 else Decimal('0')
        
        elif method == 'trend':
            # Linear trend projection
            if len(historical_data) < 2:
                return Decimal(str(historical_data[0].get('revenue', 0))) if historical_data else Decimal('0')
            
            # Simple linear regression
            n = len(historical_data)
            x_mean = (n - 1) / 2  # Centered at middle
            
            revenues = [Decimal(str(d.get('revenue', 0))) for d in historical_data]
            y_mean = sum(revenues) / n
            
            # Calculate slope
            numerator = sum((i - x_mean) * (revenues[i] - y_mean) for i in range(n))
            denominator = sum((i - x_mean) ** 2 for i in range(n))
            
            slope = numerator / denominator if denominator != 0 else Decimal('0')
            
            # Project next period
            expected = y_mean + slope * n
            return expected if expected > 0 else Decimal('0')
        
        else:
            return Decimal('0')
    
    @staticmethod
    def _determine_severity(variance_pct: Decimal) -> str:
        """Determine severity based on variance percentage"""
        abs_variance = abs(variance_pct)
        
        if abs_variance >= VARIANCE_THRESHOLDS['critical']:
            return 'CRITICAL'
        elif abs_variance >= VARIANCE_THRESHOLDS['warning']:
            return 'WARNING'
        else:
            return 'NORMAL'
    
    @staticmethod
    def batch_detect(historical_periods: List[List[Dict[str, Any]]],
                    current_period: Dict[str, Any]) -> List[VarianceResult]:
        """
        Detect variance using multiple methods and return all results.
        
        Args:
            historical_periods: List of historical data for different methods
            current_period: Current period data
        
        Returns:
            List of VarianceResult for each method
        """
        results = []
        methods = ['simple_average', 'weighted', 'trend']
        
        for i, method in enumerate(methods):
            historical = historical_periods[i] if i < len(historical_periods) else []
            result = VarianceDetector.detect_variance(historical, current_period, method)
            results.append(result)
        
        return results


def detect_revenue_variance(historical_data: List[Dict[str, Any]],
                           current_data: Dict[str, Any]) -> VarianceResult:
    """
    Public interface for variance detection.
    """
    return VarianceDetector.detect_variance(historical_data, current_data, 'simple_average')


# ============================================================================
# Tests
# ============================================================================

if __name__ == '__main__':
    print("=== Variance Detection Tests ===\n")
    
    # Test data
    historical = [
        {'period': '2024-01', 'revenue': 100000},
        {'period': '2024-02', 'revenue': 105000},
        {'period': '2024-03', 'revenue': 98000},
    ]
    
    current = {'period': '2024-04', 'revenue': 130000}
    
    # Test 1: Variance detection
    print("Test 1: Variance Detection")
    result = detect_revenue_variance(historical, current)
    print(f"  Period: {result.period}")
    print(f"  Declared: ${result.declared_revenue}")
    print(f"  Expected: ${result.expected_revenue}")
    print(f"  Variance: ${result.variance_amount} ({result.variance_percentage * 100}%)")
    print(f"  Severity: {result.severity}")
    print("  ✓ Variance detected\n")
    
    # Test 2: Warning threshold
    print("Test 2: Warning Threshold (10%)")
    current_warning = {'period': '2024-04', 'revenue': 115000}
    result2 = detect_revenue_variance(historical, current_warning)
    assert result2.severity == 'WARNING'
    print(f"  Variance: {result2.variance_percentage * 100}% -> Severity: {result2.severity}")
    print("  ✓ Warning threshold works\n")
    
    # Test 3: Normal threshold
    print("Test 3: Normal Threshold (<10%)")
    current_normal = {'period': '2024-04', 'revenue': 103000}
    result3 = detect_revenue_variance(historical, current_normal)
    assert result3.severity == 'NORMAL'
    print(f"  Variance: {result3.variance_percentage * 100}% -> Severity: {result3.severity}")
    print("  ✓ Normal threshold works\n")
    
    print("=== All Variance Detection Tests Passed ===")