from app.apimodels import APISystem, APISystemResponse
from app.dbmodels import System

class SystemMapper:
    @staticmethod
    def api_system_to_system(api_system: APISystem) -> System:
        return System(name=api_system.name, description=api_system.description)

    @staticmethod
    def system_to_api_system_response(system: System) -> APISystemResponse:
        return APISystemResponse(
            id=system.id,
            name=system.name,
            description=system.description
        )