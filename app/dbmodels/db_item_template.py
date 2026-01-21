from sqlalchemy import Column, String, Text, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import BaseModel


class ItemTemplate(BaseModel):
    __tablename__ = "item_templates"

    # Inherited columns: id, created_at, updated_at
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    system_id = Column(UUID(as_uuid=True), ForeignKey("systems.id"), nullable=False)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.id"), nullable=True)
    weight = Column(Numeric(precision=10, scale=2), nullable=True)
    value = Column(Numeric(precision=10, scale=2), nullable=True)
    rarity = Column(String, nullable=True)
    type = Column(String, nullable=True)
    tags = Column(JSONB, nullable=True)

    # Relationships
    system = relationship("System", back_populates="item_templates")
    party = relationship("Party", back_populates="item_templates")
    inventory_items = relationship("InventoryItem", back_populates="item_template", cascade="all, delete-orphan")