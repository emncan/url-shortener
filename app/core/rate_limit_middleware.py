from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from datetime import datetime
from app.db.crud.crud_user import get_user_by_api_key, update_request_count
from app.core.config import settings
from app.core.logging_config import logger


class DailyRateLimitMiddleware(BaseHTTPMiddleware):
    """
    This middleware checks if the user has exceeded the daily request limit.
    It updates the user's request count per day.
    """

    async def dispatch(self, request: Request, call_next):
        # Allow docs, redoc and openapi.json without rate limit
        allowed_paths = [
            "/docs",
            "/openapi.json",
            "/redoc",
            "/docs/oauth2-redirect"]
        if any(request.url.path.startswith(path) for path in allowed_paths):
            return await call_next(request)

        api_key = request.headers.get("x-api-key")

        if not api_key:
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "API key is missing.",
                    "data": None
                },
                status_code=401
            )

        user = get_user_by_api_key(api_key)
        if not user:
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "Invalid API key.",
                    "data": None
                },
                status_code=401
            )

        current_date = datetime.now().date()
        if user.last_request_date != current_date:
            user.request_count = 0
            user.last_request_date = current_date

        if user.request_count >= settings.RATE_LIMIT_REQUESTS:
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "Daily request limit exceeded.",
                    "data": None
                },
                status_code=429
            )

        user.request_count += 1
        update_request_count(user)

        response = await call_next(request)
        return response
