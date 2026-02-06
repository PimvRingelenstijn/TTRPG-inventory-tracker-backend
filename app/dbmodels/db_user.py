from sqlalchemy import Column, String, UUID
from app.dbmodels.db_base import DBBaseModel


class DBUser(DBBaseModel):
    __tablename__ = "users"

    # inherits id: int (pk), created_at: datetime, updated_at: datetime
    uuid = Column(UUID, nullable=False, index=True)
    name = Column(String, nullable=False)

