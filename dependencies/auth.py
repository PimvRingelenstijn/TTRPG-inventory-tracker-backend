"""Authentication dependency injection flow for Supabase Auth."""
# Standard library imports
from typing import Optional

# Third-party imports
from fastapi import Depends, HTTPException, Request, status
from supabase import Client
from supabase_auth import User, UserResponse

# Local imports
import config
from app.repositories import UserRepository
from app.services import AuthService

# Import from sibling module
from .repository import get_public_repository


def get_supabase_client() -> Client:
    """Dependency to get the shared Supabase client instance."""
    if config.supabase_client is None:
        raise RuntimeError(
            "Supabase client not initialized. "
            "Check that the application started correctly and "
            "SUPABASE_URL and SUPABASE_SERVICE_KEY are set in .env"
        )
    return config.supabase_client

def get_access_token(request: Request) -> Optional[str]:
    """Get current user from access_token cookie"""
    return request.cookies.get("access_token")

async def get_authenticated_user(
        access_token: str = Depends(get_access_token)
) -> Optional[User]:
    """Get authenticated user or raise 401 if not authenticated."""
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        response: UserResponse = config.supabase_client.auth.get_user(access_token)
        if not response or not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        return response.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

async def get_current_user_uuid(
        user: User = Depends(get_authenticated_user)
) -> str:
    """Get current user's UUID (assumes authenticated)."""
    return user.id





# def get_user_from_token(access_token) -> Optional[User]:
#     response: UserResponse = config.supabase_client.auth.get_user(access_token)
#     return response.user if response else None
#
# def get_user_uuid_from_token(access_token) -> Optional[str]:
#     user = get_user_from_token(access_token)
#     return user.id if user else None



def get_auth_service(
        supabase_client: Client = Depends(get_supabase_client),
        user_repository: UserRepository = Depends(get_public_repository(repo_type=UserRepository))
) -> AuthService:
    """Dependency to get the AuthService instance."""
    return AuthService(supabase_client, user_repository)



# # Dependency to get current user (for protected routes)
# def get_user_data(
#         request: Request,  # Access to cookies
#         auth_service: AuthService = Depends(get_auth_service)
# ):
#     """Get current user from access_token cookie"""
#     access_token = request.cookies.get("access_token")
#
#     if not access_token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#         )
#
#     # Use Supabase to validate token
#     user_data: UserDataResponse = auth_service.get_user_data_from_token(access_token)
#     if not user_data:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token"
#         )
#     return user_data