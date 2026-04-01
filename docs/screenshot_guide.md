# Phase 18 - Screenshot & Media Guide

## Purpose
This guide ensures all screenshots and media captures from the project maintain privacy 
and present the system appropriately for public sharing.

---

## Screenshot Guidelines

### ✅ ALLOWED Screenshots

| What to Capture | Description |
|-----------------|-------------|
| Dashboard overview | Full aggregated view with KPI cards |
| Monthly revenue chart | Line/bar chart showing trends |
| Trade by country | Treemap or bar chart (top 10+) |
| Trade by HS code | Stacked bar (chapter level) |
| API documentation | Swagger UI showing endpoints |
| Code structure | File tree or editor view |
| Database schema | ERD or table structure |
| Executive summary | One-page brief content |

### ⚠️ CAUTION - Needs Review

| What to Capture | Notes |
|-----------------|-------|
| Sample data rows | Must show synthetic IDs only |
| API response JSON | Must be aggregated data |
| Dashboard filters | Ensure no individual data shown |

### ❌ PROHIBITED Screenshots

| What NOT to Capture | Reason |
|---------------------|--------|
| Individual declarations | Contains synthetic IDs |
| Single importer details | Not appropriate |
| Real company names | Doesn't exist anyway |
| Actual payment amounts | Could be misinterpreted |
| Drill-down views | Not enabled anyway |

---

## Dashboard Watermark Guide

All dashboard screenshots should include:

```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️ SYNTHETIC DATA ONLY - DEMO SYSTEM                       │
│  Data Source: Customs Analytics v1.0-demo                   │
│  Not for production use - All data synthetic                │
└─────────────────────────────────────────────────────────────┘
```

### Adding Watermark in Power BI

1. Insert → Text Box
2. Enter watermark text
3. Format → Properties → Lock aspect ratio
4. Position: Bottom of page
5. Transparency: 70%

---

## Screen Recording Guidelines

### Allowed Content
- Dashboard navigation and filtering
- API documentation browsing
- Code walkthroughs
- System architecture explanations

### Prohibited Content
- Any data tables with row-level details
- Individual record searches
- Export functionality attempts

---

## Media Assets Summary

### Required Labels on All Materials
- "SYNTHETIC DATA ONLY"
- "DEMO SYSTEM"
- "NOT FOR PRODUCTION USE"

### Recommended Visuals
| Asset | Description |
|-------|-------------|
| Architecture diagram | System layers |
| Dashboard mockups | KPI cards, charts |
| API flow | Endpoint structure |
| Database design | Schema relationships |
| Use case flow | Scenario walkthrough |

---

## Document Control

**Version**: 1.0.0  
**Date**: 2026-04-01  
**Status**: APPROVED - Media guide complete
