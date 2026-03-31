# API Routes Module
# Phase 8 - Safe API Routes

from fastapi import APIRouter
from . import revenue, trade, compliance, metadata

__all__ = ['revenue', 'trade', 'compliance', 'metadata']