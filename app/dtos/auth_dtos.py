# Standard library imports
from datetime import datetime

# Third-party imports
from pydantic import BaseModel, EmailStr

from .user_dtos import UserDataResponse


# ======== Request DTOs ========
#    {?Type}{Purpose}Request
class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    username: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ======== Internal DTOs ========
#   {Context}Data/Info/Result

class LoginResult(BaseModel):
    access_token: str
    expires: datetime
    user_info: UserDataResponse


# ======== Response DTOs ========
#    {?Type}{Context}Response
