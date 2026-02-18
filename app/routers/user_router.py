from fastapi import APIRouter, Depends
from typing import List
from app.apimodels import AuthUser, APIUserResponse
from app.services import UserService
from app.dependencies import get_user_service

user_router = APIRouter()

# @user_router.post("", response_model=APIUserResponse)
# def post_add_user(
#         auth_user: AuthUser,
#         service: UserService = Depends(get_user_service)
# ):
#     return service.add_user(auth_user)

@user_router.get("", response_model=List[APIUserResponse])
def get_all_users(
        service: UserService = Depends(get_user_service)
):
    return service.get_all_users()

@user_router.get("/{user_uuid}", response_model=APIUserResponse)
def get_user_by_id(
        user_uuid: str,
        service: UserService = Depends(get_user_service)
):
    return service.get_user_by_id(user_uuid)