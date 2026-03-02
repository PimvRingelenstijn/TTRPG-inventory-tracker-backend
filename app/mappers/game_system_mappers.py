# Local imports
from app.dbmodels import DBGameSystem
from app.dtos import GameSystemCreateRequest, GameSystemDataResponse


def api_game_system_to_db_model(api_game_system: GameSystemCreateRequest) -> DBGameSystem:
    return DBGameSystem(
        name=api_game_system.name,
        description=api_game_system.description
    )

def db_game_system_to_api_response(db_game_system: DBGameSystem) -> GameSystemDataResponse:
    return GameSystemDataResponse(
        id=db_game_system.id,
        name=db_game_system.name,
        description=db_game_system.description
    )
