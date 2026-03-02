# Third-party imports
from pydantic import BaseModel


# ======== Request DTOs ========
#    {Type}{Purpose}Request
class GameSystemCreateRequest(BaseModel):
    name: str
    description: str

# ======== Internal DTOs ========
#   {Context}Data/Info/Result

# ======== Response DTOs ========
#    {Type}{?Context}Response
class GameSystemDataResponse(BaseModel):
    id: int
    name: str
    description: str

