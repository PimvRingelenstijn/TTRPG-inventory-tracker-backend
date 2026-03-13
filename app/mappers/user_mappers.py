# Third-party imports
from supabase_auth import User

# Local imports
from app.dbmodels import DBUser
from app.dtos import RegistrationRequest


def map_to_new_db_user(registration_data: RegistrationRequest, auth_user: User) -> DBUser:
    return DBUser(
        uuid=auth_user.id,
        username=registration_data.username,
        created_at=auth_user.created_at
    )

