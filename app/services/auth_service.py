from fastapi import HTTPException, status
from supabase import Client
from supabase_auth import AuthResponse
from app.apimodels import UserRegistration, UserLogin
from app.dbmodels import DBUser
from app.mappers import new_user_to_db_user
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

            return {
                "user": auth_response.user.model_dump(),
                "session": auth_response.session.model_dump()
            }

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

    def get_current_user(self, token: str):
        """Validate JWT and get current user"""
        try:
            self.client.auth.set_session(token, "")
            user = self.client.auth.get_user()
            return user.user.dict() if user else None
        except:
            return None

    # def logout_user(self) -> bool:
    #     try:
    #         self.client.auth.sign_out()
    #         return True
    #     except:
    #         return False
