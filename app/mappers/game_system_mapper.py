from app.apimodels import APIGameSystem, APIGameSystemResponse
from app.dbmodels import DBGameSystem


class GameSystemMapper:
    @staticmethod
    def api_game_system_to_db_game_system(api_system: APIGameSystem) -> DBGameSystem:
        return DBGameSystem(name=api_system.name, description=api_system.description)

    @staticmethod
    def game_system_to_api_game_system_response(system: DBGameSystem) -> APIGameSystemResponse:
        return APIGameSystemResponse(
            id=system.id,
            name=system.name,
            description=system.description
        )
