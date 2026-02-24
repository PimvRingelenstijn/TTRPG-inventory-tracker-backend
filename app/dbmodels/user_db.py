from sqlalchemy import Column, String
from app.dbmodels.base_db import DBBaseModel

class DBUser(DBBaseModel):
    __tablename__ = "users"

    # inherits created_at: datetime, updated_at: datetime
    uuid = Column(String, primary_key=True)
    username = Column(String, nullable=False)

