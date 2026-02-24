from supabase_auth import AuthResponse
from app.dtos import RegistrationRequest
from app.dbmodels import DBUser


def new_user_to_db_user(user_data: RegistrationRequest, auth_response: AuthResponse) -> DBUser:
    return DBUser(
        uuid=auth_response.user.id,
        username=user_data.username,
        created_at=auth_response.user.created_at
    )

