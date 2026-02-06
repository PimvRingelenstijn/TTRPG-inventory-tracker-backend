from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any, Type, TypeVar
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories import GameSystemRepository, UserRepository
from app.services import GameSystemService, UserService


"""Dependency injection flow to connect to Supabase Database"""
RepositoryType = TypeVar("RepositoryType")
ServiceType = TypeVar("ServiceType")

# Generic repository dependency function
def get_repository(repo_type: Type[RepositoryType]):
    def _get_repository(db: Session = Depends(get_db)) -> RepositoryType:
        return repo_type(db)
    return _get_repository

# Generic service dependency function
def get_service(service_type: Type[ServiceType], repo_type: Type[RepositoryType]):
    def _get_service(
        repository: repo_type = Depends(get_repository(repo_type))
    ) -> ServiceType:
        return service_type(repository)
    return _get_service

# Convenience functions for specific services
get_game_system_service = get_service(GameSystemService, GameSystemRepository)
get_user_service = get_service(UserService, UserRepository)

#get_change_log_service = get_service(ChangeLogService, ChangeLogRepository)
#get_inventory_service = get_service(InventoryService, InventoryRepository)
#get_inventory_item_service = get_service(InventoryItemService, InventoryItemRepository)
#get_item_template_service = get_service(ItemTemplateService, ItemTemplateRepository)
#get_party_service = get_service(PartyService, PartyRepository)
#get_player_character_service = get_service(PlayerCharacterService, PlayerCharacterRepository)

""""Dependency injection flow to connect to Supabase Auth"""
from supabase import Client
from app.clients import get_supabase_client
from app.services import AuthService

# Authentication service dependency
def get_auth_service(
        supabase_client: Client = Depends(get_supabase_client),
        user_repository: UserRepository = Depends(get_repository(repo_type = UserRepository))
) -> AuthService:
    return AuthService(supabase_client, user_repository)

# Dependency to get current user (for protected routes)
def get_current_user(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")),
        auth_service: AuthService = Depends(get_auth_service)
)-> Dict[str, Any]:
    user = auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
