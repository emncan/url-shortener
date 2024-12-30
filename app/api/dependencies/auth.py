from fastapi import Header, HTTPException, status, Security
from app.db.crud.crud_user import get_user_by_api_key
from fastapi.security.api_key import APIKeyHeader

api_key_header = APIKeyHeader(name="x-api-key")


def get_current_user(api_key: str = Security(api_key_header)):
    """
    This dependency verifies the API key from request header.
    """

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "message": "API key is missing.",
                "data": None,
            }
        )

    user = get_user_by_api_key(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "message": "Invalid API key.",
                "data": None,
            }
        )
    return user
