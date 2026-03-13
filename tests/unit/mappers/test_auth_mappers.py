from datetime import datetime, UTC

import pytest
from pydantic import ValidationError

from app.dbmodels import DBUser
from app.dtos import LoginResult, UserDataResponse
from app.mappers import map_to_login_request, map_to_user_data_response
from tests.helpers import exception_assert_helper


@pytest.mark.unit
class TestLoginRequestMapper:

    @pytest.fixture
    def sample_user_data(self):
        """Valid UserDataResponse test data"""
        return UserDataResponse(
            uuid="test-user-uuid",
            email="test@email.com",
            username="test_username",
            created_at=datetime(year=1990, month=1, day=1, tzinfo=UTC)
        )

    @pytest.fixture
    def base_date(self):
        return datetime(year=2000, month=1, day=1, tzinfo=UTC)

    @pytest.fixture
    def mock_auth_session(self, mocker, base_date):
        mock_session = mocker.Mock()
        mock_session.access_token = "test_access_token"
        mock_session.expires_at = base_date.timestamp()

        return mock_session

    def test_valid_input_returns_login_result(self, mock_auth_session, sample_user_data, base_date):
        result = map_to_login_request(auth_session=mock_auth_session, user_data_response=sample_user_data)

        assert result.access_token == "test_access_token"
        assert result.expires_at == base_date
        assert result.user_info == sample_user_data
        assert isinstance(result, LoginResult)

    def test_missing_access_token_raises_validation_error(self, mock_auth_session, sample_user_data):
        mock_auth_session.access_token = None

        with pytest.raises(ValidationError) as exc_info:
            map_to_login_request(auth_session=mock_auth_session, user_data_response=sample_user_data)

        #exception_assert_helper(exc_info)

        errors = exc_info.value.errors()
        assert any((
            e["loc"] == ("access_token",) and
            e["type"] == "string_type" and
            e["input"] is None
        ) for e in errors)

    def test_missing_expires_at_raises_type_error(self, mock_auth_session, sample_user_data):
        mock_auth_session.expires_at = None

        with pytest.raises(TypeError) as exc_info:
            map_to_login_request(auth_session=mock_auth_session, user_data_response=sample_user_data)

        #exception_assert_helper(exc_info)

        error_msg = str(exc_info.value).lower()
        assert "argument must be" in error_msg
        assert "nonetype" in error_msg or "none" in error_msg

    def test_missing_user_data_raises_validation_error(self, mock_auth_session):
        with pytest.raises(ValidationError) as exc_info:
            map_to_login_request(auth_session=mock_auth_session, user_data_response=None)

        #exception_assert_helper(exc_info)

        errors = exc_info.value.errors()
        assert any((
            e["loc"] == ("user_info",) and
            e["type"] == "model_type" and
            e["input"] is None
        ) for e in errors)

    def test_missing_auth_session_raises_attribute_error(self, sample_user_data):
        with pytest.raises(AttributeError) as exc_info:
            map_to_login_request(auth_session=None, user_data_response=sample_user_data)

        #exception_assert_helper(exc_info)

        error_msg = str(exc_info.value).lower()
        assert 'expires_at' in error_msg
        assert 'nonetype' in error_msg

    def test_expires_at_as_string_raises_type_error(self, mock_auth_session, sample_user_data):
        mock_auth_session.expires_at = "not-a-timestamp"

        with pytest.raises(TypeError) as exc_info:
            map_to_login_request(auth_session=mock_auth_session, user_data_response=sample_user_data)

        #exception_assert_helper(exc_info)

        error_msg = str(exc_info.value).lower()
        assert "argument must be" in error_msg
        assert "int or float" in error_msg

    def test_expires_at_negative_raises_os_error(self, mock_auth_session, sample_user_data):
        mock_auth_session.expires_at = -100000

        with pytest.raises(OSError) as exc_info:
            map_to_login_request(auth_session=mock_auth_session, user_data_response=sample_user_data)

        #exception_assert_helper(exc_info)

        error_msg = str(exc_info.value).lower()
        assert "invalid argument" in error_msg



