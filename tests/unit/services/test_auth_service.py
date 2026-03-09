from datetime import datetime, UTC

import pytest
from fastapi import HTTPException

from app.dbmodels import DBUser
from app.dtos import RegistrationRequest, LoginRequest
from app.services import AuthService
from tests.helpers import exception_assert_helper


@pytest.fixture
def mock_supabase_client(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_user_repository(mocker):
    return mocker.Mock()

@pytest.fixture
def valid_auth_service(mock_supabase_client, mock_user_repository):
    return AuthService(
        supabase_client=mock_supabase_client,
        user_repository=mock_user_repository
    )

@pytest.fixture
def mock_auth_user(mocker):
    mock_auth_user = mocker.Mock()
    mock_auth_user.id = "test-user-uuid"
    mock_auth_user.email = "test@example.com"

    return mock_auth_user

@pytest.fixture
def mock_auth_response(mocker, mock_auth_user):
    mock_session = mocker.Mock()

    mock_auth_response = mocker.Mock()
    mock_auth_response.session = mock_session
    mock_auth_response.user = mock_auth_user

    return mock_auth_response

@pytest.fixture
def valid_db_user():
    return DBUser(
        uuid="test-user-uuid",
        username="test_username",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

@pytest.mark.unit
class TestRegisterUser:

    @pytest.fixture
    def sample_registration_data(self):
        """Valid RegistrationRequest test data"""
        return RegistrationRequest(
            email="test@email.com",
            password="test_password",
            username="test_username"
        )

    def test_successful_registration_returns_success_message(
            self,
            valid_auth_service,
            mock_supabase_client,
            mock_user_repository,
            sample_registration_data,
            mock_auth_response,
            mocker
    ):
        mock_supabase_client.auth.sign_up.return_value = mock_auth_response

        mock_mapper = mocker.patch("app.services.auth_service.map_to_new_db_user")
        mocker.patch("app.dbmodels.DBUser.to_dict", return_value={"key": "value"})

        result = valid_auth_service.register_user(sample_registration_data)

        assert result == {"Message": "User registered successfully!"}
        mock_supabase_client.auth.sign_up.assert_called_once_with({
            "email": "test@email.com",
            "password": "test_password"
        })
        mock_mapper.assert_called_once_with(sample_registration_data, mock_auth_response.user)
        mock_user_repository.create.assert_called_once()

    def test_registration_fails_when_supabase_raises_error(
            self,
            valid_auth_service,
            mock_supabase_client,
            sample_registration_data
    ):
        mock_supabase_client.auth.sign_up.side_effect = Exception("Email already exists")

        with pytest.raises(HTTPException) as exc_info:
            valid_auth_service.register_user(sample_registration_data)

        #exception_assert_helper(exc_info)

        assert exc_info.value.status_code == 400
        assert "Email already exists" in exc_info.value.detail

    def test_registration_fails_when_repository_create_fails(
            self,
            valid_auth_service,
            mock_supabase_client,
            mock_user_repository,
            sample_registration_data,
            mock_auth_response,
            mocker
    ):
        mock_supabase_client.auth.sign_up.return_value = mock_auth_response
        mocker.patch("app.services.auth_service.map_to_new_db_user")
        mocker.patch("app.dbmodels.DBUser.to_dict", return_value={"key": "value"})
        mock_user_repository.create.side_effect = Exception("Database connection failed")

        with pytest.raises(HTTPException) as exc_info:
            valid_auth_service.register_user(sample_registration_data)

        #exception_assert_helper(exc_info)

        assert exc_info.value.status_code == 400
        assert "Database connection failed" in exc_info.value.detail


class TestLoginUser:

    @pytest.fixture
    def sample_login_request(self):
        """Valid login data"""
        return LoginRequest(
            email="test@example.com",
            password="test_password"
        )

    def test_successful_login_returns_login_result(
            self,
            valid_auth_service,
            mock_supabase_client,
            mock_user_repository,
            sample_login_request,
            mock_auth_response,
            valid_db_user,
            mocker
    ):
        mock_supabase_client.auth.sign_in_with_password.return_value = mock_auth_response
        mock_user_repository.get_uuid.return_value = valid_db_user

        mock_user_data_response = mocker.Mock()
        mock_login_result = mocker.Mock()

        mock_user_mapper = mocker.patch("app.services.auth_service.map_to_user_data_response",
                     return_value=mock_user_data_response)
        mock_login_mapper = mocker.patch("app.services.auth_service.map_to_login_request",
                     return_value=mock_login_result)

        result = valid_auth_service.login_user(sample_login_request)

        assert result == mock_login_result
        mock_supabase_client.auth.sign_in_with_password.assert_called_once_with({
            "email": "test@example.com",
            "password": "test_password"
        })
        mock_user_repository.get_uuid.assert_called_once_with("test-user-uuid")
        mock_user_mapper.assert_called_once_with(mock_auth_response.user, valid_db_user)
        mock_login_mapper.assert_called_once_with(mock_auth_response.session, mock_user_data_response)

    def test_login_with_invalid_credentials_returns_401(
            self,
            valid_auth_service,
            mock_supabase_client,
            sample_login_request
    ):
        mock_supabase_client.auth.sign_in_with_password.side_effect = Exception("Invalid login credentials")

        with pytest.raises(HTTPException) as exc_info:
            valid_auth_service.login_user(sample_login_request)

        #exception_assert_helper(exc_info)

        assert exc_info.value.status_code == 401
        assert "Invalid credentials" in exc_info.value.detail

    def test_login_with_user_not_in_database_returns_401(
            self,
            valid_auth_service,
            mock_supabase_client,
            mock_user_repository,
            sample_login_request,
            mock_auth_response
    ):
        mock_supabase_client.auth.sign_in_with_password.return_value = mock_auth_response
        mock_user_repository.get_uuid.return_value = None  # User not in your DB

        with pytest.raises(HTTPException) as exc_info:
            valid_auth_service.login_user(sample_login_request)

        assert exc_info.value.status_code == 401
        assert "Invalid credentials" in exc_info.value.detail


class TestGetUserData:

    def test_get_user_data_returns_user_data_response(
            self,
            valid_auth_service,
            mock_user_repository,
            valid_db_user,
            mock_auth_user,
            mocker
    ):
        mock_user_repository.get_uuid.return_value = valid_db_user

        mock_user_data_response = mocker.Mock()
        mocker.patch("app.services.auth_service.map_to_user_data_response",
                     return_value=mock_user_data_response)

        result = valid_auth_service.get_user_data(mock_auth_user)

        assert result == mock_user_data_response
        mock_user_repository.get_uuid.assert_called_once_with("test-user-uuid")

    def test_get_user_data_user_not_found_raises_error(
            self,
            valid_auth_service,
            mock_user_repository,
            mock_auth_user
    ):
        mock_user_repository.get_uuid.return_value = None

        with pytest.raises(AttributeError) as exc_info:  # Or specific exception
            valid_auth_service.get_user_data(mock_auth_user)

        #exception_assert_helper(exc_info)

        error_msg = str(exc_info.value).lower()
        assert "nonetype" in error_msg