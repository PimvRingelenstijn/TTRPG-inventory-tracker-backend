from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories import GameSystemRepository
from app.services import GameSystemService


def get_game_system_repository(db: Session = Depends(get_db)) -> GameSystemRepository:
    return GameSystemRepository(db)

def get_game_system_service(
    repository: GameSystemRepository = Depends(get_game_system_repository)
) -> GameSystemService:
    return GameSystemService(repository)
