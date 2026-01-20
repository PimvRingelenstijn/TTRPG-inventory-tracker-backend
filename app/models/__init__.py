# Import all models here so SQLAlchemy registers them with Base.metadata
from app.models.base import BaseModel
from app.models.system import System

__all__ = ["BaseModel", "System"]
