from pydantic import BaseModel

class AuthUser(BaseModel):
    uuid: str
    username: str

class APIUserResponse(BaseModel):
    uuid: str
    username: str