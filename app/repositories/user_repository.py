# Standard library imports
from typing import Optional

# Third-party imports
from sqlalchemy.orm import Session

# Local imports
from app.dbmodels import DBUser
from app.repositories import BaseRepository


class UserRepository(BaseRepository[DBUser]):
    """Repository for user model with additional user-specific methods"""

    def __init__(self, db: Session):
        super().__init__(DBUser, db)

    def get_uuid(self, uuid_value: str) -> Optional[DBUser]:
        """Get a single record by ID"""
        return self.db.query(self.model).filter(self.model.uuid == uuid_value).first()