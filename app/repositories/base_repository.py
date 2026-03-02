# Standard library imports
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

# Third-party imports
from sqlalchemy.orm import Session

# Local imports
from app.dbmodels import DBBaseModel

ModelType = TypeVar("ModelType", bound=DBBaseModel)

class BaseRepository(Generic[ModelType]):
    """Base repository class with common CRUD operations"""
    
    def __init__(self, model: Type[ModelType], db: Session, user_uuid: Optional[str] = None):
        self.model = model
        self.db = db
        self.user_uuid = user_uuid

    def _apply_user_filter(self, query):
        """Apply user filter if user_uuid is set"""
        if self.user_uuid:
            return query.filter(self.model.user_uuid == self.user_uuid)
        return query

    def _inject_user_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.user_uuid and hasattr(self.model, 'user_uuid'):
            if 'user_uuid' not in data:
                data = {**data, 'user_uuid': self.user_uuid}
        return data

    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
