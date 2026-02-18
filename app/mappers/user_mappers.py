from supabase_auth import AuthResponse
from app.apimodels import APIUserResponse, UserRegistration
from app.dbmodels import DBUser


def new_user_to_db_user(user_data: UserRegistration, auth_response: AuthResponse) -> DBUser:
    return DBUser(
        uuid=auth_response.user.id,
        username=user_data.username,
        created_at=auth_response.user.created_at
    )

def db_user_to_api_response(db_user: DBUser) -> APIUserResponse:
    return APIUserResponse(
        uuid=db_user.uuid,
        username=db_user.username
    )