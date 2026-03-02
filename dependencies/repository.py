"""Database dependency injection flow for repositories."""

# Standard library imports
from typing import Type, TypeVar

# Third-party imports
from fastapi import Depends
from sqlalchemy.orm import Session

# Local imports
from db import get_db

from .auth import get_current_user_uuid

RepositoryType = TypeVar("RepositoryType")

def get_public_repository(repo_type: Type[RepositoryType]):
    """Public repository factory - no user context."""
    def _get_public_repository(db: Session = Depends(get_db)) -> RepositoryType:
        return repo_type(db)
    return _get_public_repository

def get_protected_repository(repo_type: Type[RepositoryType]):
    """Protected repository factory - with user context."""
    def _get_protected_repository(
        db: Session = Depends(get_db),
        user_uuid: str = Depends(get_current_user_uuid)
    ) -> RepositoryType:
        return repo_type(db, user_uuid=user_uuid)
    return _get_protected_repository


# def get_repository(repo_type: Type[RepositoryType]):
#     """Generic factory for repository dependencies."""
#     def _get_repository(db: Session = Depends(get_db)) -> RepositoryType:
#         return repo_type(db)
#     return _get_repository
