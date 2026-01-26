from typing import List

from app.apimodels import APIGameSystem, APIGameSystemResponse
from app.dbmodels import DBGameSystem
from app.mappers import GameSystemMapper
from app.repositories import GameSystemRepository


class GameSystemService:
    def __init__(self, repository: GameSystemRepository):
        self.repository = repository

    def add_game_system(self, api_system: APIGameSystem) -> APIGameSystemResponse:
        system: DBGameSystem = GameSystemMapper.api_game_system_to_db_game_system(api_system)
        created_system = self.repository.create(system.to_dict())
        return GameSystemMapper.game_system_to_api_game_system_response(created_system)

    def get_all_game_systems(self) -> List[APIGameSystemResponse]:
        systems = self.repository.get_all()
        return [GameSystemMapper.game_system_to_api_game_system_response(system) for system in systems]

    def get_game_system_by_id(self, system_id: int) -> APIGameSystemResponse:
        system = self.repository.get(id = system_id)
        return GameSystemMapper.game_system_to_api_game_system_response(system)