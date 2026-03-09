# Third-party imports
from fastapi import HTTPException, status
from supabase import Client
from supabase_auth import AuthResponse, User

# Local imports
from app.dbmodels import DBUser
from app.dtos import LoginRequest, LoginResult, RegistrationRequest, UserDataResponse
from app.mappers import (
    map_to_login_request,
    map_to_user_data_response,
    map_to_new_db_user,
)
from app.repositories import UserRepository


class AuthService:
    def __init__(self, supabase_client: Client, user_repository: UserRepository):
        self.client = supabase_client
        self.repository = user_repository

    def register_user(self, registration_data: RegistrationRequest) -> dict:
        try:
            # create user in Supabase Auth
            auth_response: AuthResponse = self.client.auth.sign_up({
                "email": registration_data.email,
                "password": registration_data.password
            })

            # store additional user data in your database
            new_user: DBUser = map_to_new_db_user(registration_data, auth_response.user)
            self.repository.create(new_user.to_dict())

            return {"Message": "User registered successfully!"}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Registration failed: {str(e)}"
            )


    def login_user(self, login_data: LoginRequest):
        try:
            auth_response: AuthResponse = self.client.auth.sign_in_with_password({
                "email": login_data.email,
                "password": login_data.password
            })
            db_user_data: DBUser = self.repository.get_uuid(auth_response.user.id)

            user_data_response: UserDataResponse = map_to_user_data_response(auth_response.user, db_user_data)

            login_response: LoginResult = map_to_login_request(auth_response.session, user_data_response)

            return login_response

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid credentials"
            )

    def get_user_data(self, user: User) -> UserDataResponse:
        """Get and return required user data"""
        db_user_data: DBUser = self.repository.get_uuid(user.id)
        user_data_response: UserDataResponse = map_to_user_data_response(user, db_user_data)

        return user_data_response
