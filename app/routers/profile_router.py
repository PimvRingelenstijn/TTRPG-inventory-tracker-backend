# Create a new router for protected endpoints, e.g., profile_router.py
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

profile_router = APIRouter()


@profile_router.get("/me")
def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Protected endpoint - requires authentication cookie"""
    return {"user": current_user}


@profile_router.get("/protected-data")
def get_protected_data(current_user: dict = Depends(get_current_user)):
    """Example of filtering data by user ID"""
    user_id = current_user["id"]

    # Use user_id to filter database queries
    # return filtered_data

    return {"message": f"Protected data for user {user_id}"}