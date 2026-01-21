from app.apimodels import APISystem, APISystemResponse
from app.dbmodels import System
from app.mappers import SystemMapper
from app.repositories import SystemRepository


class SystemService:
    def __init__(self, repository: SystemRepository):
        self.repository = repository

    def add_system(self, api_system: APISystem) -> APISystemResponse:
        system: System = SystemMapper.api_system_to_system(api_system)
        created_system = self.repository.add_new_system(system)
        return SystemMapper.system_to_api_system_response(created_system)
