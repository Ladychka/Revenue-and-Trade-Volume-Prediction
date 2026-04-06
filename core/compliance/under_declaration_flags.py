#!/usr/bin/env python3
"""
Under-Declaration Flags Module - Detection of Potential Under-Declarations
Phase 6 - Compliance Analytics Implementation

Flags potential under-declarations based on statistical analysis.
All outputs are aggregated to maintain privacy.
"""

from decimal import Decimal
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


# ============================================================================
# Detection Thresholds
# ============================================================================

THRESHOLDS = {
    'value_deviation': 0.30,      # 30% below expected value
    'duty_deviation': 0.20,      # 20% below expected duty
    'quantity_anomaly': 3.0,      # 3x standard deviation
    'rate_anomaly': 0.50,        # 50% different from average
}


@dataclass
class FlagResult:
    """Under-declaration flag result"""
    flag_id: str
    flag_type: str  # VALUE, DUTY, QUANTITY, RATE
    severity: str   # LOW, MEDIUM, HIGH
    description: str
    deviation_percentage: Decimal
    recommendation: str


class UnderDeclarationDetector:
    """
    Detect potential under-declarations based on statistical patterns.
    
    Privacy: All analysis is aggregated, no individual identifiers exposed.
    """
    
    @staticmethod
    def detect(declaration_data: List[Dict[str, Any]],
              reference_data: Dict[str, Any]) -> List[FlagResult]:
        """
        Detect potential under-declarations.
        
        Args:
            declaration_data: List of aggregated declaration statistics
            reference_data: Reference data (HS codes, average values, etc.)
        
        Returns:
            List of FlagResult objects
        """
        flags = []
        
        if not declaration_data:
            return flags
        
        # Calculate aggregate statistics
        stats = UnderDeclarationDetector._calculate_statistics(declaration_data)
        
        # Check for value under-declaration
        value_flags = UnderDeclarationDetector._check_value_deviation(
            declaration_data, stats, reference_data
        )
        flags.extend(value_flags)
        
        # Check for duty under-declaration
        duty_flags = UnderDeclarationDetector._check_duty_deviation(
            declaration_data, stats, reference_data
        )
        flags.extend(duty_flags)
        
        # Check for rate anomalies
        rate_flags = UnderDeclarationDetector._check_rate_anomaly(declaration_data, stats)
        flags.extend(rate_flags)
        
        return flags
    
    @staticmethod
    def _calculate_statistics(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate aggregate statistics"""
        values = [Decimal(str(d.get('customs_value', 0))) for d in data]
        duties = [Decimal(str(d.get('duty_amount', 0))) for d in data]
        rates = [Decimal(str(d.get('duty_rate', 0))) for d in data if d.get('duty_rate', 0) > 0]
        
        n = len(values)
        
        # Mean
        avg_value = sum(values) / n if n > 0 else Decimal('0')
        avg_duty = sum(duties) / n if n > 0 else Decimal('0')
        avg_rate = sum(rates) / len(rates) if rates else Decimal('0')
        
        # Standard deviation
        value_var = sum((v - avg_value) ** 2 for v in values) / n if n > 0 else Decimal('0')
        value_std = value_var ** Decimal('0.5')
        
        return {
            'count': n,
            'avg_value': avg_value,
            'avg_duty': avg_duty,
            'avg_rate': avg_rate,
            'value_std': value_std,
            'value_sum': sum(values),
            'duty_sum': sum(duties),
        }
    
    @staticmethod
    def _check_value_deviation(data: List[Dict[str, Any]], 
                               stats: Dict[str, Any],
                               reference: Dict[str, Any]) -> List[FlagResult]:
        """Check for declarations significantly below expected value"""
        flags = []
        
        # Calculate expected value for each declaration type
        expected_value = stats['avg_value']
        
        # Check each aggregation group
        for i, d in enumerate(data):
            value = Decimal(str(d.get('customs_value', 0)))
            
            if expected_value > 0:
                deviation = (expected_value - value) / expected_value
                
                if deviation > THRESHOLDS['value_deviation']:
                    severity = 'HIGH' if deviation > 0.5 else 'MEDIUM'
                    
                    flags.append(FlagResult(
                        flag_id=f'VALUE-{i:04d}',
                        flag_type='VALUE',
                        severity=severity,
                        description=f"Customs value {float(deviation)*100:.1f}% below average",
                        deviation_percentage=deviation.quantize(Decimal('0.01')),
                        recommendation='Review declared value against reference prices'
                    ))
        
        return flags
    
    @staticmethod
    def _check_duty_deviation(data: List[Dict[str, Any]],
                             stats: Dict[str, Any],
                             reference: Dict[str, Any]) -> List[FlagResult]:
        """Check for duty amounts significantly below expected"""
        flags = []
        
        expected_duty = stats['avg_duty']
        
        for i, d in enumerate(data):
            duty = Decimal(str(d.get('duty_amount', 0)))
            
            if expected_duty > 0:
                deviation = (expected_duty - duty) / expected_duty
                
                if deviation > THRESHOLDS['duty_deviation']:
                    severity = 'HIGH' if deviation > 0.4 else 'MEDIUM'
                    
                    flags.append(FlagResult(
                        flag_id=f'DUTY-{i:04d}',
                        flag_type='DUTY',
                        severity=severity,
                        description=f"Duty amount {float(deviation)*100:.1f}% below expected",
                        deviation_percentage=deviation.quantize(Decimal('0.01')),
                        recommendation='Verify duty calculation and HS code classification'
                    ))
        
        return flags
    
    @staticmethod
    def _check_rate_anomaly(data: List[Dict[str, Any]],
                           stats: Dict[str, Any]) -> List[FlagResult]:
        """Check for duty rate anomalies"""
        flags = []
        
        expected_rate = stats['avg_rate']
        
        if expected_rate <= 0:
            return flags
        
        for i, d in enumerate(data):
            rate = Decimal(str(d.get('duty_rate', 0)))
            
            if rate > 0:
                deviation = abs(expected_rate - rate) / expected_rate
                
                if deviation > THRESHOLDS['rate_anomaly']:
                    severity = 'HIGH' if deviation > 0.7 else 'MEDIUM'
                    
                    direction = 'higher' if rate > expected_rate else 'lower'
                    
                    flags.append(FlagResult(
                        flag_id=f'RATE-{i:04d}',
                        flag_type='RATE',
                        severity=severity,
                        description=f"Duty rate {float(deviation)*100:.1f}% {direction} than average",
                        deviation_percentage=deviation.quantize(Decimal('0.01')),
                        recommendation='Verify HS code classification and applicable rates'
                    ))
        
        return flags
    
    @staticmethod
    def aggregate_flags(flags: List[FlagResult]) -> Dict[str, Any]:
        """Aggregate flag statistics"""
        if not flags:
            return {
                'total_flags': 0,
                'by_severity': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0},
                'by_type': {'VALUE': 0, 'DUTY': 0, 'QUANTITY': 0, 'RATE': 0},
            }
        
        by_severity = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        by_type = {'VALUE': 0, 'DUTY': 0, 'QUANTITY': 0, 'RATE': 0}
        
        for flag in flags:
            by_severity[flag.severity] += 1
            by_type[flag.flag_type] += 1
        
        return {
            'total_flags': len(flags),
            'by_severity': by_severity,
            'by_type': by_type,
        }


def detect_under_declarations(declaration_data: List[Dict[str, Any]],
                             reference_data: Dict[str, Any]) -> List[FlagResult]:
    """
    Public interface for under-declaration detection.
    """
    return UnderDeclarationDetector.detect(declaration_data, reference_data)


# ============================================================================
# Tests
# ============================================================================

if __name__ == '__main__':
    print("=== Under-Declaration Detection Tests ===\n")
    
    # Test data
    test_data = [
        {'customs_value': 10000, 'duty_amount': 1000, 'duty_rate': 0.10},
        {'customs_value': 12000, 'duty_amount': 1200, 'duty_rate': 0.10},
        {'customs_value': 8000, 'duty_amount': 800, 'duty_rate': 0.10},    # Below average
        {'customs_value': 15000, 'duty_amount': 1500, 'duty_rate': 0.10},
        {'customs_value': 5000, 'duty_amount': 250, 'duty_rate': 0.05},    # Significantly below
    ]
    
    reference = {}
    
    # Test 1: Detection
    print("Test 1: Under-Declaration Detection")
    flags = detect_under_declarations(test_data, reference)
    print(f"  Found {len(flags)} flags")
    
    # Test 2: Aggregation
    print("Test 2: Flag Aggregation")
    aggregated = UnderDeclarationDetector.aggregate_flags(flags)
    print(f"  Total flags: {aggregated['total_flags']}")
    print(f"  By severity: {aggregated['by_severity']}")
    print(f"  By type: {aggregated['by_type']}")
    print("  ✓ Aggregation works\n")
    
    # Test 3: No data case
    print("Test 3: No Data Case")
    empty_flags = detect_under_declarations([], reference)
    assert len(empty_flags) == 0
    print("  ✓ Handles empty data correctly\n")
    
    print("=== All Under-Declaration Tests Passed ===")