#!/usr/bin/env python3
"""
Risk Scoring Module - Entity Risk Assessment
Phase 6 - Compliance Analytics Implementation

Provides risk scoring for importers/traders based on declaration patterns.
All outputs are aggregated to maintain privacy.
"""

from decimal import Decimal
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta


# ============================================================================
# Risk Scoring Configuration
# ============================================================================

# Risk factors and their weights
RISK_FACTORS = {
    'high_value': {'weight': 0.25, 'threshold': 50000},
    'high_frequency': {'weight': 0.20, 'threshold': 10},  # declarations per month
    'duty_variance': {'weight': 0.20, 'threshold': 0.15},  # 15% variance from average
    'rejected_count': {'weight': 0.15, 'threshold': 2},
    'late_payment': {'weight': 0.10, 'threshold': 3},  # days late
    'preferential_abuse': {'weight': 0.10, 'threshold': 0.3},  # 30% preferential rate usage
}


@dataclass
class RiskScore:
    """Risk score result for an entity"""
    entity_id: str
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    risk_score: Decimal
    risk_factors: Dict[str, Any]
    recommendation: str


class RiskScorer:
    """
    Calculate risk scores for entities (importers/traders).
    
    Privacy: All calculations are done on aggregated data.
    Individual declarations are not exposed.
    """
    
    # Risk score thresholds
    LOW_THRESHOLD = Decimal('0.20')
    MEDIUM_THRESHOLD = Decimal('0.40')
    HIGH_THRESHOLD = Decimal('0.70')
    CRITICAL_THRESHOLD = Decimal('0.90')
    
    @staticmethod
    def calculate_risk_score(entity_declarations: List[Dict[str, Any]]) -> RiskScore:
        """
        Calculate overall risk score for an entity.
        
        Args:
            entity_declarations: List of aggregated declaration stats for entity
        
        Returns:
            RiskScore object with aggregated risk metrics
        """
        if not entity_declarations:
            return RiskScore(
                entity_id='UNKNOWN',
                risk_level='LOW',
                risk_score=Decimal('0'),
                risk_factors={},
                recommendation='No data available'
            )
        
        # Get entity ID from first record
        entity_id = entity_declarations[0].get('entity_id', 'UNKNOWN')
        
        # Calculate individual risk factors
        factors = RiskScorer._calculate_risk_factors(entity_declarations)
        
        # Calculate weighted total score
        total_score = Decimal('0')
        for factor_name, factor_data in factors.items():
            weight = RISK_FACTORS.get(factor_name, {}).get('weight', 0)
            total_score += Decimal(str(factor_data['score'])) * Decimal(str(weight))
        
        # Determine risk level
        risk_level = RiskScorer._determine_risk_level(total_score)
        
        # Generate recommendation
        recommendation = RiskScorer._generate_recommendation(risk_level, factors)
        
        return RiskScore(
            entity_id=entity_id,
            risk_level=risk_level,
            risk_score=total_score.quantize(Decimal('0.01')),
            risk_factors=factors,
            recommendation=recommendation
        )
    
    @staticmethod
    def _calculate_risk_factors(declarations: List[Dict[str, Any]]) -> Dict[str, Dict]:
        """Calculate individual risk factors"""
        factors = {}
        
        # 1. High Value Risk
        total_value = sum(d.get('total_value', 0) for d in declarations)
        max_value = max(d.get('total_value', 0) for d in declarations)
        
        if max_value > RISK_FACTORS['high_value']['threshold']:
            factors['high_value'] = {
                'score': 1.0,
                'value': max_value,
                'threshold': RISK_FACTORS['high_value']['threshold']
            }
        else:
            factors['high_value'] = {
                'score': max_value / RISK_FACTORS['high_value']['threshold'],
                'value': max_value,
                'threshold': RISK_FACTORS['high_value']['threshold']
            }
        
        # 2. High Frequency Risk
        decl_count = len(declarations)
        factors['high_frequency'] = {
            'score': min(1.0, decl_count / RISK_FACTORS['high_frequency']['threshold']),
            'count': decl_count,
            'threshold': RISK_FACTORS['high_frequency']['threshold']
        }
        
        # 3. Duty Variance Risk
        if len(declarations) > 1:
            avg_duty = sum(d.get('avg_duty_rate', 0) for d in declarations) / len(declarations)
            duty_rates = [d.get('avg_duty_rate', 0) for d in declarations]
            
            if avg_duty > 0:
                variance = sum((r - avg_duty) ** 2 for r in duty_rates) / len(duty_rates)
                std_dev = variance ** 0.5
                cv = std_dev / avg_duty if avg_duty > 0 else 0
                
                factors['duty_variance'] = {
                    'score': min(1.0, cv / RISK_FACTORS['duty_variance']['threshold']),
                    'coefficient_of_variation': cv,
                    'threshold': RISK_FACTORS['duty_variance']['threshold']
                }
            else:
                factors['duty_variance'] = {'score': 0, 'cv': 0}
        else:
            factors['duty_variance'] = {'score': 0, 'cv': 0}
        
        # 4. Rejected Count Risk
        rejected = sum(1 for d in declarations if d.get('status') == 'REJECTED')
        factors['rejected_count'] = {
            'score': min(1.0, rejected / RISK_FACTORS['rejected_count']['threshold']),
            'count': rejected,
            'threshold': RISK_FACTORS['rejected_count']['threshold']
        }
        
        # 5. Late Payment Risk (placeholder - would need payment data)
        factors['late_payment'] = {'score': 0, 'avg_days_late': 0}
        
        # 6. Preferential Abuse Risk
        preferential_count = sum(1 for d in declarations if d.get('preferential_used', False))
        pref_ratio = preferential_count / len(declarations) if declarations else 0
        
        factors['preferential_abuse'] = {
            'score': min(1.0, pref_ratio / RISK_FACTORS['preferential_abuse']['threshold']),
            'ratio': pref_ratio,
            'threshold': RISK_FACTORS['preferential_abuse']['threshold']
        }
        
        return factors
    
    @staticmethod
    def _determine_risk_level(score: Decimal) -> str:
        """Determine risk level from score"""
        if score >= RiskScorer.CRITICAL_THRESHOLD:
            return 'CRITICAL'
        elif score >= RiskScorer.HIGH_THRESHOLD:
            return 'HIGH'
        elif score >= RiskScorer.MEDIUM_THRESHOLD:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @staticmethod
    def _generate_recommendation(risk_level: str, factors: Dict) -> str:
        """Generate recommendation based on risk level and factors"""
        if risk_level == 'CRITICAL':
            return 'Immediate review required - high value and/or frequent discrepancies detected'
        elif risk_level == 'HIGH':
            return 'Priority review recommended - elevated risk indicators identified'
        elif risk_level == 'MEDIUM':
            return 'Standard monitoring - periodic review advised'
        else:
            return 'Routine monitoring - no significant risk indicators'


