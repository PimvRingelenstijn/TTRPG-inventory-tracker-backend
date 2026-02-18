from supabase_auth import AuthResponse
from app.apimodels import LoginResponse, LoginUserInfo
from app.dbmodels import DBUser
from datetime import datetime, UTC

def login_request_to_login_response(auth_response: AuthResponse, login_user_info: LoginUserInfo) -> LoginResponse:

    expires_datetime = datetime.fromtimestamp(auth_response.session.expires_at, tz=UTC)

    return LoginResponse(
        access_token=auth_response.session.access_token,
        expires=expires_datetime,
        userinfo=login_user_info
    )

def user_data_to_user_info(auth_response: AuthResponse, user_data: DBUser) -> LoginUserInfo:
    return LoginUserInfo(
        uuid=auth_response.user.id,
        email=auth_response.user.email,
        username=user_data.username,
        created_at=user_data.created_at
    )
