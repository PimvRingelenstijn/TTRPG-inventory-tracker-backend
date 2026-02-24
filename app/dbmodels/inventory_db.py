from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.dbmodels.base_db import DBBaseModel


class DBInventory(DBBaseModel):
    __tablename__ = "inventories"

    # inherits created_at: datetime, updated_at: datetime
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    player_character_id = Column(Integer, ForeignKey("player_characters.id"), nullable=True)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=True)
    user_uuid = Column(String, ForeignKey("users.uuid"), nullable=True)

    # # Relationships
    # player_character = relationship(
    #     "DBPlayerCharacter",
    #     foreign_keys=[player_character_id],
    #     back_populates="inventory",
    #     uselist=False
    # )
    # inventory_items = relationship("DBInventoryItem", back_populates="inventory", cascade="all, delete-orphan")
    #

