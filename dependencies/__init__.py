"""Dependency injection modules for the application.

This package provides:
- repository.py: Database repository and service dependencies
- auth.py: Supabase authentication dependencies
"""

from .service import get_game_system_service, get_auth_service
from .auth import get_authenticated_user

__all__ = [
    # From services.py
    "get_game_system_service",
    "get_auth_service",
    # From auth.py
    "get_authenticated_user"
]