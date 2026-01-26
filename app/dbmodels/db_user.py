from sqlalchemy import Column, String, UUID
from app.dbmodels.db_base import DBBaseModel


class DBUser(DBBaseModel):
    __tablename__ = "users"

    user_uid = Column(UUID, nullable=False, index=True)
    user_name = Column(String, nullable=False)

    # Relationships
    #   change log
    #   game_system
    #   inventory
    #   item_template
    #   party
    #   player_character