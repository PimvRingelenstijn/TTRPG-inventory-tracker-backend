from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import BaseModel


class System(BaseModel):
    __tablename__ = "systems"

    # Inherited columns: id, created_at, updated_at
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    parties = relationship("Party", back_populates="system", cascade="all, delete-orphan")
    item_templates = relationship("ItemTemplate", back_populates="system", cascade="all, delete-orphan")
    player_characters = relationship("PlayerCharacter", back_populates="system", cascade="all, delete-orphan")