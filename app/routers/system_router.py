from fastapi import APIRouter, Depends

from app.apimodels import APISystem, APISystemResponse
from app.services import SystemService
from app.dependencies import get_system_service


class SystemRouter:
    router = APIRouter()

    @router.post("/add-system", response_model=APISystemResponse)
    def post_add_system(
        api_system: APISystem,
        service: SystemService = Depends(get_system_service)
    ):
        return service.add_system(api_system)
