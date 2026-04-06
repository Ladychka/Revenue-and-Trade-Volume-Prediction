# Analytics Samples
## Customs Revenue Analytics Platform - Showcase Artifact

**Document Version:** 1.0-FINAL  
**Status:** CLOSED - Portfolio Ready  
**Date:** 2026-04-01

---

## 1. Dashboard Screenshots Description

### 1.1 Revenue Overview Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         REVENUE OVERVIEW DASHBOARD                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────┐  ┌────────────────────────────────┐    │
│  │    TOTAL REVENUE               │  │    REVENUE GROWTH              │    │
│  │    $48,234,567                 │  │    +12.5% YoY                  │    │
│  │    (Duty + VAT + Excise)       │  │    +3.2% MoM                  │    │
│  └────────────────────────────────┘  └────────────────────────────────┘    │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    MONTHLY REVENUE TREND                             │  │
│  │                                                                      │  │
│  │   $5M |    ████                                                    │  │
│  │   $4M |  ██    ██                                                  │  │
│  │   $3M |██        ██   ████                                         │  │
│  │   $2M |            ██     ████                                     │  │
│  │   $1M |              ██       ████                                 │  │
│  │       └───────────────┴─────────────                                │  │
│  │            Jan  Feb  Mar  Apr  May  Jun                            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────┐  ┌────────────────────────┐    │
│  │     REVENUE BY TAX TYPE              │  │     TOP PORTS          │    │
│  │     ████████ Duty $19.2M (40%)       │  │  1. Port A - $12.5M   │    │
│  │     ████████████ VAT $21.7M (45%)    │  │  2. Port B - $9.8M    │    │
│  │     ██████ Excise $7.3M (15%)        │  │  3. Port C - $7.2M    │    │
│  └──────────────────────────────────────┘  └────────────────────────┘    │
│                                                                              │
│  ════════════════════════════════════════════════════════════════════════  │
│  ⚠️  SYNTHETIC DATA ONLY - NOT FOR OPERATIONAL USE                         ║  │
│  ════════════════════════════════════════════════════════════════════════  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Trade Summary Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRADE SUMMARY DASHBOARD                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────┐  ┌────────────────────────────────┐    │
│  │    TOTAL TRADE VALUE           │  │    DECLARATIONS                │    │
│  │    $523,456,789                │  │    24,567                      │    │
│  │    (Customs Value)             │  │    (Cleared)                   │    │
│  └────────────────────────────────┘  └────────────────────────────────┘    │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    TRADE BY COUNTRY                                 │  │
│  │                                                                      │  │
│  │    China        ████████████████████  35%   $183M                    │  │
│  │    Thailand     ██████████████      22%   $115M                    │  │
│  │    Vietnam      ██████████          15%   $78M                    │  │
│  │    Japan        ████████             10%   $52M                     │  │
│  │    USA          ██████               8%   $42M                     │  │
│  │    Other        ████                 10%   $53M                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    TRADE BY HS CHAPTER                              │  │
│  │                                                                      │  │
│  │    Ch.84 (Machinery)     ████████████    $89M  17%                   │  │
│  │    Ch.85 (Electronics)   ██████████      $78M  15%                   │  │
│  │    Ch.87 (Vehicles)      ████████        $65M  12%                   │  │
│  │    Ch.62 (Textiles)      ██████          $52M  10%                   │  │
│  │    Ch.39 (Plastics)      ██████          $47M   9%                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ════════════════════════════════════════════════════════════════════════  │
│  ⚠️  SYNTHETIC DATA ONLY - NOT FOR OPERATIONAL USE                         ║  │
│  ════════════════════════════════════════════════════════════════════════  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Risk Monitoring Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RISK MONITORING DASHBOARD                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────┐  ┌────────────────────────────────┐    │
│  │    HIGH RISK COUNT             │  │    VARIANCE ALERTS             │    │
│  │    127                         │  │    43                          │    │
│  │    Entities flagged            │  │    >10% deviation             │    │
│  └────────────────────────────────┘  └────────────────────────────────┘    │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    REVENUE VARIANCE ANALYSIS                        │  │
│  │                                                                      │  │
│  │    Expected vs Actual Duty Collection                                │  │
│  │                                                                      │  │
│  │    Expected: $17,234,567                                            │  │
│  │    Actual:   $19,123,456                                            │  │
│  │    Variance: +$1,888,889 (+10.9%)                                   │  │
│  │                                                                      │  │
│  │    Expected VAT: $28,456,789                                        │  │
│  │    Actual VAT:   $26,987,654                                        │  │
│  │    Variance:    -$1,469,135 (-5.2%)  ⚠️                             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────┐  ┌────────────────────────┐    │
│  │     HIGH RISK HS CODES              │  │    RISK TRENDS         │    │
│  │     ██████████ Electronics          │  │    ↑ Increasing        │    │
│  │     ████████   Vehicles             │  │    → Stable            │    │
│  │     ██████     Machinery            │  │    ↓ Decreasing       │    │
│  └──────────────────────────────────────┘  └────────────────────────┘    │
│                                                                              │
│  ════════════════════════════════════════════════════════════════════════  │
│  ⚠️  SYNTHETIC DATA ONLY - NOT FOR OPERATIONAL USE                         ║  │
│  ════════════════════════════════════════════════════════════════════════  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Aggregated Tables (Sample API Responses)

