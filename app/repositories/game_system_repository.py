from typing import Optional, List
from sqlalchemy.orm import Session
from app.dbmodels import DBGameSystem
from app.repositories import BaseRepository

class GameSystemRepository(BaseRepository[DBGameSystem]):
    """Repository for Game-System model with additional game-system-specific methods"""
    
    def __init__(self, db: Session):
        super().__init__(DBGameSystem, db)

    def get_id(self, id_value: int) -> Optional[DBGameSystem]:
        """Get a single record by ID"""
        return self.db.query(self.model).filter(self.model.id == id_value).first()

