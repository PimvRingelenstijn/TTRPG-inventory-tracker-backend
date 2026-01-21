from fastapi import APIRouter

from app.apimodels import APISystem, APISystemResponse
from app.services import SystemService


class SystemRouter:
    router = APIRouter()

    @staticmethod
    @router.post("/add-system", response_model=APISystemResponse)
    def post_add_system(api_system: APISystem):
        """Add a new system"""
        return SystemService.add_system(api_system)

