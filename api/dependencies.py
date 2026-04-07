"""
API Dependencies — Database Connection Pool & Shared Services
Phase 8 - API Implementation

Provides async database connectivity via asyncpg with graceful fallback
to demo data when no database is available.
"""

import os
import logging
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

# Database connection pool (initialized at startup)
_pool = None
_db_available = False


async def init_db_pool():
    """Initialize the async database connection pool."""
    global _pool, _db_available
    try:
        import asyncpg
        _pool = await asyncpg.create_pool(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "customs_analytics"),
            user=os.getenv("DB_USER", "customs_user"),
            password=os.getenv("DB_PASSWORD", "customs_demo_2026"),
            min_size=2,
            max_size=10,
            command_timeout=30,
        )
        # Test the connection
        async with _pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        _db_available = True
        logger.info("Database connection pool initialized successfully")
    except Exception as e:
        _pool = None
        _db_available = False
        logger.warning(
            f"Database not available — running in DEMO MODE with static data. "
            f"Error: {e}"
        )


async def close_db_pool():
    """Close the database connection pool."""
    global _pool, _db_available
    if _pool is not None:
        await _pool.close()
        _pool = None
        _db_available = False
        logger.info("Database connection pool closed")


def is_db_available() -> bool:
    """Check whether the database is connected."""
    return _db_available


@asynccontextmanager
async def get_db_connection() -> AsyncGenerator:
    """
    Yield an asyncpg connection from the pool.

    Usage:
        async with get_db_connection() as conn:
            rows = await conn.fetch("SELECT ...")
    """
    if _pool is None:
        raise RuntimeError("Database pool is not initialized")
    async with _pool.acquire() as conn:
        yield conn


async def fetch_rows(query: str, *args):
    """
    Execute a query and return all rows as list of Records.
    Returns None if database is not available (caller should fall back to demo data).
    """
    if not _db_available or _pool is None:
        return None
    try:
        async with _pool.acquire() as conn:
            return await conn.fetch(query, *args)
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        return None


async def fetch_row(query: str, *args):
    """
    Execute a query and return a single row.
    Returns None if database is not available.
    """
    if not _db_available or _pool is None:
        return None
    try:
        async with _pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        return None


async def fetch_val(query: str, *args):
    """
    Execute a query and return a single value.
    Returns None if database is not available.
    """
    if not _db_available or _pool is None:
        return None
    try:
        async with _pool.acquire() as conn:
            return await conn.fetchval(query, *args)
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        return None
