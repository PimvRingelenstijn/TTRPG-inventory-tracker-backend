from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import BaseModel


class ChangeLog(BaseModel):
    __tablename__ = "change_logs"

    # Inherited columns: id, created_at, updated_at
    user_id = Column(String, nullable=False, index=True)  # From Supabase Auth
    player_character_id = Column(UUID(as_uuid=True), ForeignKey("player_characters.id"), nullable=True)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("inventories.id"), nullable=True)
    inventory_item_id = Column(UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=True)
    action = Column(String, nullable=False)  # e.g., "ADD_ITEM", "UPDATE_ITEM", "REMOVE_ITEM"
    description = Column(Text, nullable=True)  # Human-readable summary

    # Relationships
    player_character = relationship("PlayerCharacter", back_populates="change_logs")
    inventory = relationship("Inventory")
    inventory_item = relationship("InventoryItem", back_populates="change_logs")