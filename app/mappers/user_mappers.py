# Third-party imports
from supabase_auth import AuthResponse

# Local imports
from app.dbmodels import DBUser
from app.dtos import RegistrationRequest


def new_user_to_db_user(user_data: RegistrationRequest, auth_response: AuthResponse) -> DBUser:
    return DBUser(
        uuid=auth_response.user.id,
        username=user_data.username,
        created_at=auth_response.user.created_at
    )

