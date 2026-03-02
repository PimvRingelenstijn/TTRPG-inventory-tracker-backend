# Standard library imports
from datetime import datetime

# Third-party imports
from fastapi import Response


def set_cookies(access_token: str,
                expires: datetime,
                response: Response):
    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        expires=expires,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )