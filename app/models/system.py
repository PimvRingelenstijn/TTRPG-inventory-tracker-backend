from sqlalchemy import Column, String, Text
from app.models.base import BaseModel


class System(BaseModel):
    """System model for TTRPG systems"""
    __tablename__ = "systems"

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
