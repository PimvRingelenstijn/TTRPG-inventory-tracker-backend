from fastapi import HTTPException, status
from supabase import Client
from supabase_auth import AuthResponse
from app.apimodels import UserRegistration, UserLogin, LoginResponse, LoginUserInfo
from app.dbmodels import DBUser
from app.mappers import new_user_to_db_user, login_request_to_login_response, user_data_to_user_info
from app.repositories import UserRepository


class AuthService:
    def __init__(self, supabase_client: Client, user_repository: UserRepository):
        self.client = supabase_client
        self.repository = user_repository

    def register_user(self, user_data: UserRegistration):
        try:
            # create user in Supabase Auth
            auth_response: AuthResponse = self.client.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password
            })

            # store additional user data in your database
            new_user: DBUser = new_user_to_db_user(user_data, auth_response)
            self.repository.create(new_user.to_dict())

            return {"Message": "User registered successfully!"}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Registration failed: {str(e)}"
            )

    def login_user(self, login_data: UserLogin):
        try:
            auth_response: AuthResponse = self.client.auth.sign_in_with_password({
                "email": login_data.email,
                "password": login_data.password
            })
            user_data: DBUser = self.repository.get_uuid(auth_response.user.id)

            login_user_info: LoginUserInfo = user_data_to_user_info(auth_response, user_data)

            login_response: LoginResponse = login_request_to_login_response(auth_response, login_user_info)

            return login_response

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

    def get_user_from_token(self, access_token: str):
        """Validate access token and return user info"""
        try:
            # Set the token and get user info from Supabase
            self.client.auth.set_session(access_token, "")
            user_response = self.client.auth.get_user()

            if user_response and user_response.user:
                return {
                    "id": user_response.user.id,
                    "email": user_response.user.email,
                    # Add any other user fields you need
                }
            return None
        except Exception:
            return None

