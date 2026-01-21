from app.apimodels import APISystem, APISystemResponse
from app.dbmodels import System
from app.mappers import SystemMapper
from app.repositories import SystemRepository

class SystemService:
    @staticmethod
    def add_system(api_system: APISystem) -> APISystemResponse:
        """Add new system"""
        system: System = SystemMapper.api_system_to_system(api_system)
        SystemRepository.add_new_system(system)
        return SystemMapper.system_to_api_system_response(system)
