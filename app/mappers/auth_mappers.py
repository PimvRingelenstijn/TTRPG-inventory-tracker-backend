# Standard library imports
from datetime import UTC, datetime

# Third-party imports
from supabase_auth import Session, User

# Local imports
from app.dbmodels import DBUser
from app.dtos import LoginResult, UserDataResponse


def map_to_login_request(auth_session: Session, user_data_response: UserDataResponse) -> LoginResult:

    expires_datetime = datetime.fromtimestamp(auth_session.expires_at, tz=UTC)

    return LoginResult(
        access_token=auth_session.access_token,
        expires_at=expires_datetime,
        user_info=user_data_response
    )

def map_to_user_data_response(auth_user: User, db_user_data: DBUser) -> UserDataResponse:
    return UserDataResponse(
        uuid=auth_user.id,
        email=auth_user.email,
        username=db_user_data.username,
        created_at=db_user_data.created_at
    )