def calculate_entity_risk(aggregated_data: List[Dict[str, Any]]) -> RiskScore:
    """
    Public interface for risk scoring.
    
    Args:
        aggregated_data: Aggregated entity data
    
    Returns:
        RiskScore object
    """
    return RiskScorer.calculate_risk_score(aggregated_data)


def batch_risk_scores(entity_data_list: List[List[Dict[str, Any]]]) -> List[RiskScore]:
    """
    Calculate risk scores for multiple entities.
    
    Args:
        entity_data_list: List of aggregated data for each entity
    
    Returns:
        List of RiskScore objects
    """
    return [RiskScorer.calculate_risk_score(data) for data in entity_data_list]


# ============================================================================
# Tests
# ============================================================================

if __name__ == '__main__':
    print("=== Risk Scoring Tests ===\n")
    
    # Test data - aggregated entity data
    test_entity = [
        {'entity_id': 'IMP-12345-0000001', 'total_value': 75000, 'avg_duty_rate': 0.15,
         'status': 'CLEARED', 'preferential_used': True},
        {'entity_id': 'IMP-12345-0000001', 'total_value': 60000, 'avg_duty_rate': 0.12,
         'status': 'CLEARED', 'preferential_used': True},
        {'entity_id': 'IMP-12345-0000001', 'total_value': 80000, 'avg_duty_rate': 0.18,
         'status': 'CLEARED', 'preferential_used': False},
    ]
    
    # Test 1: Calculate risk score
    print("Test 1: Risk Score Calculation")
    result = calculate_entity_risk(test_entity)
    print(f"  Entity: {result.entity_id}")
    print(f"  Risk Level: {result.risk_level}")
    print(f"  Risk Score: {result.risk_score}")
    print(f"  Recommendation: {result.recommendation}")
    print("  ✓ Risk scoring completed\n")
    
    # Test 2: Verify score is in valid range
    print("Test 2: Score Range Validation")
    assert 0 <= float(result.risk_score) <= 1
    print("  ✓ Score is in valid range (0-1)\n")
    
    # Test 3: Risk level determination
    print("Test 3: Risk Level Classification")
    assert result.risk_level in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    print(f"  ✓ Valid risk level: {result.risk_level}\n")
    
    print("=== All Risk Scoring Tests Passed ===")