from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginUserInfo(BaseModel):
    uuid: str
    email: str
    username: str
    created_at: datetime

class LoginResponse(BaseModel):
    access_token: str
    expires: datetime
    userinfo: LoginUserInfo

