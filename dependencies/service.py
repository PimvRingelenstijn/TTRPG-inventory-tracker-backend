"""Database dependency injection flow for services."""

# Standard library imports
from typing import Type, TypeVar

# Third-party imports
from fastapi import Depends
from supabase import Client

# Local imports
from app.repositories import GameSystemRepository, UserRepository
from app.services import GameSystemService, UserService, AuthService

from .auth import get_supabase_client
from .repository import get_repository

RepositoryType = TypeVar("RepositoryType")
ServiceType = TypeVar("ServiceType")

# src/dependencies/service.py
def get_service(service_type: Type[ServiceType], repo_type: Type[RepositoryType]):
    """Factory for public services."""
    def _get_service(
        repository: repo_type = Depends(get_repository(repo_type))
    ) -> service_type:
        return service_type(repository)
    return _get_service

# Specific service dependencies
get_game_system_service = get_service(GameSystemService, GameSystemRepository)
get_user_service = get_service(UserService, UserRepository)
#get_change_log_service = get_service(ChangeLogService, ChangeLogRepository)
#get_inventory_service = get_service(InventoryService, InventoryRepository)
#get_inventory_item_service = get_service(InventoryItemService, InventoryItemRepository)
#get_item_template_service = get_service(ItemTemplateService, ItemTemplateRepository)
#get_party_service = get_service(PartyService, PartyRepository)
#get_player_character_service = get_service(PlayerCharacterService, PlayerCharacterRepository)


def get_auth_service(
        supabase_client: Client = Depends(get_supabase_client),
        user_repository: UserRepository = Depends(get_repository(repo_type=UserRepository))
) -> AuthService:
    """Dependency to get the AuthService instance."""
    return AuthService(supabase_client, user_repository)

