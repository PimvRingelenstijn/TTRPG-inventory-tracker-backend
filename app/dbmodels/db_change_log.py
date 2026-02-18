from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import DBBaseModel


class DBChangeLog(DBBaseModel):
    __tablename__ = "change_logs"

    # inherits created_at: datetime, updated_at: datetime
    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(String, ForeignKey("users.uuid"), nullable=False, index=True)
    player_character_id = Column(Integer, ForeignKey("player_characters.id"), nullable=True)
    inventory_id = Column(Integer, ForeignKey("inventories.id"), nullable=True)
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)
    action = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # # Relationships
    # player_character = relationship("DBPlayerCharacter", back_populates="change_logs")
    # inventory = relationship("DBInventory")
    # inventory_item = relationship("DBInventoryItem", back_populates="change_logs")
    #



