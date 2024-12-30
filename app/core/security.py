from fastapi import HTTPException, status
from app.db.crud.crud_user import get_user_by_api_key


def validate_api_key(api_key: str):
    """
    Validate if the provided API key belongs to an existing user.
    """
    user = get_user_by_api_key(api_key=api_key)
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
