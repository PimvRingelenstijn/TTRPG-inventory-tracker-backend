# Standard library imports
from typing import List

# Third-party imports
from fastapi import APIRouter, Depends

# Local imports
from app.dtos import GameSystemCreateRequest, GameSystemDataResponse
from app.services import GameSystemService
from dependencies import (
    get_game_system_service,
)
from dependencies.auth import get_authenticated_user

game_system_router = APIRouter()

@game_system_router.post("", response_model=GameSystemDataResponse)
def post_add_game_system(
        game_system_info: GameSystemCreateRequest,
        game_system_service: GameSystemService = Depends(get_game_system_service)
):

    return game_system_service.add_game_system(game_system_info)

@game_system_router.get("", response_model=List[GameSystemDataResponse])
def get_all_game_systems(
        game_system_service: GameSystemService = Depends(get_game_system_service)
):
    return game_system_service.get_all_game_systems()

@game_system_router.get("/{system_id}", response_model=GameSystemDataResponse)
def get_game_system_by_id(
        game_system_id: int,
        game_system_service: GameSystemService = Depends(get_game_system_service)
):
    return game_system_service.get_game_system_by_id(game_system_id)
