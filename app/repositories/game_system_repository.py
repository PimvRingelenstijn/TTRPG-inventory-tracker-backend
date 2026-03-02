# Standard library imports
from typing import List, Optional

# Third-party imports
from sqlalchemy.orm import Session

# Local imports
from app.dbmodels import DBGameSystem
from app.repositories import BaseRepository


class GameSystemRepository(BaseRepository[DBGameSystem]):
    """Repository for Game-System model with additional game-system-specific methods"""
    
    def __init__(self, db: Session, user_uuid: Optional[str] = None):
        super().__init__(DBGameSystem, db, user_uuid)

    def get_id(self, id_value: int) -> Optional[DBGameSystem]:
        """Get a single record by ID"""
        return self.db.query(self.model).filter(self.model.id == id_value).first()

