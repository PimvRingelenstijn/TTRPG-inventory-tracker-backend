from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import DBBaseModel


class DBGameSystem(DBBaseModel):
    __tablename__ = "game_systems"

    # inherits id: int (pk), created_at: datetime, updated_at: datetime
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # # Relationships (ONE system has MANY of these)
    # parties = relationship("DBParty", back_populates="game_system", cascade="all, delete-orphan")
    # item_templates = relationship("DBItemTemplate", back_populates="game_system", cascade="all, delete-orphan")
    # player_characters = relationship("DBPlayerCharacter", back_populates="game_system", cascade="all, delete-orphan")
    #

