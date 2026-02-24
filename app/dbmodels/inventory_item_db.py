from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.dbmodels.base_db import DBBaseModel


class DBInventoryItem(DBBaseModel):
    __tablename__ = "inventory_items"

    # inherits created_at: datetime, updated_at: datetime
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventories.id"), nullable=False)
    item_template_id = Column(Integer, ForeignKey("item_templates.id"), nullable=False)
    quantity = Column(Integer, default=1)

    # # Relationships
    # inventory = relationship("DBInventory", back_populates="inventory_items")
    # item_template = relationship("DBItemTemplate", back_populates="inventory_items")
    # change_logs = relationship("DBChangeLog", back_populates="inventory_item")
    #
