from app.dtos import APIGameSystem, APIGameSystemResponse
from app.dbmodels import DBGameSystem

def api_game_system_to_db_model(api_game_system: APIGameSystem) -> DBGameSystem:
    return DBGameSystem(
        name=api_game_system.name,
        description=api_game_system.description
    )

def db_game_system_to_api_response(db_game_system: DBGameSystem) -> APIGameSystemResponse:
    return APIGameSystemResponse(
        id=db_game_system.id,
        name=db_game_system.name,
        description=db_game_system.description
    )
