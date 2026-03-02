"""Dependency injection modules for the application.

This package provides:
- repository.py: Database repository and service dependencies
- auth.py: Supabase authentication dependencies
"""

from .auth import (
    get_auth_service,
)
from .service import get_protected_game_system_service, get_public_game_system_service

__all__ = [
    # From repository.py
    "get_public_game_system_service",
    "get_protected_game_system_service",
    # From auth.py
    "get_auth_service",
]