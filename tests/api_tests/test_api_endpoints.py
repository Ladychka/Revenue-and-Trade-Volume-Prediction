#!/usr/bin/env python3
"""
API Endpoint Tests
Phase 10 - Testing

Integration tests for all API endpoints using FastAPI TestClient.
Tests run in demo mode (no database required).
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from api.main import app

client = TestClient(app)


# ============================================================================
# Health Check
# ============================================================================

class TestHealthEndpoint:
    """Test the health check endpoint"""

    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_fields(self):
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "data_mode" in data


# ============================================================================
# Revenue Endpoints
# ============================================================================

class TestRevenueEndpoints:
    """Test revenue analytics endpoints"""

    def test_revenue_summary(self):
        response = client.get("/api/v1/revenue/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_declarations" in data
        assert "total_customs_value" in data
        assert "total_customs_duty" in data
        assert "total_vat" in data
        assert "total_tax_liability" in data
        assert data["total_declarations"] > 0

    def test_revenue_summary_with_year_filter(self):
        response = client.get("/api/v1/revenue/summary?year=2024")
        assert response.status_code == 200

    def test_revenue_monthly(self):
        response = client.get("/api/v1/revenue/monthly")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        first = data[0]
        assert "year" in first
        assert "month" in first
        assert "total_customs_value" in first

    def test_revenue_monthly_with_limit(self):
        response = client.get("/api/v1/revenue/monthly?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3

    def test_revenue_by_port(self):
        response = client.get("/api/v1/revenue/by-port")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        first = data[0]
        assert "port_code" in first
        assert "total_customs_value" in first

    def test_revenue_by_port_with_limit(self):
        response = client.get("/api/v1/revenue/by-port?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3

    def test_revenue_by_tax_type(self):
        response = client.get("/api/v1/revenue/by-tax-type")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3  # duty, vat, excise
        tax_types = [d["tax_type"] for d in data]
        assert "Customs Duty" in tax_types
        assert "Value-Added Tax" in tax_types

    def test_revenue_trends(self):
        response = client.get("/api/v1/revenue/trends")
        assert response.status_code == 200
        data = response.json()
        assert "period_type" in data
        assert "data_points" in data
        assert "summary" in data

    def test_revenue_trends_invalid_period(self):
        response = client.get("/api/v1/revenue/trends?period=yearly")
        assert response.status_code == 422  # Validation error


# ============================================================================
# Trade Endpoints
# ============================================================================

class TestTradeEndpoints:
    """Test trade analytics endpoints"""

    def test_trade_summary(self):
        response = client.get("/api/v1/trade/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_declarations" in data
        assert "total_items" in data
        assert "total_customs_value" in data

    def test_trade_by_country(self):
        response = client.get("/api/v1/trade/by-country")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        first = data[0]
        assert "country_code" in first
        assert "country_name" in first
        assert "total_customs_value" in first

    def test_trade_by_country_with_limit(self):
        response = client.get("/api/v1/trade/by-country?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2

    def test_trade_by_hs(self):
        response = client.get("/api/v1/trade/by-hs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        first = data[0]
        assert "hs_chapter" in first
        assert "chapter_description" in first

    def test_trade_time_series(self):
        response = client.get("/api/v1/trade/time-series")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_trade_top_importers(self):
        response = client.get("/api/v1/trade/top-importers")
        assert response.status_code == 200
        data = response.json()
        assert "rankings" in data
        assert "note" in data


# ============================================================================
# Compliance Endpoints
# ============================================================================

class TestComplianceEndpoints:
    """Test compliance analytics endpoints"""

    def test_risk_summary(self):
        response = client.get("/api/v1/compliance/risk-summary")
        assert response.status_code == 200
        data = response.json()
        assert "high_risk_count" in data
        assert "total_declarations" in data
        assert "flagged_percentage" in data
        assert data["total_declarations"] > 0

    def test_variance_summary(self):
        response = client.get("/api/v1/compliance/variance-summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_analyzed" in data
        assert "variance_detected" in data
        assert "variance_percentage" in data

    def test_variance_summary_with_threshold(self):
        response = client.get("/api/v1/compliance/variance-summary?threshold=0.20")
        assert response.status_code == 200

    def test_high_risk_entities(self):
        response = client.get("/api/v1/compliance/high-risk-entities")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "note" in data


# ============================================================================
# Metadata Endpoints
# ============================================================================

class TestMetadataEndpoints:
    """Test metadata/reference data endpoints"""

    def test_api_info(self):
        response = client.get("/api/v1/metadata/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Customs Revenue Analytics API"
        assert "safety_features" in data
        assert data["safety_features"]["read_only"] is True

    def test_endpoints_list(self):
        response = client.get("/api/v1/metadata/endpoints")
        assert response.status_code == 200
        data = response.json()
        assert "revenue" in data
        assert "trade" in data
        assert "compliance" in data

    def test_ports_reference(self):
        response = client.get("/api/v1/metadata/ports")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_countries_reference(self):
        response = client.get("/api/v1/metadata/countries")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_hs_codes_reference(self):
        response = client.get("/api/v1/metadata/hs-codes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        first = data[0]
        assert "hs_code" in first
        assert "description" in first


# ============================================================================
# Safety Verification Tests
# ============================================================================

class TestSafetyConstraints:
    """Verify safety-by-design constraints"""

    def test_no_write_endpoints(self):
        """Verify that POST/PUT/DELETE methods are rejected"""
        # POST should return 405 Method Not Allowed
        response = client.post("/api/v1/revenue/summary", json={})
        assert response.status_code == 405

    def test_no_individual_ids_in_revenue(self):
        """Revenue summary should not contain individual declaration IDs"""
        response = client.get("/api/v1/revenue/summary")
        data = response.json()
        text = str(data)
        assert "DEC-" not in text  # No declaration IDs
        assert "IMP-" not in text  # No importer IDs

    def test_no_individual_ids_in_trade(self):
        """Trade data should not contain individual identifiers"""
        response = client.get("/api/v1/trade/by-country")
        data = response.json()
        text = str(data)
        assert "DEC-" not in text
        assert "IMP-" not in text

    def test_no_individual_ids_in_top_importers(self):
        """Top importers should not expose importer IDs"""
        response = client.get("/api/v1/trade/top-importers")
        data = response.json()
        text = str(data)
        assert "IMP-" not in text

    def test_openapi_docs_available(self):
        """API documentation should be accessible"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_available(self):
        """ReDoc documentation should be accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
