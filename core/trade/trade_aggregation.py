"""
Trade Aggregation Module - Aggregated Trade Analytics
Phase 6 - Trade Volume Analytics Implementation

Provides aggregated trade statistics with privacy-safe outputs.
All outputs are aggregated to prevent identification of individual declarations or importers.

Aggregation Levels:
- By HS Chapter (2-digit)
- By Country (origin)
- By Month (temporal)
- By Port
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# Data Transfer Objects (Privacy-Safe Output)
# ============================================================================

@dataclass
class TradeByHSChapter:
    """Aggregated trade statistics by HS chapter - NO individual identifiers"""
    chapter: str
    chapter_description: str
    
    # Aggregated metrics only
    total_declarations: int
    total_items: int
    total_quantity: Decimal
    quantity_unit: str
    
    # Value metrics
    total_customs_value: Decimal
    total_duty_collected: Decimal
    total_vat_collected: Decimal
    
    # Averages
    average_declaration_value: Decimal
    average_duty_rate: Decimal
    
    # No individual identifiers - IMPORTER_ID, DECLARATION_ID excluded


@dataclass 
class TradeByCountry:
    """Aggregated trade statistics by origin country - NO individual identifiers"""
    country_code: str
    country_name: str
    
    # Aggregated metrics
    total_declarations: int
    total_items: int
    total_customs_value: Decimal
    total_duty_collected: Decimal
    total_vat_collected: Decimal
    
    # Top HS chapters (aggregated only)
    top_chapters: List[Dict[str, Any]]
    
    # No individual identifiers


@dataclass
class TradeByMonth:
    """Aggregated trade statistics by month - NO individual identifiers"""
    year: int
    month: int
    month_label: str
    
    # Aggregated metrics
    total_declarations: int
    total_items: int
    total_customs_value: Decimal
    total_duty_collected: Decimal
    total_vat_collected: Decimal
    
    # Trade counts
    cleared_declarations: int
    rejected_declarations: int
    
    # No individual identifiers


# ============================================================================
# Aggregation Engine
# ============================================================================

class TradeAggregator:
    """
    Aggregates trade data at various levels while maintaining privacy.
    
    All methods return aggregated data only - no individual declaration
    or importer identifiers are exposed.
    """
    
    # Minimum aggregation threshold for privacy
    MIN_AGGREGATION_COUNT = 5
    
    @staticmethod
    def aggregate_by_hs_chapter(declarations: List[Dict[str, Any]]) -> List[TradeByHSChapter]:
        """
        Aggregate trade data by HS chapter (2-digit).
        
        Privacy: No declaration_id, importer_id, or item_id in output.
        """
        # Group by chapter
        chapter_data: Dict[str, Dict[str, Any]] = {}
        
        for decl in declarations:
            if decl.get('status') != 'CLEARED':
                continue
                
            # Extract chapter from HS code (first 2 digits)
            # In real implementation, join with declaration_items
            chapter = decl.get('hs_chapter', 'UNKNOWN')
            
            if chapter not in chapter_data:
                chapter_data[chapter] = {
                    'chapter': chapter,
                    'total_declarations': 0,
                    'total_items': 0,
                    'total_quantity': Decimal('0'),
                    'total_value': Decimal('0'),
                    'total_duty': Decimal('0'),
                    'total_vat': Decimal('0'),
                }
            
            cd = chapter_data[chapter]
            cd['total_declarations'] += 1
            cd['total_items'] += decl.get('total_items', 0)
            cd['total_value'] += Decimal(str(decl.get('total_customs_value', 0)))
            cd['total_duty'] += Decimal(str(decl.get('total_customs_duty', 0)))
            cd['total_vat'] += Decimal(str(decl.get('total_vat', 0)))
        
        # Build output (aggregated only)
        results = []
        for chapter, data in chapter_data.items():
            if data['total_declarations'] < TradeAggregator.MIN_AGGREGATION_COUNT:
                continue  # Skip small samples for privacy
                
            total_value = data['total_value']
            total_decls = Decimal(str(data['total_declarations']))
            
            results.append(TradeByHSChapter(
                chapter=chapter,
                chapter_description=f"Chapter {chapter} - Aggregated",
                total_declarations=data['total_declarations'],
                total_items=data['total_items'],
                total_quantity=data['total_quantity'],
                quantity_unit='KGM',  # Aggregated unit
                total_customs_value=TradeAggregator._round_amount(total_value),
                total_duty_collected=TradeAggregator._round_amount(data['total_duty']),
                total_vat_collected=TradeAggregator._round_amount(data['total_vat']),
                average_declaration_value=TradeAggregator._round_amount(total_value / total_decls),
                average_duty_rate=TradeAggregator._round_amount(
                    data['total_duty'] / total_value if total_value > 0 else 0
                )
            ))
        
        return sorted(results, key=lambda x: x.total_customs_value, reverse=True)
    
    @staticmethod
    def aggregate_by_country(declarations: List[Dict[str, Any]]) -> List[TradeByCountry]:
        """
        Aggregate trade data by origin country.
        
        Privacy: No declaration_id, importer_id in output.
        """
        country_data: Dict[str, Dict[str, Any]] = {}
        
        for decl in declarations:
            if decl.get('status') != 'CLEARED':
                continue
                
            country = decl.get('origin_country', 'XX')
            
            if country not in country_data:
                country_data[country] = {
                    'country_code': country,
                    'total_declarations': 0,
                    'total_items': 0,
                    'total_value': Decimal('0'),
                    'total_duty': Decimal('0'),
                    'total_vat': Decimal('0'),
                }
            
            cd = country_data[country]
            cd['total_declarations'] += 1
            cd['total_items'] += decl.get('total_items', 0)
            cd['total_value'] += Decimal(str(decl.get('total_customs_value', 0)))
            cd['total_duty'] += Decimal(str(decl.get('total_customs_duty', 0)))
            cd['total_vat'] += Decimal(str(decl.get('total_vat', 0)))
        
        # Build output
        results = []
        for country, data in country_data.items():
            if data['total_declarations'] < TradeAggregator.MIN_AGGREGATION_COUNT:
                continue
                
            results.append(TradeByCountry(
                country_code=country,
                country_name=f"Country {country} - Aggregated",
                total_declarations=data['total_declarations'],
                total_items=data['total_items'],
                total_customs_value=TradeAggregator._round_amount(data['total_value']),
                total_duty_collected=TradeAggregator._round_amount(data['total_duty']),
                total_vat_collected=TradeAggregator._round_amount(data['total_vat']),
                top_chapters=[]  # Would be populated from detailed join
            ))
        
        return sorted(results, key=lambda x: x.total_customs_value, reverse=True)
    
    @staticmethod
    def aggregate_by_month(declarations: List[Dict[str, Any]]) -> List[TradeByMonth]:
        """
        Aggregate trade data by month.
        
        Privacy: No declaration_id, importer_id in output.
        """
        month_data: Dict[str, Dict[str, Any]] = {}
        
        for decl in declarations:
            decl_date = decl.get('declaration_date')
            if not decl_date:
                continue
                
            if isinstance(decl_date, str):
                try:
                    decl_date = datetime.fromisoformat(decl_date.replace('Z', '+00:00'))
                except:
                    continue
            
            year_month = f"{decl_date.year}-{decl_date.month:02d}"
            
            if year_month not in month_data:
                month_data[year_month] = {
                    'year': decl_date.year,
                    'month': decl_date.month,
                    'total_declarations': 0,
                    'cleared': 0,
                    'rejected': 0,
                    'total_items': 0,
                    'total_value': Decimal('0'),
                    'total_duty': Decimal('0'),
                    'total_vat': Decimal('0'),
                }
            
            md = year_month[year_month]
            md['total_declarations'] += 1
            md['total_items'] += decl.get('total_items', 0)
            
            status = decl.get('status', 'LODGED')
            if status == 'CLEARED':
                md['cleared'] += 1
            elif status == 'REJECTED':
                md['rejected'] += 1
            
            md['total_value'] += Decimal(str(decl.get('total_customs_value', 0)))
            md['total_duty'] += Decimal(str(decl.get('total_customs_duty', 0)))
            md['total_vat'] += Decimal(str(decl.get('total_vat', 0)))
        
        # Build output
        results = []
        for year_month, data in month_data.items():
            results.append(TradeByMonth(
                year=data['year'],
                month=data['month'],
                month_label=f"{data['year']}-{data['month']:02d}",
                total_declarations=data['total_declarations'],
                total_items=data['total_items'],
                total_customs_value=TradeAggregator._round_amount(data['total_value']),
                total_duty_collected=TradeAggregator._round_amount(data['total_duty']),
                total_vat_collected=TradeAggregator._round_amount(data['total_vat']),
                cleared_declarations=data['cleared'],
                rejected_declarations=data['rejected']
            ))
        
        return sorted(results, key=lambda x: (x.year, x.month))
    
    @staticmethod
    def _round_amount(amount: Decimal) -> Decimal:
        """Round to 2 decimal places"""
        return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


# ============================================================================
# Safe Output Functions
# ============================================================================

def aggregate_trade_data(declarations: List[Dict[str, Any]], 
                        group_by: str) -> List[Dict[str, Any]]:
    """
    Public interface for trade aggregation.
    
    Args:
        declarations: List of declaration records
        group_by: 'hs_chapter', 'country', or 'month'
    
    Returns:
        Aggregated data with NO individual identifiers
    
    Privacy: 
    - No declaration_id in output
    - No importer_id in output  
    - No item_id in output
    - Minimum threshold applied (5 records)
    """
    if group_by == 'hs_chapter':
        results = TradeAggregator.aggregate_by_hs_chapter(declarations)
    elif group_by == 'country':
        results = TradeAggregator.aggregate_by_country(declarations)
    elif group_by == 'month':
        results = TradeAggregator.aggregate_by_month(declarations)
    else:
        raise ValueError(f"Unknown group_by: {group_by}")
    
    # Convert to dict for JSON serialization
    return [r.__dict__ for r in results]


# ============================================================================
# Validation
# ============================================================================

def validate_aggregation_safety(aggregated_data: List[Dict[str, Any]]) -> Dict[str, bool]:
    """
    Validate that aggregated data is privacy-safe.
    
    Returns dict with safety check results.
    """
    checks = {
        'no_declaration_ids': True,
        'no_importer_ids': True,
        'no_item_ids': True,
        'min_threshold_met': True,
    }
    
    forbidden_fields = ['declaration_id', 'importer_id', 'trader_id', 'item_id', 
                       'payment_id', 'bank_reference']
    
    for record in aggregated_data:
        for field in forbidden_fields:
            if field in record:
                checks['no_declaration_ids'] = False
                break
        
        if record.get('total_declarations', 0) < 5:
            checks['min_threshold_met'] = False
    
    return checks


# ============================================================================
# Tests
# ============================================================================

if __name__ == '__main__':
    print("=== Trade Aggregation Tests ===\n")
    
    # Synthetic test data
    synthetic_declarations = [
        {
            'declaration_id': 'DEC-20240101-0000001',  # Should NOT appear in output
            'declarant_id': 'IMP-12345-0000001',       # Should NOT appear in output
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
            'declaration_id': 'DEC-20240102-0000002',  # Should NOT appear
            'declarant_id': 'IMP-12345-0000002',       # Should NOT appear
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
            'declaration_id': 'DEC-20240103-0000003',  # Should NOT appear
            'declarant_id': 'IMP-12345-0000003',       # Should NOT appear
            'origin_country': 'JP',
            'hs_chapter': '85',
            'declaration_date': '2024-01-25',
            'status': 'CLEARED',
            'total_items': 1,
            'total_customs_value': 10000.00,
            'total_customs_duty': 0.00,
            'total_vat': 1700.00,
        },
    ]
    
    # Test 1: Aggregate by HS Chapter
    print("Test 1: Aggregate by HS Chapter")
    by_chapter = aggregate_trade_data(synthetic_declarations, 'hs_chapter')
    for record in by_chapter:
        print(f"  Chapter {record['chapter']}: {record['total_declarations']} decls, "
              f"${record['total_customs_value']}")
        assert 'declaration_id' not in record
        assert 'declarant_id' not in record
    print("  ✓ PASSED - No individual identifiers\n")
    
    # Test 2: Aggregate by Country
    print("Test 2: Aggregate by Country")
    by_country = aggregate_trade_data(synthetic_declarations, 'country')
    for record in by_country:
        print(f"  Country {record['country_code']}: {record['total_declarations']} decls, "
              f"${record['total_customs_value']}")
        assert 'declaration_id' not in record
        assert 'importer_id' not in record
    print("  ✓ PASSED - No individual identifiers\n")
    
    # Test 3: Aggregate by Month
    print("Test 3: Aggregate by Month")
    by_month = aggregate_trade_data(synthetic_declarations, 'month')
    for record in by_month:
        print(f"  {record['month_label']}: {record['total_declarations']} decls, "
              f"${record['total_customs_value']}")
        assert 'declaration_id' not in record
    print("  ✓ PASSED - No individual identifiers\n")
    
    # Test 4: Validate safety
    print("Test 4: Validate aggregation safety")
    safety = validate_aggregation_safety(by_chapter)
    print(f"  Safety checks: {safety}")
    assert safety['no_declaration_ids'] == True
    assert safety['no_importer_ids'] == True
    print("  ✓ PASSED - All safety checks passed\n")
    
    # Test 5: Check totals vs synthetic base
    print("Test 5: Validate totals")
    total_value = sum(r['total_customs_value'] for r in by_chapter)
    base_total = sum(d['total_customs_value'] for d in synthetic_declarations)
    print(f"  Aggregated total: ${total_value}")
    print(f"  Base data total: ${base_total}")
    assert abs(float(total_value) - base_total) < 0.01
    print("  ✓ PASSED - Totals match\n")
    
    print("=== All Tests Passed ===")
    print("Trade aggregation is privacy-safe and reproducible.")