#!/usr/bin/env python3
"""
API Roles Module - Role-Based Access Control
Phase 8 - API Implementation

Defines roles and permissions for API access.
"""

from enum import Enum
from typing import List, Dict, Set
from functools import wraps


# ============================================================================
# Role Definitions
# ============================================================================

class UserRole(str, Enum):
    """User roles for API access"""
    ADMIN = "admin"
    ANALYTICS = "analytics"
    VIEWER = "viewer"
    GUEST = "guest"


class Permission(str, Enum):
    """API permissions"""
    # Revenue permissions
    READ_REVENUE_SUMMARY = "revenue:read_summary"
    READ_REVENUE_MONTHLY = "revenue:read_monthly"
    READ_REVENUE_BY_PORT = "revenue:read_port"
    READ_REVENUE_BY_TAX_TYPE = "revenue:read_tax_type"
    WRITE_REVENUE = "revenue:write"
    
    # Trade permissions
    READ_TRADE_SUMMARY = "trade:read_summary"
    READ_TRADE_BY_COUNTRY = "trade:read_country"
    READ_TRADE_BY_HS = "trade:read_hs"
    READ_TRADE_TIME_SERIES = "trade:read_time_series"
    WRITE_TRADE = "trade:write"
    
    # Compliance permissions
    READ_COMPLIANCE_RISK = "compliance:read_risk"
    READ_COMPLIANCE_VARIANCE = "compliance:read_variance"
    WRITE_COMPLIANCE = "compliance:write"
    
    # Metadata permissions
    READ_METADATA = "metadata:read"
    WRITE_METADATA = "metadata:write"
    
    # Admin permissions
    ADMIN_ACCESS = "admin:access"
    READ_AUDIT_LOGS = "audit:read"
    MANAGE_API_KEYS = "api_keys:manage"


# ============================================================================
# Role-Permission Mapping
# ============================================================================

ROLE_PERMISSIONS: Dict[UserRole, Set[Permission]] = {
    UserRole.ADMIN: {
        Permission.READ_REVENUE_SUMMARY,
        Permission.READ_REVENUE_MONTHLY,
        Permission.READ_REVENUE_BY_PORT,
        Permission.READ_REVENUE_BY_TAX_TYPE,
        Permission.WRITE_REVENUE,
        Permission.READ_TRADE_SUMMARY,
        Permission.READ_TRADE_BY_COUNTRY,
        Permission.READ_TRADE_BY_HS,
        Permission.READ_TRADE_TIME_SERIES,
        Permission.WRITE_TRADE,
        Permission.READ_COMPLIANCE_RISK,
        Permission.READ_COMPLIANCE_VARIANCE,
        Permission.WRITE_COMPLIANCE,
        Permission.READ_METADATA,
        Permission.WRITE_METADATA,
        Permission.ADMIN_ACCESS,
        Permission.READ_AUDIT_LOGS,
        Permission.MANAGE_API_KEYS,
    },
    UserRole.ANALYTICS: {
        Permission.READ_REVENUE_SUMMARY,
        Permission.READ_REVENUE_MONTHLY,
        Permission.READ_REVENUE_BY_PORT,
        Permission.READ_REVENUE_BY_TAX_TYPE,
        Permission.READ_TRADE_SUMMARY,
        Permission.READ_TRADE_BY_COUNTRY,
        Permission.READ_TRADE_BY_HS,
        Permission.READ_TRADE_TIME_SERIES,
        Permission.READ_COMPLIANCE_RISK,
        Permission.READ_COMPLIANCE_VARIANCE,
        Permission.READ_METADATA,
    },
    UserRole.VIEWER: {
        Permission.READ_REVENUE_SUMMARY,
        Permission.READ_REVENUE_MONTHLY,
        Permission.READ_TRADE_SUMMARY,
        Permission.READ_TRADE_BY_COUNTRY,
        Permission.READ_METADATA,
    },
    UserRole.GUEST: {
        Permission.READ_REVENUE_SUMMARY,
        Permission.READ_TRADE_SUMMARY,
    },
}


# ============================================================================
# Permission Checker
# ============================================================================

def has_permission(role: UserRole, permission: Permission) -> bool:
    """Check if a role has a specific permission"""
    return permission in ROLE_PERMISSIONS.get(role, set())


