# Standard library imports
from typing import List

# Local imports
from app.dbmodels import DBGameSystem
from app.dtos import GameSystemCreateRequest, GameSystemDataResponse
from app.mappers import api_game_system_to_db_model, db_game_system_to_api_response
from app.repositories import GameSystemRepository


class GameSystemService:
    def __init__(self, repository: GameSystemRepository):
        self.repository = repository

    def add_game_system(self, api_game_system: GameSystemCreateRequest) -> GameSystemDataResponse:
        game_system: DBGameSystem = api_game_system_to_db_model(api_game_system)
        created_game_system = self.repository.create(game_system.to_dict())
        return db_game_system_to_api_response(created_game_system)

    def get_all_game_systems(self) -> List[GameSystemDataResponse]:
        game_systems = self.repository.get_all()
        return [db_game_system_to_api_response(game_system) for game_system in game_systems]

    def get_game_system_by_id(self, game_system_id: int) -> GameSystemDataResponse:
        game_system = self.repository.get_id(id_value=game_system_id)
        return db_game_system_to_api_response(game_system)

