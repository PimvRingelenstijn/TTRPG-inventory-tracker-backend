from typing import List
from app.apimodels import APIUserResponse
from app.repositories import UserRepository
from app.mappers import db_user_to_api_response

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all_users(self) -> List[APIUserResponse]:
        users = self.repository.get_all()
        return [db_user_to_api_response(user) for user in users]

    def get_user_by_id(self, user_uuid: str) -> APIUserResponse:
        user = self.repository.get_uuid(uuid_value=user_uuid)
        return db_user_to_api_response(user)