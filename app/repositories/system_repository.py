from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.system import System
from app.repositories.base import BaseRepository


class SystemRepository(BaseRepository[System]):
    """Repository for System model with additional system-specific methods"""
    
    def __init__(self, db: Session):
        super().__init__(System, db)
    
    def get_by_name(self, name: str) -> Optional[System]:
        """Get system by name"""
        return self.db.query(System).filter(System.name == name).first()
    
    def search_by_name(self, name_pattern: str) -> List[System]:
        """Search systems by name pattern (case-insensitive partial match)"""
        return self.db.query(System).filter(
            System.name.ilike(f"%{name_pattern}%")
        ).all()
