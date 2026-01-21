from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import BaseModel


# In your Inventory model:
class Inventory(BaseModel):
    __tablename__ = "inventories"

    player_character_id = Column(UUID(as_uuid=True), ForeignKey("player_characters.id"), nullable=False)

    # Specify which foreign key this relationship uses
    player_character = relationship(
        "PlayerCharacter",
        foreign_keys=[player_character_id],  # THIS LINE IS CRITICAL
        back_populates="inventory",
        uselist=False
    )
    inventory_items = relationship("InventoryItem", back_populates="inventory", cascade="all, delete-orphan")