from fastapi import APIRouter, Depends, status, Response
from fastapi.security import HTTPBearer
from typing import Dict, Any

from starlette.responses import Response

from app.apimodels import UserRegistration, UserLogin, LoginResponse
from app.dependencies import get_auth_service, get_current_user
from app.services import AuthService
from app.utils import set_cookies

auth_router = APIRouter()
security = HTTPBearer()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
        user_data: UserRegistration,
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.register_user(user_data)

@auth_router.post("/login")
def login_user(
        login_data: UserLogin,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
):
    #temporary return all AuthResponse data
    login_response: LoginResponse = auth_service.login_user(login_data)
    set_cookies(
        access_token=login_response.access_token,
        expires=login_response.expires,
        response=response
    )

    return login_response.userinfo

@auth_router.post("/logout")
def logout_user(response: Response):
    """Logout user by clearing cookies"""
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

@auth_router.get("/me")
def get_current_user_profile(
        current_user: Dict[str, Any] = Depends(get_current_user)
):
    return {"user": current_user}
