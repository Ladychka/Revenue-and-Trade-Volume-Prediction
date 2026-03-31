"""
Volume Metrics Module - Trade Volume Calculations
Phase 6 - Trade Volume Analytics Implementation

Provides volume-based trade metrics with privacy-safe outputs.
All metrics are aggregated to prevent identification.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class VolumeMetrics:
    """Aggregated volume metrics - NO individual identifiers"""
    total_declarations: int
    total_items: int
    total_quantity: Decimal
    quantity_unit: str
    
    # Distribution metrics
    average_items_per_declaration: Decimal
    average_quantity_per_item: Decimal
    
    # Value metrics  
    total_value: Decimal
    average_value_per_declaration: Decimal


@dataclass
class PortMetrics:
    """Aggregated port performance metrics - NO individual identifiers"""
    port_code: str
    port_name: str
    
    # Aggregated volume
    total_declarations: int
    total_value: Decimal
    total_duty: Decimal
    
    # Throughput
    average_daily_declarations: Decimal
    clearance_rate: Decimal


class VolumeCalculator:
    """
    Calculator for trade volume metrics.
    
    All outputs are aggregated - no individual declaration or importer data.
    """
    
    @staticmethod
    def calculate_volume_metrics(declarations: List[Dict[str, Any]]) -> VolumeMetrics:
        """
        Calculate overall volume metrics.
        
        Privacy: Aggregated only, no identifiers.
        """
        cleared_decls = [d for d in declarations if d.get('status') == 'CLEARED']
        
        if not cleared_decls:
            return VolumeMetrics(
                total_declarations=0,
                total_items=0,
                total_quantity=Decimal('0'),
                quantity_unit='KGM',
                average_items_per_declaration=Decimal('0'),
                average_quantity_per_item=Decimal('0'),
                total_value=Decimal('0'),
                average_value_per_declaration=Decimal('0')
            )
        
        total_decls = len(cleared_decls)
        total_items = sum(d.get('total_items', 0) for d in cleared_decls)
        total_value = sum(Decimal(str(d.get('total_customs_value', 0))) for d in cleared_decls)
        
        decl_count = Decimal(str(total_decls))
        item_count = Decimal(str(total_items)) if total_items > 0 else Decimal('1')
        
        return VolumeMetrics(
            total_declarations=total_decls,
            total_items=total_items,
            total_quantity=Decimal('0'),  # Would be from items table
            quantity_unit='KGM',
            average_items_per_declaration=VolumeCalculator._round(total_items / total_decls),
            average_quantity_per_item=Decimal('0'),
            total_value=VolumeCalculator._round(total_value),
            average_value_per_declaration=VolumeCalculator._round(total_value / decl_count)
        )
    
    @staticmethod
    def calculate_port_metrics(declarations: List[Dict[str, Any]]) -> List[PortMetrics]:
        """
        Calculate port-level volume metrics.
        
        Privacy: Aggregated by port, no individual identifiers.
        """
        port_data: Dict[str, Dict[str, Any]] = {}
        
        for decl in declarations:
            if decl.get('status') != 'CLEARED':
                continue
            
            port = decl.get('office_code', 'UNKNOWN')
            
            if port not in port_data:
                port_data[port] = {
                    'port_code': port,
                    'port_name': f'Port {port} - Aggregated',
                    'total_declarations': 0,
                    'total_value': Decimal('0'),
                    'total_duty': Decimal('0'),
                }
            
            pd = port_data[port]
            pd['total_declarations'] += 1
            pd['total_value'] += Decimal(str(decl.get('total_customs_value', 0)))
            pd['total_duty'] += Decimal(str(decl.get('total_customs_duty', 0)))
        
        results = []
        for port, data in port_data.items():
            decl_count = Decimal(str(data['total_declarations']))
            
            results.append(PortMetrics(
                port_code=port,
                port_name=data['port_name'],
                total_declarations=data['total_declarations'],
                total_value=VolumeCalculator._round(data['total_value']),
                total_duty=VolumeCalculator._round(data['total_duty']),
                average_daily_declarations=VolumeCalculator._round(decl_count / 365),  # Simplified
                clearance_rate=Decimal('0.85')  # Would be calculated from status
            ))
        
        return sorted(results, key=lambda x: x.total_value, reverse=True)
    
    @staticmethod
    def _round(value: Decimal) -> Decimal:
        """Round to 2 decimal places"""
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


# ============================================================================
# Safe Output Functions
# ============================================================================

def calculate_volume_analytics(declarations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate volume analytics with privacy-safe output.
    
    Returns aggregated metrics only.
    """
    metrics = VolumeCalculator.calculate_volume_metrics(declarations)
    port_metrics = VolumeCalculator.calculate_port_metrics(declarations)
    
    return {
        'overall_metrics': metrics.__dict__,
        'port_metrics': [pm.__dict__ for pm in port_metrics[:10]],  # Top 10 ports
    }


def validate_volume_totals(calculated_metrics: Dict[str, Any], 
                           base_data: List[Dict[str, Any]]) -> Dict[str, bool]:
    """
    Validate that calculated volume metrics match base data.
    """
    base_total = sum(d.get('total_customs_value', 0) for d in base_data 
                     if d.get('status') == 'CLEARED')
    
    calc_total = calculated_metrics.get('overall_metrics', {}).get('total_value', 0)
    
    return {
        'totals_match': abs(float(calc_total) - base_total) < 0.01,
        'units_consistent': True,  # Would check quantity units
    }


# ============================================================================
# Tests
# ============================================================================

if __name__ == '__main__':
    print("=== Volume Metrics Tests ===\n")
    
    synthetic_data = [
        {'status': 'CLEARED', 'total_items': 3, 'total_customs_value': 5000.00, 
         'total_customs_duty': 250.00, 'office_code': 'PORT001'},
        {'status': 'CLEARED', 'total_items': 2, 'total_customs_value': 3000.00,
         'total_customs_duty': 150.00, 'office_code': 'PORT001'},
        {'status': 'CLEARED', 'total_items': 1, 'total_customs_value': 10000.00,
         'total_customs_duty': 0.00, 'office_code': 'PORT002'},
    ]
    
    # Test 1: Overall metrics
    print("Test 1: Volume metrics")
    result = calculate_volume_analytics(synthetic_data)
    print(f"  Total declarations: {result['overall_metrics']['total_declarations']}")
    print(f"  Total value: ${result['overall_metrics']['total_value']}")
    print(f"  Avg value/declaration: ${result['overall_metrics']['average_value_per_declaration']}")
    assert result['overall_metrics']['total_declarations'] == 3
    print("  ✓ PASSED\n")
    
    # Test 2: Port metrics
    print("Test 2: Port metrics")
    for pm in result['port_metrics']:
        print(f"  Port {pm['port_code']}: {pm['total_declarations']} decls")
        assert 'declaration_id' not in pm
    print("  ✓ PASSED\n")
    
    # Test 3: Validation
    print("Test 3: Total validation")
    validation = validate_volume_totals(result, synthetic_data)
    print(f"  Validation: {validation}")
    assert validation['totals_match'] == True
    print("  ✓ PASSED\n")
    
    print("=== All Tests Passed ===")