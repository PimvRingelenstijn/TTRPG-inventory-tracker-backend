# Standard library imports
import os
from datetime import UTC, datetime

# Third-party imports
import pytest

from app.dtos import UserDataResponse

# Set dummy env vars before any app imports
os.environ.setdefault("USER", "test_user")
os.environ.setdefault("PASSWORD", "test_password")
os.environ.setdefault("HOST", "localhost")
os.environ.setdefault("PORT", "5432")
os.environ.setdefault("DBNAME", "test_db")
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_KEY", "test-service-key")


# @pytest.fixture
# def mock_supabase_client(mocker):
#     mock = mocker.Mock()
#     return mock

# @pytest.fixture
# def mock_supabase_client() -> Generator[MagicMock, None, None]:
#     """Fixture providing a mocked Supabase client"""
#     mock_client = MagicMock()
#     mock_auth = MagicMock()
#     mock_client.mappers = mock_auth
#     yield mock_client
#
#
# @pytest.fixture
# def mock_user_repository() -> Generator[MagicMock, None, None]:
#     """Fixture providing a mocked UserRepository"""
#     mock_repo = MagicMock()
#     yield mock_repo
#
#
# @pytest.fixture
# def sample_user() -> MagicMock:
#     """Fixture providing a sample User object"""
#     user = MagicMock()
#     user.id = "test-user-uuid-123"
#     user.email = "test@example.com"
#     user.created_at = datetime.now(UTC).isoformat()
#     user.username = "testuser"
#     return user
#
#
# @pytest.fixture
# def sample_auth_response(sample_user: MagicMock) -> MagicMock:
#     """Fixture providing a sample AuthResponse object"""
#     expires_at = int(datetime.now(UTC).timestamp()) + 3600
#
#     mock_session = MagicMock()
#     mock_session.access_token = "test-access-token"
#     mock_session.expires_at = expires_at
#
#     auth_response = MagicMock()
#     auth_response.user = sample_user
#     auth_response.session = mock_session
#
#     return auth_response