### 2.1 Monthly Revenue Summary

```json
GET /api/v1/revenue/monthly

[
  {
    "year": 2024,
    "month": 12,
    "cleared_declarations": 2156,
    "total_customs_value": 45678900.00,
    "total_customs_duty": 2740734.00,
    "total_vat": 7777421.00,
    "total_tax_liability": 10518155.00
  },
  {
    "year": 2024,
    "month": 11,
    "cleared_declarations": 2083,
    "total_customs_value": 42345678.00,
    "total_customs_duty": 2540740.68,
    "total_vat": 7198765.26,
    "total_tax_liability": 9739505.94
  },
  {
    "year": 2024,
    "month": 10,
    "cleared_declarations": 2345,
    "total_customs_value": 48901234.00,
    "total_customs_duty": 2934074.04,
    "total_vat": 8313210.78,
    "total_tax_liability": 11247284.82
  }
]
```

### 2.2 Trade by Country

```json
GET /api/v1/trade/by-country?limit=10

[
  {
    "country_code": "CN",
    "country_name": "China",
    "total_declarations": 5621,
    "total_items": 28456,
    "total_customs_value": 183234567.89,
    "total_customs_duty": 10994074.07,
    "total_vat": 31149876.54,
    "avg_shipment_value": 32597.45
  },
  {
    "country_code": "TH",
    "country_name": "Thailand",
    "total_declarations": 3845,
    "total_items": 15234,
    "total_customs_value": 115234567.12,
    "total_customs_duty": 6914074.03,
    "total_vat": 19589876.41,
    "avg_shipment_value": 29985.23
  },
  {
    "country_code": "VN",
    "country_name": "Vietnam",
    "total_declarations": 2934,
    "total_items": 11234,
    "total_customs_value": 78456789.45,
    "total_customs_duty": 4707407.37,
    "total_vat": 13337654.21,
    "avg_shipment_value": 26745.67
  }
]
```

### 2.3 Trade by HS Code

```json
GET /api/v1/trade/by-hs?limit=10

[
  {
    "hs_chapter": "84",
    "chapter_description": "Nuclear Reactors, Machinery",
    "total_declarations": 3456,
    "total_customs_value": 89012345.67,
    "total_customs_duty": 5340740.74,
    "total_vat": 15132101.56,
    "avg_duty_rate": 0.06
  },
  {
    "hs_chapter": "85",
    "chapter_description": "Electrical Machinery",
    "total_declarations": 2987,
    "total_customs_value": 78234567.89,
    "total_customs_duty": 4694074.07,
    "total_vat": 13299876.54,
    "avg_duty_rate": 0.06
  },
  {
    "hs_chapter": "87",
    "chapter_description": "Vehicles",
    "total_declarations": 1876,
    "total_customs_value": 65123456.78,
    "total_customs_duty": 3907407.41,
    "total_vat": 11070987.65,
    "avg_duty_rate": 0.06
  }
]
```

### 2.4 Revenue by Port

