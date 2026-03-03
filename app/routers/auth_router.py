# Third-party imports
from fastapi import APIRouter, Depends, Response, status
from supabase_auth import User

# Local imports
from app.dtos import LoginRequest, LoginResult, RegistrationRequest, UserDataResponse
from app.services import AuthService
from app.utils import set_cookies
from dependencies import get_auth_service, get_authenticated_user

auth_router = APIRouter()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
        user_data: RegistrationRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.register_user(user_data)

@auth_router.post("/login", response_model=UserDataResponse)
def login_user(
        login_data: LoginRequest,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
):
    #temporary return all AuthResponse data
    login_result: LoginResult = auth_service.login_user(login_data)
    set_cookies(
        access_token=login_result.access_token,
        expires=login_result.expires,
        response=response
    )

    return login_result.user_info

@auth_router.post("/logout")
def logout_user(response: Response):
    """Logout user by clearing cookies"""
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

@auth_router.get("/me", response_model=UserDataResponse)
def get_user_data(
        user: User = Depends(get_authenticated_user),
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.get_user_data(user)
