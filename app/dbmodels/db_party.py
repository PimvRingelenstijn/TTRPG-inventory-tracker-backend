from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import BaseModel


class Party(BaseModel):
    __tablename__ = "parties"

    # Inherited columns: id, created_at, updated_at
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    system_id = Column(UUID(as_uuid=True), ForeignKey("systems.id"), nullable=False)

    # Relationships
    system = relationship("System", back_populates="parties")
    player_characters = relationship("PlayerCharacter", back_populates="party", cascade="all, delete-orphan")
    item_templates = relationship("ItemTemplate", back_populates="party", cascade="all, delete-orphan")