```json
GET /api/v1/revenue/by-port

[
  {
    "port_code": "PNH",
    "port_name": "Phnom Penh",
    "total_declarations": 8923,
    "total_customs_value": 198765432.10,
    "total_customs_duty": 11925925.93,
    "total_vat": 33790073.46,
    "total_tax_liability": 45715999.39,
    "avg_processing_days": 2.3
  },
  {
    "port_code": "SIH",
    "port_name": "Sihanoukville",
    "total_declarations": 5634,
    "total_customs_value": 156789012.34,
    "total_customs_duty": 9407340.74,
    "total_vat": 26654132.10,
    "total_tax_liability": 36061472.84,
    "avg_processing_days": 1.8
  },
  {
    "port_code": "BVB",
    "port_name": "Bavet",
    "total_declarations": 4123,
    "total_customs_value": 98765432.10,
    "total_customs_duty": 5925925.93,
    "total_vat": 16790123.46,
    "total_tax_liability": 22716049.39,
    "avg_processing_days": 1.5
  }
]
```

### 2.5 Compliance - Variance Summary

```json
GET /api/v1/compliance/variance

{
  "total_analyzed": 24567,
  "total_variance": 2345678.90,
  "variance_percentage": 4.86,
  "high_variance_count": 127,
  "by_tax_type": [
    {
      "tax_type": "customs_duty",
      "expected": 17234567.89,
      "actual": 19123456.78,
      "variance": 1888888.89,
      "variance_percentage": 10.96
    },
    {
      "tax_type": "vat",
      "expected": 28456789.12,
      "actual": 26987654.32,
      "variance": -1469134.80,
      "variance_percentage": -5.16
    }
  ],
  "by_month": [
    {
      "year": 2024,
      "month": 12,
      "duty_variance": 234567.89,
      "vat_variance": -123456.78
    }
  ]
}
```

---

## 3. Synthetic Watermark Statement

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SYNTHETIC DATA WATERMARK                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ████  ████  ████  ████  ████  ████  ████  ████  ████  ████              │
│   ████  ████  ████  ████  ████  ████  ████  ████  ████  ████              │
│                                                                              │
│   ⚠️  THIS DATA IS 100% SYNTHETIC                                           │
│                                                                              │
│   All figures in this system are artificially generated for demonstration  │
│   purposes only. No real customs declarations, payments, or trade         │
│   transactions are represented.                                            │
│                                                                              │
│   • All identifiers are synthetic (DEC-*, IMP-*, PMT-*)                    │
│   • All values are randomly generated within realistic ranges              │
│   • All country/port/HS data is reference-only                             │
│   • No real entities are identified                                         │
│                                                                              │
│   NOT FOR: Production use, Operational decisions, Official reporting      │
│                                                                              │
│   ████  ████  ████  ████  ████  ████  ████  ████  ████  ████              │
│   ████  ████  ████  ████  ████  ████  ████  ████  ████  ████              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Aggregation Rules Applied

| Rule | Implementation | Example |
|------|----------------|---------|
| **Minimum Threshold** | 5 records minimum | No single-entity data shown |
| **Top-N Limitation** | 10-20 records max | Countries: 20, HS codes: 20 |
| **No Drill-Down** | Disabled in Power BI | Cannot click-through to details |
| **No Export** | Disabled in Power BI | Cannot export to Excel/PDF |
| **Synthetic IDs** | Format: DEC-*, IMP-*, PMT-* | Cannot trace to real entities |
| **Aggregated Values** | SUM, AVG, COUNT only | No individual transactions |

---

## 5. Status

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    ANALYTICS SAMPLES STATUS                              ║
║                                                                           ║
║  ✅ Dashboard screenshots documented                                    ║
║  ✅ Aggregated tables shown (JSON responses)                           ║
║  ✅ Synthetic watermark demonstrated                                   ║
║  ✅ Aggregation rules documented                                        ║
║                                                                           ║
║  Status: COMPLETE - VERSION FINAL 1.0                                   ║
║  Freeze: EFFECTIVE 2026-04-01                                            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

**Document Status:** APPROVED - Analytics Samples Artifact  
**Project Status:** CLOSED - VERSION FINAL  
**Last Updated:** 2026-04-01