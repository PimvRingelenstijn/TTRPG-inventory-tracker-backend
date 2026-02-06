from pydantic import BaseModel
from uuid import UUID

class AuthUser(BaseModel):
    uuid: UUID
    name: str

class APIUserResponse(BaseModel):
    id: int
    uuid: UUID
    name: str