from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import DBBaseModel


class DBParty(DBBaseModel):
    __tablename__ = "parties"

    # inherits created_at: datetime, updated_at: datetime
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    game_system_id = Column(Integer, ForeignKey("game_systems.id"), nullable=False)
    user_uuid = Column(String, ForeignKey("users.uuid"), nullable=False)


    # # Relationships (MANY parties belong to ONE system)
    # game_system = relationship("DBGameSystem", back_populates="parties")
    #
    # # Relationships (ONE party has MANY of these)
    # player_characters = relationship("DBPlayerCharacter", back_populates="party", cascade="all, delete-orphan")
    # item_templates = relationship("DBItemTemplate", back_populates="party", cascade="all, delete-orphan")
    #

