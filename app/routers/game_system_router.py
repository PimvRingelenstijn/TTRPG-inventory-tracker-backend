from fastapi import APIRouter, Depends
from typing import List
from app.apimodels import APIGameSystem, APIGameSystemResponse
from app.services import GameSystemService
from app.dependencies import get_game_system_service

game_system_router = APIRouter()

@game_system_router.post("", response_model=APIGameSystemResponse)
def post_add_game_system(
        api_game_system: APIGameSystem,
        service: GameSystemService = Depends(get_game_system_service)
):
    return service.add_game_system(api_game_system)

@game_system_router.get("", response_model=List[APIGameSystemResponse])
def get_all_game_systems(
        service: GameSystemService = Depends(get_game_system_service)
):
    return service.get_all_game_systems()

@game_system_router.get("/{system_id}", response_model=APIGameSystemResponse)
def get_game_system_by_id(
        game_system_id: int,
        service: GameSystemService = Depends(get_game_system_service)
):
    return service.get_game_system_by_id(game_system_id)
