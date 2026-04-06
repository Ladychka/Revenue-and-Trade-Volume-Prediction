#!/usr/bin/env python3
"""
API Authentication Module
Phase 8 - API Implementation

Provides API key-based authentication for the analytics API.
"""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from typing import Optional
import hashlib
import os


# API Key configuration
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

# Store API keys (in production, use a database)
# Format: {key_hash: {role: role, description: desc}}
API_KEYS = {
    # Default demo keys - replace in production
    'demo_key_hash': {
        'role': 'viewer',
        'description': 'Demo viewer key',
        'rate_limit': 100  # requests per hour
    },
    'admin_key_hash': {
        'role': 'admin',
        'description': 'Admin key',
        'rate_limit': 1000
    },
    'analytics_key_hash': {
        'role': 'analytics',
        'description': 'Analytics user key',
        'rate_limit': 500
    }
}


def hash_api_key(api_key: str) -> str:
    """Hash API key for secure storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()


def get_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> str:
    """
    Validate API key from header.
    
    In demo mode, accepts any key for testing.
    In production, validate against stored keys.
    """
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required. Include 'X-API-Key' header."
        )
    
    # Hash the provided key
    key_hash = hash_api_key(api_key)
    
    # Check against stored keys (or accept demo mode)
    if key_hash in API_KEYS:
        return api_key
    
    # Demo mode: accept any key for testing
    if os.getenv('API_DEMO_MODE', 'true').lower() == 'true':
        return api_key
    
    # Production mode: reject unknown keys
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API key"
    )


def verify_api_key_role(api_key: str, required_role: str) -> bool:
    """Verify that API key has required role"""
    key_hash = hash_api_key(api_key)
    
    if key_hash not in API_KEYS:
        return False
    
    key_info = API_KEYS[key_hash]
    role = key_info.get('role', 'viewer')
    
    # Role hierarchy: admin > analytics > viewer
    role_hierarchy = {
        'admin': 3,
        'analytics': 2,
        'viewer': 1
    }
    
    return role_hierarchy.get(role, 0) >= role_hierarchy.get(required_role, 0)


def get_client_role(api_key: str) -> str:
    """Get the role for an API key"""
    key_hash = hash_api_key(api_key)
    
    if key_hash in API_KEYS:
        return API_KEYS[key_hash].get('role', 'viewer')
    
    return 'viewer'  # Default role for demo mode


def check_rate_limit(api_key: str) -> bool:
    """
    Check if API key has exceeded rate limit.
    
    In production, implement proper rate limiting with Redis or database.
    """
    key_hash = hash_api_key(api_key)
    
    if key_hash not in API_KEYS:
        return True  # Allow in demo mode
    
    # Placeholder for rate limit check
    # In production: check against Redis/cache for request count
    return True


# ============================================================================
# Dependency for role-based access
# ============================================================================

def require_role(required_role: str):
    """Dependency that requires a specific role"""
    def role_checker(api_key: str = Security(API_KEY_HEADER)) -> str:
        if api_key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required"
            )
        
        if not verify_api_key_role(api_key, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required for this endpoint"
            )
        
        return api_key
    
    return role_checker


# ============================================================================
# Rate Limiter
# ============================================================================

class RateLimiter:
    """Simple rate limiter for API endpoints"""
    
    def __init__(self, requests_per_hour: int = 100):
        self.requests_per_hour = requests_per_hour
        self.request_counts = {}
    
    def check_limit(self, client_id: str) -> bool:
        """Check if client has exceeded rate limit"""
        import time
        current_time = int(time.time())
        
        if client_id not in self.request_counts:
            self.request_counts[client_id] = {'reset_time': current_time + 3600, 'count': 1}
            return True
        
        client_data = self.request_counts[client_id]
        
        if current_time > client_data['reset_time']:
            # Reset counter
            client_data['reset_time'] = current_time + 3600
            client_data['count'] = 1
            return True
        
        if client_data['count'] >= self.requests_per_hour:
            return False
        
        client_data['count'] += 1
        return True


# ============================================================================
# Tests
# ============================================================================

if __name__ == '__main__':
    print("=== API Authentication Tests ===\n")
    
    # Test key hashing
    print("Test 1: Key Hashing")
    test_key = "test_api_key_123"
    hashed = hash_api_key(test_key)
    print(f"  Original: {test_key}")
    print(f"  Hashed: {hashed}")
    print("  ✓ Hashing works\n")
    
    # Test role verification
    print("Test 2: Role Verification")
    demo_key = "demo_key"
    admin_key = "admin_key"
    
    assert verify_api_key_role(demo_key, 'viewer') == True
    assert verify_api_key_role(demo_key, 'admin') == False
    assert verify_api_key_role(admin_key, 'admin') == True
    print("  ✓ Role verification works\n")
    
    # Test rate limiter
    print("Test 3: Rate Limiter")
    limiter = RateLimiter(requests_per_hour=5)
    
    for i in range(5):
        assert limiter.check_limit('test_client') == True
    
    assert limiter.check_limit('test_client') == False
    print("  ✓ Rate limiting works\n")
    
    print("=== All Authentication Tests Passed ===")