from typing import Optional, List
from sqlalchemy.orm import Session
from app.dbmodels import System
from app.repositories import BaseRepository


class SystemRepository(BaseRepository[System]):
    """Repository for System model with additional system-specific methods"""
    
    def __init__(self, db: Session):
        super().__init__(System, db)

    def add_new_system(self, system: System) -> System:
        return self.create(system.to_dict())

