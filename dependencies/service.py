"""Database dependency injection flow for services."""

# Standard library imports
from typing import Optional, Type, TypeVar

# Third-party imports
from fastapi import Depends, HTTPException, status
from supabase import Client

# Local imports
from app.repositories import GameSystemRepository, UserRepository
from app.services import GameSystemService, UserService

from .auth import get_access_token, get_supabase_client
from .repository import get_protected_repository, get_public_repository

RepositoryType = TypeVar("RepositoryType")
ServiceType = TypeVar("ServiceType")

# src/dependencies/service.py
def get_public_service(service_type: Type[ServiceType], repo_type: Type[RepositoryType]):
    """Factory for public services."""
    def _get_public_service(
        repository: repo_type = Depends(get_public_repository(repo_type))
    ) -> service_type:
        return service_type(repository)
    return _get_public_service

def get_protected_service(service_type: Type[ServiceType], repo_type: Type[RepositoryType]):
    """Factory for protected services - user is automatically authenticated."""
    def _get_protected_service(
        repository: repo_type = Depends(get_protected_repository(repo_type))
    ) -> service_type:
        return service_type(repository)
    return _get_protected_service

# Specific service dependencies
get_public_game_system_service = get_public_service(GameSystemService, GameSystemRepository)
get_protected_game_system_service = get_protected_service(GameSystemService, GameSystemRepository)

# def get_service(
#         service_type: Type[ServiceType],
#         repo_type: Type[RepositoryType],
#         protected: bool = True, # set to false in router layer
#         access_token: Optional[str] = Depends(get_access_token)
# ):
#     # check for protected route
#     if protected and not access_token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#         )
#
#     """Generic factory for service dependencies."""
#     def _get_service(
#         client: Client = Depends(get_supabase_client),
#         repository: RepositoryType = Depends(get_repository(repo_type))
#     ) -> ServiceType:
#         return service_type(client, repository)
#     return _get_service
#
#
# # Convenience functions for specific services
# def get_game_system_service(protected: bool = True):
#     return get_service(GameSystemService, GameSystemRepository, protected)
#
# def get_user_service(protected: bool = True):
#     return get_service(UserService, UserRepository, protected)

#get_change_log_service = get_service(ChangeLogService, ChangeLogRepository)
#get_inventory_service = get_service(InventoryService, InventoryRepository)
#get_inventory_item_service = get_service(InventoryItemService, InventoryItemRepository)
#get_item_template_service = get_service(ItemTemplateService, ItemTemplateRepository)
#get_party_service = get_service(PartyService, PartyRepository)
#get_player_character_service = get_service(PlayerCharacterService, PlayerCharacterRepository)