from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories import SystemRepository
from app.services import SystemService


def get_system_repository(db: Session = Depends(get_db)) -> SystemRepository:
    return SystemRepository(db)


def get_system_service(
    repository: SystemRepository = Depends(get_system_repository)
) -> SystemService:
    return SystemService(repository)
