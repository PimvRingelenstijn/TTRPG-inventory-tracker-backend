from typing import Optional, List
from sqlalchemy.orm import Session
from app.dbmodels import DBGameSystem
from app.repositories import BaseRepository

class GameSystemRepository(BaseRepository[DBGameSystem]):
    """Repository for Game-System model with additional game-system-specific methods"""
    
    def __init__(self, db: Session):
        super().__init__(DBGameSystem, db)


