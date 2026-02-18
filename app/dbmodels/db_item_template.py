from sqlalchemy import Column, String, Text, ForeignKey, Numeric, Integer, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import DBBaseModel


class DBItemTemplate(DBBaseModel):
    __tablename__ = "item_templates"

    # inherits created_at: datetime, updated_at: datetime
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    weight = Column(Numeric(precision=10, scale=2), nullable=True)
    value = Column(Numeric(precision=10, scale=2), nullable=True)
    rarity = Column(String, nullable=True)
    type = Column(String, nullable=True)
    tags = Column(JSONB, nullable=True)
    gm_approved = Column(Boolean, nullable=True)
    game_system_id = Column(Integer, ForeignKey("game_systems.id"), nullable=False)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=True)
    player_character_id = Column(Integer, ForeignKey("player_characters.id"), nullable=True)
    user_uuid = Column(String, ForeignKey("users.uuid"), nullable=False)

    # # Relationships
    # game_system = relationship("DBGameSystem", back_populates="item_templates")
    # party = relationship("DBParty", back_populates="item_templates")
    # inventory_items = relationship("DBInventoryItem", back_populates="item_template")
    #
