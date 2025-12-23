from fastapi import Depends, HTTPException, Security, Request
from fastapi.security import APIKeyHeader
import os

# Define where the API key comes from
api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)

# Load expected API key from environment
API_KEY = os.getenv("API_KEY")


async def verify_api_key(
    request: Request,
    api_key: str = Security(api_key_header)
):
    if API_KEY is None:
        raise HTTPException(
            status_code=500,
            detail="API key not configured on server"
        )

    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API key"
        )

    return True
