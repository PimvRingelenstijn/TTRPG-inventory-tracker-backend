from pydantic import BaseModel

class APISystem(BaseModel):
    name: str
    description: str

class APISystemResponse(BaseModel):
    id: int
    name: str
    description: str
