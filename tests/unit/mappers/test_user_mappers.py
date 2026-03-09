from datetime import datetime, UTC

import pytest

from app.mappers import map_to_new_db_user
from app.dtos import RegistrationRequest
from app.dbmodels import DBUser
from tests.helpers import exception_assert_helper

@pytest.mark.unit
class TestNewDBUserMapper:

    @pytest.fixture
    def sample_registration_data(self):
        """Valid RegistrationRequest test data"""
        return RegistrationRequest(
            email="test@email.com",
            password="test_password",
            username="test_username"
        )

    @pytest.fixture
    def base_date(self):
        return datetime(year=2000, month=1, day=1, tzinfo=UTC)

    @pytest.fixture
    def mock_auth_user(self, mocker, base_date):
        mock_auth_user = mocker.Mock
        mock_auth_user.id = "test-user-uuid"
        mock_auth_user.created_at = base_date

        return mock_auth_user

    def test_valid_input_returns_db_user(self, sample_registration_data, mock_auth_user):
        result = map_to_new_db_user(registration_data=sample_registration_data, auth_user=mock_auth_user)

        assert result.uuid == mock_auth_user.id
        assert result.username == sample_registration_data.username
        assert result.created_at == mock_auth_user.created_at
        assert isinstance(result, DBUser)

    def test_missing_registration_request_raises_attribute_error(self, mock_auth_user):
        with pytest.raises(AttributeError) as exc_info:
            map_to_new_db_user(registration_data=None, auth_user=mock_auth_user)

        #exception_assert_helper(exc_info)

        error_msg = str(exc_info.value).lower()
        assert 'username' in error_msg
        assert 'nonetype' in error_msg

    def test_missing_auth_user_raises_attribute_error(self, sample_registration_data):
        with pytest.raises(AttributeError) as exc_info:
            map_to_new_db_user(registration_data=sample_registration_data, auth_user=None)

        #exception_assert_helper(exc_info)

        error_msg = str(exc_info.value).lower()
        assert 'id' in error_msg
        assert 'nonetype' in error_msg

    # def test_missing_id_raises_validation_error(self, sample_registration_data, mock_auth_user):
    #     mock_auth_user.id = None
    #
    #     result = map_to_new_db_user(registration_data=sample_registration_data, auth_user=mock_auth_user)
    #     print(result.to_dict())
    #     #exception_assert_helper(exc_info)


    # def test_missing_username_raises_validation_error(self, sample_registration_data, mock_auth_user):
    #     sample_registration_data.username = None
    #
    #     result = map_to_new_db_user(registration_data=sample_registration_data, auth_user=mock_auth_user)
    #     print(result.to_dict())
    #     #exception_assert_helper(exc_info)

    # def test_missing_created_at_raises_validation_response(self, sample_registration_data, mock_auth_user):
    #     mock_auth_user.created_at = None
    #
    #     result = map_to_new_db_user(registration_data=sample_registration_data, auth_user=mock_auth_user)
    #     print(result.to_dict())
    #     #exception_assert_helper(exc_info)

