from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from app.apimodels import UserRegistration, UserLogin
from app.dependencies import get_auth_service, get_current_user
from app.services import AuthService

auth_router = APIRouter()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
        user_data: UserRegistration,
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.register_user(user_data)

@auth_router.post("/login")
def login_user(
        login_data: UserLogin,
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.login_user(login_data)

@auth_router.post("/logout")
def logout_user():
    """Simple client-side logout"""
    return {"message": "Successfully logged out - clear token from client storage"}

@auth_router.get("/me")
def get_current_user_profile(
        current_user: Dict[str, Any] = Depends(get_current_user)
):
    return {"user": current_user}
