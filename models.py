from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from database import Base


class System(Base):
    __tablename__ = "systems"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    parties = relationship("Party", back_populates="system")
    item_templates = relationship("ItemTemplate", back_populates="system")
    player_characters = relationship("PlayerCharacter", back_populates="system")


class Party(Base):
    __tablename__ = "parties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    system_id = Column(UUID(as_uuid=True), ForeignKey("systems.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    system = relationship("System", back_populates="parties")
    player_characters = relationship("PlayerCharacter", back_populates="party")
    item_templates = relationship("ItemTemplate", back_populates="party")


class ItemTemplate(Base):
    __tablename__ = "item_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    system_id = Column(UUID(as_uuid=True), ForeignKey("systems.id"), nullable=False)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.id"), nullable=True)
    weight = Column(Numeric(precision=10, scale=2), nullable=True)
    value = Column(Numeric(precision=10, scale=2), nullable=True)
    rarity = Column(String, nullable=True)
    type = Column(String, nullable=True)
    tags = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    system = relationship("System", back_populates="item_templates")
    party = relationship("Party", back_populates="item_templates")
    inventory_items = relationship("InventoryItem", back_populates="item_template")


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    player_character = relationship("PlayerCharacter", back_populates="inventory", uselist=False)
    inventory_items = relationship("InventoryItem", back_populates="inventory")


class PlayerCharacter(Base):
    __tablename__ = "player_characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(String, nullable=False, index=True)  # From Supabase Auth
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    system_id = Column(UUID(as_uuid=True), ForeignKey("systems.id"), nullable=False)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("inventories.id"), unique=True, nullable=False)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    system = relationship("System", back_populates="player_characters")
    party = relationship("Party", back_populates="player_characters")
    inventory = relationship("Inventory", back_populates="player_character")
    change_logs = relationship("ChangeLog", back_populates="player_character")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("inventories.id"), nullable=False)
    item_template_id = Column(UUID(as_uuid=True), ForeignKey("item_templates.id"), nullable=False)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    inventory = relationship("Inventory", back_populates="inventory_items")
    item_template = relationship("ItemTemplate", back_populates="inventory_items")
    change_logs = relationship("ChangeLog", back_populates="inventory_item")


class ChangeLog(Base):
    __tablename__ = "change_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(String, nullable=False, index=True)  # From Supabase Auth
    player_character_id = Column(UUID(as_uuid=True), ForeignKey("player_characters.id"), nullable=True)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("inventories.id"), nullable=True)
    inventory_item_id = Column(UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=True)
    action = Column(String, nullable=False)  # e.g., "ADD_ITEM", "UPDATE_ITEM", "REMOVE_ITEM"
    description = Column(Text, nullable=True)  # Human-readable summary
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    player_character = relationship("PlayerCharacter", back_populates="change_logs")
    inventory = relationship("Inventory")
    inventory_item = relationship("InventoryItem", back_populates="change_logs")