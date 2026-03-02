# Standard library imports
from datetime import datetime

# Third-party imports
from pydantic import BaseModel

# ======== Request DTOs ========
#    {Type}{Purpose}Request

# ======== Internal DTOs ========
#   {Context}Data/Info/Result

# ======== Response DTOs ========
#    {Type}{?Context}Response
class UserDataResponse(BaseModel):
    uuid: str
    email: str
    username: str
    created_at: datetime