from uuid import UUID
from pydantic import BaseModel


class APISystem(BaseModel):
    name: str
    description: str


class APISystemResponse(BaseModel):
    id: UUID
    name: str
    description: str
