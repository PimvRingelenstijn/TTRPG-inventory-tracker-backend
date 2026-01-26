from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import DBBaseModel


class DBInventory(DBBaseModel):
    __tablename__ = "inventories"

    inventory_name = Column(String, nullable=True)
    player_character_id = Column(Integer, ForeignKey("player_characters.id"), nullable=True)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    player_character = relationship(
        "DBPlayerCharacter",
        foreign_keys=[player_character_id],
        back_populates="inventory",
        uselist=False
    )
    inventory_items = relationship("DBInventoryItem", back_populates="inventory", cascade="all, delete-orphan")