@pytest.mark.unit
class TestUserDataResponseMapper:

    @pytest.fixture
    def mock_auth_user(self, mocker):
        mock_user = mocker.Mock()
        mock_user.id = "test-user-uuid"
        mock_user.email = "test@email.com"

        return mock_user

    @pytest.fixture
    def base_date(self):
        return datetime(year=1990, month=1, day=1, tzinfo=UTC)

    @pytest.fixture
    def sample_db_user(self, base_date):
        """Valid DBUser test data"""
        return DBUser(
            uuid="test-user-uuid",
            username="test_username",
            created_at=base_date,
            updated_at=datetime(year=2000, month=1, day=1, tzinfo=UTC)
        )

    def test_valid_input_returns_user_data_response(self, mock_auth_user, sample_db_user, base_date):
        result = map_to_user_data_response(auth_user=mock_auth_user, db_user_data=sample_db_user)

        assert result.uuid == mock_auth_user.id
        assert result.email == mock_auth_user.email
        assert result.username == sample_db_user.username
        assert result.created_at == sample_db_user.created_at
        assert isinstance(result, UserDataResponse)

    def test_missing_uuid_raises_validation_error(self, mock_auth_user, sample_db_user):
        mock_auth_user.id = None

        with pytest.raises(ValidationError) as exc_info:
            map_to_user_data_response(auth_user=mock_auth_user, db_user_data=sample_db_user)

        #exception_assert_helper(exc_info)

        errors = exc_info.value.errors()
        assert any((
            e["loc"] == ("uuid",) and
            e["type"] == "string_type" and
            e["input"] is None
        ) for e in errors)

    def test_missing_email_raises_validation_error(self, mock_auth_user, sample_db_user):
        mock_auth_user.email = None

        with pytest.raises(ValidationError) as exc_info:
            map_to_user_data_response(auth_user=mock_auth_user, db_user_data=sample_db_user)

        #exception_assert_helper(exc_info)

        errors = exc_info.value.errors()
        assert any((
            e["loc"] == ("email",) and
            e["type"] == "string_type" and
            e["input"] is None
        ) for e in errors)

    def test_missing_username_raises_validation_error(self, mock_auth_user, sample_db_user):
        sample_db_user.username = None

        with pytest.raises(ValidationError) as exc_info:
            map_to_user_data_response(auth_user=mock_auth_user, db_user_data=sample_db_user)

        #exception_assert_helper(exc_info)

        errors = exc_info.value.errors()
        assert any((
            e["loc"] == ("username",) and
            e["type"] == "string_type" and
            e["input"] is None
        ) for e in errors)

    def test_missing_created_at_raises_validation_error(self, mock_auth_user, sample_db_user):
        sample_db_user.created_at = None

        with pytest.raises(ValidationError) as exc_info:
            map_to_user_data_response(auth_user=mock_auth_user, db_user_data=sample_db_user)

        #exception_assert_helper(exc_info)

        errors = exc_info.value.errors()
        assert any((
            e["loc"] == ("created_at",) and
            e["type"] == "datetime_type" and
            e["input"] is None
        ) for e in errors)

    def test_missing_auth_user_raises_attribute_error(self, sample_db_user):
        with pytest.raises(AttributeError) as exc_info:
            map_to_user_data_response(None, sample_db_user)

        #exception_assert_helper(exc_info)

        error_msg = str(exc_info.value).lower()
        assert 'id' in error_msg
        assert 'nonetype' in error_msg

    def test_missing_db_user_raises_attribute_error(self, mock_auth_user):
        with pytest.raises(AttributeError) as exc_info:
            map_to_user_data_response(mock_auth_user, None)

        #exception_assert_helper(exc_info)

        error_msg = str(exc_info.value).lower()
        assert 'username' in error_msg
        assert 'nonetype' in error_msg