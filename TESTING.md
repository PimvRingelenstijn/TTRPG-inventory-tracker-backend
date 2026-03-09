# Unit Testing Guide

This document explains how unit testing is set up in this project, how to write tests following the **AAA (Arrange-Act-Assert)** principle, and how to effectively use mocks.

---

## Table of Contents

1. [Testing Framework Stack](#testing-framework-stack)
2. [Project Structure](#project-structure)
3. [How Tests Are Set Up](#how-tests-are-set-up)
4. [The AAA Principle](#the-aaa-principle)
5. [Working with Mocks](#working-with-mocks)
6. [Verifying Mock Calls](#verifying-mock-calls)
7. [Complete Test Examples](#complete-test-examples)
8. [Running Tests](#running-tests)
9. [Writing Your Own Tests](#writing-your-own-tests)

---

## Testing Framework Stack

| Package | Purpose |
|---------|---------|
| `pytest` | Testing framework |
| `pytest-asyncio` | Async/await test support |
| `pytest-mock` | Mocking utilities |
| `httpx` | HTTP client for API testing |
| `faker` | Test data generation |

---

## Project Structure

```
tests/
├── __init__.py              # Makes tests a Python package
├── conftest.py              # Shared fixtures (mocks, test data)
└── unit/
    ├── __init__.py          # Makes unit a Python package
    └── test_auth_service.py # Unit tests for AuthService
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `pytest.ini` | Pytest configuration (test discovery, markers, async mode) |
| `tests/conftest.py` | Shared fixtures available to all tests automatically |
| `tests/unit/*.py` | Unit tests that test individual components in isolation |

---

## How Tests Are Set Up

### 1. Environment Configuration (`conftest.py`)

Before any tests run, we set dummy environment variables to prevent database connection errors:

```python
import os

os.environ.setdefault("USER", "test_user")
os.environ.setdefault("PASSWORD", "test_password")
os.environ.setdefault("HOST", "localhost")
os.environ.setdefault("PORT", "5432")
os.environ.setdefault("DBNAME", "test_db")
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_KEY", "test-service-key")
```

### 2. Fixtures (`conftest.py`)

Fixtures are reusable test components that pytest automatically injects into tests:

```python
@pytest.fixture
def mock_supabase_client():
    """Provides a mocked Supabase client"""
    mock_client = MagicMock()
    mock_client.auth = MagicMock()
    yield mock_client

@pytest.fixture
def mock_user_repository():
    """Provides a mocked UserRepository"""
    yield MagicMock()

@pytest.fixture
def sample_user():
    """Provides a sample User object"""
    user = MagicMock()
    user.id = "test-user-uuid-123"
    user.email = "test@example.com"
    user.username = "testuser"
    return user
```

### 3. Test Classes and Markers

Tests are organized in classes and marked for categorization:

```python
@pytest.mark.unit  # Mark as unit test
class TestAuthService:
    """Unit tests for AuthService"""
    
    def test_something(self):
        pass
```

---

## The AAA Principle

Every test should follow the **Arrange-Act-Assert** pattern:

```
┌─────────────────────────────────────────────────────────────┐
│  ARRANGE  │  Set up test data, create mocks, configure     │
│           │  return values and expected behaviors          │
├───────────┼─────────────────────────────────────────────────┤
│    ACT    │  Execute the code/method being tested          │
│           │  (usually a single action)                     │
├───────────┼─────────────────────────────────────────────────┤
│  ASSERT   │  Verify the results are correct                │
│           │  Verify mocks were called correctly            │
└───────────┴─────────────────────────────────────────────────┘
```

### AAA Example

```python
def test_login_user_success(self):
    """Test successful user login"""
    
    # ═══════════════════════════════════════════════════════
    # ARRANGE - Set up all test prerequisites
    # ═══════════════════════════════════════════════════════
    
    # Create mocks for dependencies
    mock_supabase_client = MagicMock()
    mock_user_repository = MagicMock()
    
    # Configure mock return values
    mock_user = MagicMock()
    mock_user.id = "user-123"
    mock_user.email = "test@example.com"
    
    mock_session = MagicMock()
    mock_session.access_token = "access-token-123"
    
    mock_auth_response = MagicMock()
    mock_auth_response.user = mock_user
    mock_auth_response.session = mock_session
    
    # Tell the mock what to return when called
    mock_supabase_client.auth.sign_in_with_password.return_value = mock_auth_response
    
    mock_db_user = MagicMock()
    mock_db_user.username = "testuser"
    mock_user_repository.get_uuid.return_value = mock_db_user
    
    # Test input data
    email = "test@example.com"
    password = "password123"
    
    # ═══════════════════════════════════════════════════════
    # ACT - Execute the code being tested
    # ═══════════════════════════════════════════════════════
    
    response = mock_supabase_client.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
    db_user = mock_user_repository.get_uuid(response.user.id)
    
    # ═══════════════════════════════════════════════════════
    # ASSERT - Verify results and mock interactions
    # ═══════════════════════════════════════════════════════
    
    # Verify return values
    assert response.session.access_token == "access-token-123"
    assert response.user.email == "test@example.com"
    
    # Verify mocks were called correctly
    mock_supabase_client.auth.sign_in_with_password.assert_called_once_with({
        "email": email,
        "password": password,
    })
    mock_user_repository.get_uuid.assert_called_once_with("user-123")
```

---

## Working with Mocks

### What is a Mock?

A **mock** is a fake object that simulates the behavior of real objects. We use mocks to:
- Isolate the code being tested
- Avoid calling real external services (Supabase, database)
- Control what dependencies return
- Verify how dependencies are used

### Creating Mocks

```python
from unittest.mock import MagicMock

# Create a basic mock
mock_object = MagicMock()

# Mock automatically creates attributes when accessed
mock_object.some_attribute        # Works!
mock_object.nested.deep.attribute # Works!
mock_object.method()              # Works!
```

### Configuring Mock Return Values

```python
# Simple return value
mock_repo.get_user.return_value = {"id": "123", "name": "Test"}

# Return value with nested attributes
mock_response = MagicMock()
mock_response.user.id = "user-123"
mock_response.user.email = "test@example.com"
mock_response.session.access_token = "token-abc"

mock_client.auth.sign_up.return_value = mock_response

# Chained mock creation (shorthand)
mock_client.auth.sign_up.return_value = MagicMock(
    user=MagicMock(id="123", email="test@example.com"),
    session=MagicMock(access_token="token-abc")
)
```

### Configuring Mock Exceptions

```python
# Make a mock raise an exception when called
mock_client.auth.sign_up.side_effect = Exception("Auth failed")

# Now when called, it will raise:
# mock_client.mappers.sign_up(...)  -> raises Exception("Auth failed")
```

---

## Verifying Mock Calls

After the **Act** phase, you should verify that mocks were called correctly in the **Assert** phase.

### Basic Verification Methods

```python
# ┌────────────────────────────────────────────────────────────────┐
# │ VERIFICATION METHOD              │ WHAT IT CHECKS              │
# ├──────────────────────────────────┼─────────────────────────────┤
# │ assert_called()                  │ Was called at least once    │
# │ assert_called_once()             │ Was called exactly once     │
# │ assert_called_with(args)         │ Last call had these args    │
# │ assert_called_once_with(args)    │ Called once with these args │
# │ assert_not_called()              │ Was never called            │
# │ assert_any_call(args)            │ Any call had these args     │
# └──────────────────────────────────┴─────────────────────────────┘
```

### Verification Examples

```python
# Verify method was called exactly once with specific arguments
mock_supabase_client.auth.sign_up.assert_called_once_with({
    "email": "test@example.com",
    "password": "password123"
})

# Verify method was called (at least once)
mock_user_repository.create.assert_called()

# Verify method was NEVER called (useful for error paths)
mock_user_repository.create.assert_not_called()

# Check how many times a method was called
assert mock_repo.get_user.call_count == 2

# Get the arguments from the last call
args, kwargs = mock_repo.get_user.call_args
assert args[0] == "user-123"

# Get all calls made to a mock
all_calls = mock_repo.get_user.call_args_list
```

### Verifying Call Order

```python
from unittest.mock import call

# Verify multiple calls in order
mock_repo.assert_has_calls([
    call.get_user("user-1"),
    call.get_user("user-2"),
    call.update_user("user-1", {"name": "New Name"})
])
```

---

## Complete Test Examples

### Example 1: Testing Success Path

```python
def test_register_user_success(self):
    """Test successful user registration"""
    
    # ═══════════════════════════════════════════════════════
    # ARRANGE
    # ═══════════════════════════════════════════════════════
    
    # Create mocks
    mock_supabase_client = MagicMock()
    mock_user_repository = MagicMock()
    
    # Configure Supabase mock response
    mock_user_response = MagicMock()
    mock_user_response.id = "user-123"
    mock_user_response.created_at = datetime.now(UTC)
    
    mock_auth_response = MagicMock()
    mock_auth_response.user = mock_user_response
    
    mock_supabase_client.auth.sign_up.return_value = mock_auth_response
    mock_user_repository.create.return_value = MagicMock()
    
    # Test data
    email = "test@example.com"
    password = "password123"
    
    # ═══════════════════════════════════════════════════════
    # ACT
    # ═══════════════════════════════════════════════════════
    
    response = mock_supabase_client.auth.sign_up({
        "email": email,
        "password": password
    })
    mock_user_repository.create({})
    result = {"Message": "User registered successfully!"}
    
    # ═══════════════════════════════════════════════════════
    # ASSERT
    # ═══════════════════════════════════════════════════════
    
    # Verify result
    assert result == {"Message": "User registered successfully!"}
    
    # Verify Supabase was called correctly
    mock_supabase_client.auth.sign_up.assert_called_once_with({
        "email": email,
        "password": password,
    })
    
    # Verify repository was called
    mock_user_repository.create.assert_called_once()
```

### Example 2: Testing Error Path

```python
def test_register_user_supabase_failure(self):
    """Test user registration when Supabase fails"""
    
    # ═══════════════════════════════════════════════════════
    # ARRANGE
    # ═══════════════════════════════════════════════════════
    
    mock_supabase_client = MagicMock()
    mock_user_repository = MagicMock()
    
    # Configure mock to raise an exception
    mock_supabase_client.auth.sign_up.side_effect = Exception("Auth failed")
    
    email = "test@example.com"
    password = "password123"
    
    # ═══════════════════════════════════════════════════════
    # ACT & ASSERT (combined for exception testing)
    # ═══════════════════════════════════════════════════════
    
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
    
    # Verify exception details
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Registration failed" in exc_info.value.detail
    
    # Verify repository was NEVER called (important!)
    mock_user_repository.create.assert_not_called()
```

### Example 3: Using Fixtures

```python
def test_with_fixtures(
    self,
    mock_supabase_client,    # Injected from conftest.py
    mock_user_repository,    # Injected from conftest.py
    sample_user,             # Injected from conftest.py
    sample_auth_response     # Injected from conftest.py
):
    """Test using pytest fixtures"""
    
    # ═══════════════════════════════════════════════════════
    # ARRANGE - Fixtures are already set up!
    # ═══════════════════════════════════════════════════════
    
    mock_supabase_client.auth.sign_up.return_value = sample_auth_response
    
    # ═══════════════════════════════════════════════════════
    # ACT
    # ═══════════════════════════════════════════════════════
    
    response = mock_supabase_client.auth.sign_up({
        "email": sample_user.email,
        "password": "password123"
    })
    
    # ═══════════════════════════════════════════════════════
    # ASSERT
    # ═══════════════════════════════════════════════════════
    
    assert response.user.id == sample_user.id
    mock_supabase_client.auth.sign_up.assert_called_once()
```

---

## Running Tests

### Run All Tests
```bash
python3 -m pytest tests/ -v
```

### Run Only Unit Tests
```bash
python3 -m pytest tests/unit/ -v
```

### Run Specific Test File
```bash
python3 -m pytest tests/unit/test_auth_service.py -v
```

### Run Specific Test Class
```bash
python3 -m pytest tests/unit/test_auth_service.py::TestAuthServiceMockedDependencies -v
```

### Run Specific Test Method
```bash
python3 -m pytest tests/unit/test_auth_service.py::TestAuthServiceMockedDependencies::test_service_calls_supabase_sign_up_correctly -v
```

### Run Tests by Marker
```bash
python3 -m pytest -m unit -v      # Only unit tests
python3 -m pytest -m integration  # Only integration tests
```

### Run with Coverage Report
```bash
python3 -m pytest tests/ --cov=app --cov-report=html
```

---

## Writing Your Own Tests

### Step-by-Step Guide

#### 1. Create a new test file

```bash
# Create tests/unit/test_game_system_service.py
```

#### 2. Add imports and test class

```python
from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status


@pytest.mark.unit
class TestGameSystemService:
    """Unit tests for GameSystemService"""
    pass
```

#### 3. Write your first test following AAA

```python
def test_get_all_game_systems_success(self):
    """Test retrieving all game systems"""
    
    # ═══════════════════════════════════════════════════════
    # ARRANGE
    # ═══════════════════════════════════════════════════════
    
    mock_repository = MagicMock()
    
    # Configure what the repository should return
    mock_repository.get_all.return_value = [
        MagicMock(id=1, name="D&D 5e"),
        MagicMock(id=2, name="Pathfinder"),
    ]
    
    # ═══════════════════════════════════════════════════════
    # ACT
    # ═══════════════════════════════════════════════════════
    
    result = mock_repository.get_all()
    
    # ═══════════════════════════════════════════════════════
    # ASSERT
    # ═══════════════════════════════════════════════════════
    
    assert len(result) == 2
    assert result[0].name == "D&D 5e"
    mock_repository.get_all.assert_called_once()
```

#### 4. Add error case tests

```python
def test_get_game_system_not_found(self):
    """Test error when game system doesn't exist"""
    
    # ARRANGE
    mock_repository = MagicMock()
    mock_repository.get_by_id.return_value = None
    
    # ACT & ASSERT
    result = mock_repository.get_by_id(999)
    
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
```

### Test Naming Convention

```
test_<method_name>_<scenario>_<expected_result>

Examples:
- test_register_user_success
- test_register_user_invalid_email_raises_error
- test_login_user_wrong_password_returns_401
- test_get_user_not_found_returns_none
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│                    MOCK CHEAT SHEET                             │
├─────────────────────────────────────────────────────────────────┤
│ CREATE MOCK                                                     │
│   mock = MagicMock()                                            │
│                                                                 │
│ SET RETURN VALUE                                                │
│   mock.method.return_value = "value"                            │
│                                                                 │
│ SET EXCEPTION                                                   │
│   mock.method.side_effect = Exception("error")                  │
│                                                                 │
│ VERIFY CALLED                                                   │
│   mock.method.assert_called()                                   │
│   mock.method.assert_called_once()                              │
│   mock.method.assert_called_with(arg1, arg2)                    │
│   mock.method.assert_called_once_with(arg1, arg2)               │
│   mock.method.assert_not_called()                               │
│                                                                 │
│ CHECK CALL COUNT                                                │
│   assert mock.method.call_count == 2                            │
│                                                                 │
│ GET CALL ARGUMENTS                                              │
│   args, kwargs = mock.method.call_args                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    AAA TEMPLATE                                 │
├─────────────────────────────────────────────────────────────────┤
│ def test_something(self):                                       │
│     # ARRANGE                                                   │
│     mock = MagicMock()                                          │
│     mock.method.return_value = expected_value                   │
│                                                                 │
│     # ACT                                                       │
│     result = mock.method(input_data)                            │
│                                                                 │
│     # ASSERT                                                    │
│     assert result == expected_value                             │
│     mock.method.assert_called_once_with(input_data)             │
└─────────────────────────────────────────────────────────────────┘
```
