from pydantic import BaseModel

class APIGameSystem(BaseModel):
    name: str
    description: str

class APIGameSystemResponse(BaseModel):
    id: int
    name: str
    description: str

