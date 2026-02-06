from sqlalchemy.orm import Session
from app.dbmodels import DBUser
from app.repositories import BaseRepository


class UserRepository(BaseRepository[DBUser]):
    """Repository for user model with additional user-specific methods"""

    def __init__(self, db: Session):
        super().__init__(DBUser, db)