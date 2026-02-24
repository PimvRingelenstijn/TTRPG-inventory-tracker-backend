from pydantic import BaseModel

# ======== Request DTOs ========
#    {Type}{Purpose}Request

# ======== Internal DTOs ========
#   {Context}Data/Info/Result

# ======== Response DTOs ========
#    {Type}{?Context}Response
class APIGameSystem(BaseModel):
    name: str
    description: str

class APIGameSystemResponse(BaseModel):
    id: int
    name: str
    description: str

