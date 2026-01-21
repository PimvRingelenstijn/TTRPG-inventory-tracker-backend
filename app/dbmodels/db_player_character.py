from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.dbmodels.db_base import BaseModel


# In your PlayerCharacter model:
class PlayerCharacter(BaseModel):
    __tablename__ = "player_characters"

    user_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    system_id = Column(UUID(as_uuid=True), ForeignKey("systems.id"), nullable=False)
    party_id = Column(UUID(as_uuid=True), ForeignKey("parties.id"), nullable=True)

    # Relationships with explicit foreign_keys
    system = relationship("System", back_populates="player_characters")
    party = relationship("Party", back_populates="player_characters")

    inventory = relationship(
        "Inventory",
        back_populates="player_character",
        uselist=False  # One-to-one relationship
    )
    change_logs = relationship("ChangeLog", back_populates="player_character", cascade="all, delete-orphan")