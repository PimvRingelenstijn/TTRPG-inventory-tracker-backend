from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import DBBaseModel


class DBPlayerCharacter(DBBaseModel):
    __tablename__ = "player_characters"

    # inherits id: int (pk), created_at: datetime, updated_at: datetime
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_system_id = Column(Integer, ForeignKey("game_systems.id"), nullable=True)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=True)

    # # Relationships (MANY characters belong to ONE system/party)
    # game_system = relationship("DBGameSystem", back_populates="player_characters")
    # party = relationship("DBParty", back_populates="player_characters")
    # user = relationship("DBUser", back_populates="player_character")

    # # Relationships (ONE character has ONE inventory, MANY change logs)
    # inventory = relationship("DBInventory", back_populates="player_character", uselist=False)
    # change_logs = relationship("DBChangeLog", back_populates="player_character")
    #

