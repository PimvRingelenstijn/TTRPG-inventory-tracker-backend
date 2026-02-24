from fastapi import HTTPException, status
from supabase import Client
from supabase_auth import AuthResponse
from app.dtos import RegistrationRequest, LoginRequest, LoginResult, UserDataResponse
from app.dbmodels import DBUser
from app.mappers import new_user_to_db_user, map_to_login_request, map_to_user_data_response
from app.repositories import UserRepository


class AuthService:
    def __init__(self, supabase_client: Client, user_repository: UserRepository):
        self.client = supabase_client
        self.repository = user_repository

    def register_user(self, user_data: RegistrationRequest):
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

    def login_user(self, login_data: LoginRequest):
        try:
            auth_response: AuthResponse = self.client.auth.sign_in_with_password({
                "email": login_data.email,
                "password": login_data.password
            })
            db_user_data: DBUser = self.repository.get_uuid(auth_response.user.id)

            user_data_response: UserDataResponse = map_to_user_data_response(auth_response.user, db_user_data)

            login_response: LoginResult = map_to_login_request(auth_response, user_data_response)

            return login_response

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

    def get_user_data_from_token(self, access_token: str):
        """Validate access token and return user info"""
        # Set the token and get user info from Supabase
        self.client.auth.set_session(access_token, "")
        auth_user = self.client.auth.get_user()

        db_user_data: DBUser = self.repository.get_uuid(auth_user.user.id)

        user_data_response: UserDataResponse = map_to_user_data_response(auth_user.user, db_user_data)

        return user_data_response


