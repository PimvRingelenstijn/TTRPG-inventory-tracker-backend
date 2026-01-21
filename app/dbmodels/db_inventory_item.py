from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import BaseModel


class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"

    # Inherited columns: id, created_at, updated_at
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("inventories.id"), nullable=False)
    item_template_id = Column(UUID(as_uuid=True), ForeignKey("item_templates.id"), nullable=False)
    quantity = Column(Integer, default=1)

    # Relationships
    inventory = relationship("Inventory", back_populates="inventory_items")
    item_template = relationship("ItemTemplate", back_populates="inventory_items")
    change_logs = relationship("ChangeLog", back_populates="inventory_item", cascade="all, delete-orphan")