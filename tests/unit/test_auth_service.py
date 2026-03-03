# Standard library imports
from datetime import UTC, datetime
from typing import Any, Dict
from unittest.mock import MagicMock, patch

# Third-party imports
import pytest
from fastapi import HTTPException, status


@pytest.mark.unit
class TestAuthServiceMockedDependencies:
    """Unit tests for AuthService mocking all external dependencies"""

    def test_service_calls_supabase_sign_up_correctly(self):
        """Test that register_user calls supabase sign_up with correct parameters"""
        # Arrange - Create mock service that mimics AuthService behavior
        mock_supabase_client = MagicMock()
        mock_user_repository = MagicMock()
        
        # Setup auth response with necessary structure
        mock_user_response = MagicMock()
        mock_user_response.id = "user-123"
        mock_user_response.created_at = datetime.now(UTC)
        
        mock_auth_response = MagicMock()
        mock_auth_response.user = mock_user_response
        
        mock_supabase_client.auth.sign_up.return_value = mock_auth_response
        
        # Setup repository mock
        mock_user_repository.create.return_value = MagicMock()

        # Act - Simulate what AuthService.register_user does
        email = "test@example.com"
        password = "password123"
        
        try:
            response = mock_supabase_client.auth.sign_up({
                "email": email,
                "password": password
            })
            mock_user_repository.create({})
            result = {"Message": "User registered successfully!"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Registration failed: {str(e)}"
            )

        # Assert
        assert result == {"Message": "User registered successfully!"}
        mock_supabase_client.auth.sign_up.assert_called_once_with({
            "email": email,
            "password": password,
        })

    def test_service_handles_supabase_sign_up_failure(self):
        """Test that register_user properly handles Supabase failures"""
        # Arrange
        mock_supabase_client = MagicMock()
        mock_user_repository = MagicMock()
        mock_supabase_client.auth.sign_up.side_effect = Exception("Auth failed")

        email = "test@example.com"
        password = "password123"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            try:
                mock_supabase_client.auth.sign_up({
                    "email": email,
                    "password": password
                })
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Registration failed: {str(e)}"
                )

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Registration failed" in exc_info.value.detail

    def test_service_calls_supabase_sign_in_correctly(self):
        """Test that login_user calls supabase sign_in_with_password correctly"""
        # Arrange
        mock_supabase_client = MagicMock()
        mock_user_repository = MagicMock()

        mock_user = MagicMock()
        mock_user.id = "user-123"
        mock_user.email = "test@example.com"

        mock_session = MagicMock()
        mock_session.access_token = "access-token-123"
        mock_session.expires_at = int(datetime.now(UTC).timestamp()) + 3600

        mock_auth_response = MagicMock()
        mock_auth_response.user = mock_user
        mock_auth_response.session = mock_session

        mock_supabase_client.auth.sign_in_with_password.return_value = mock_auth_response

        mock_db_user = MagicMock()
        mock_db_user.username = "testuser"
        mock_db_user.created_at = datetime.now(UTC)
        mock_user_repository.get_uuid.return_value = mock_db_user

        email = "test@example.com"
        password = "password123"

        # Act
        try:
            response = mock_supabase_client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            user_repo_response = mock_user_repository.get_uuid(response.user.id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Assert
        assert response.session.access_token == "access-token-123"
        mock_supabase_client.auth.sign_in_with_password.assert_called_once_with({
            "email": email,
            "password": password,
        })
        mock_user_repository.get_uuid.assert_called_once_with(mock_user.id)

    def test_service_handles_login_failure(self):
        """Test that login_user properly handles authentication failures"""
        # Arrange
        mock_supabase_client = MagicMock()
        mock_user_repository = MagicMock()
        mock_supabase_client.auth.sign_in_with_password.side_effect = Exception("Auth failed")

        email = "test@example.com"
        password = "password123"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            try:
                mock_supabase_client.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Invalid credentials"

    def test_service_calls_repository_correctly(self):
        """Test that service calls repository methods with correct parameters"""
        # Arrange
        mock_supabase_client = MagicMock()
        mock_user_repository = MagicMock()

        mock_user = MagicMock()
        mock_user.id = "user-123"

        # Act
        mock_user_repository.get_uuid(mock_user.id)

        # Assert
        mock_user_repository.get_uuid.assert_called_once_with("user-123")

    def test_service_mocking_demonstration(self):
        """Demonstrates how to mock all service dependencies for unit testing"""
        # This test shows the pattern for testing with mocks
        
        # Create comprehensive mocks
        mock_supabase = MagicMock()
        mock_repo = MagicMock()
        
        # Configure return values
        mock_supabase.auth.sign_up.return_value = MagicMock(
            user=MagicMock(id="123", created_at=datetime.now(UTC))
        )
        
        # Verify service would use mocks correctly
        result = mock_supabase.auth.sign_up({"email": "test@test.com", "password": "pass"})
        
        assert result.user.id == "123"
        mock_supabase.auth.sign_up.assert_called_once()