def get_role_permissions(role: UserRole) -> Set[Permission]:
    """Get all permissions for a role"""
    return ROLE_PERMISSIONS.get(role, set())


def check_permission(role: UserRole, required_permission: Permission):
    """
    Decorator to check permission before executing endpoint.
    
    Usage:
        @check_permission(UserRole.ANALYTICS, Permission.READ_REVENUE_SUMMARY)
        async def my_endpoint():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not has_permission(role, required_permission):
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{required_permission.value}' required"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================================
# Role Validator
# ============================================================================

def validate_role(role_name: str) -> UserRole:
    """Validate role name and return UserRole enum"""
    try:
        return UserRole(role_name.lower())
    except ValueError:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role: {role_name}. Valid roles: {[r.value for r in UserRole]}"
        )


def get_role_from_api_key(api_key: str) -> UserRole:
    """
    Get role from API key.
    
    In production, look up role from database based on API key.
    For demo, return ANALYTICS role.
    """
    # Demo mode: return analytics role
    return UserRole.ANALYTICS


# ============================================================================
# Access Control Helper
# ============================================================================

class AccessControl:
    """Helper class for access control checks"""
    
    @staticmethod
    def can_access_endpoint(role: UserRole, endpoint_path: str) -> bool:
        """Check if role can access endpoint path"""
        # Map endpoint paths to required permissions
        endpoint_permissions = {
            '/revenue/summary': Permission.READ_REVENUE_SUMMARY,
            '/revenue/monthly': Permission.READ_REVENUE_MONTHLY,
            '/revenue/by-port': Permission.READ_REVENUE_BY_PORT,
            '/revenue/by-tax-type': Permission.READ_REVENUE_BY_TAX_TYPE,
            '/trade/summary': Permission.READ_TRADE_SUMMARY,
            '/trade/by-country': Permission.READ_TRADE_BY_COUNTRY,
            '/trade/by-hs': Permission.READ_TRADE_BY_HS,
            '/trade/time-series': Permission.READ_TRADE_TIME_SERIES,
            '/compliance/risk': Permission.READ_COMPLIANCE_RISK,
            '/compliance/variance': Permission.READ_COMPLIANCE_VARIANCE,
            '/metadata': Permission.READ_METADATA,
        }
        
        required_perm = endpoint_permissions.get(endpoint_path)
        if required_perm is None:
            return True  # Unknown endpoint, allow
        
        return has_permission(role, required_perm)
    
    @staticmethod
    def filter_response_data(role: UserRole, data: dict) -> dict:
        """
        Filter response data based on role.
        
        Remove sensitive fields for lower-privileged roles.
        """
        # Fields to hide from non-admin roles
        restricted_fields = ['api_key', 'internal_id', 'raw_data']
        
        if role == UserRole.ADMIN:
            return data
        
        return {k: v for k, v in data.items() if k not in restricted_fields}


# ============================================================================
# Tests
# ============================================================================

if __name__ == '__main__':
    print("=== Role-Based Access Control Tests ===\n")
    
    # Test 1: Role permissions
    print("Test 1: Role Permissions")
    admin_perms = get_role_permissions(UserRole.ADMIN)
    viewer_perms = get_role_permissions(UserRole.VIEWER)
    
    assert Permission.ADMIN_ACCESS in admin_perms
    assert Permission.ADMIN_ACCESS not in viewer_perms
    print(f"  Admin has {len(admin_perms)} permissions")
    print(f"  Viewer has {len(viewer_perms)} permissions")
    print("  ✓ Role permissions work\n")
    
    # Test 2: Permission check
    print("Test 2: Permission Check")
    assert has_permission(UserRole.VIEWER, Permission.READ_REVENUE_SUMMARY) == True
    assert has_permission(UserRole.VIEWER, Permission.WRITE_REVENUE) == False
    print("  ✓ Permission checks work\n")
    
    # Test 3: Access control
    print("Test 3: Endpoint Access Control")
    assert AccessControl.can_access_endpoint(UserRole.VIEWER, '/revenue/summary') == True
    assert AccessControl.can_access_endpoint(UserRole.VIEWER, '/revenue/by-port') == False
    print("  ✓ Endpoint access control works\n")
    
    # Test 4: Role validation
    print("Test 4: Role Validation")
    role = validate_role('admin')
    assert role == UserRole.ADMIN
    print("  ✓ Role validation works\n")
    
    print("=== All Role Tests Passed ===")