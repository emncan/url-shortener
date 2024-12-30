from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse, JSONResponse
from app.db.schemas import URLCreate, URLResponse
from app.db.crud import crud_url
from app.services.utils import generate_short_code
from app.api.dependencies.auth import get_current_user
from app.core.logging_config import logger
from app.db.crud.crud_url import increment_click_count
from app.db.database import SessionLocal
from app.db.models import User
import redis
from app.core.config import settings

router = APIRouter()


# Redis client
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0)


@router.post("/shorten", response_model=URLResponse)
def shorten_url(payload: URLCreate, user: User = Depends(get_current_user)):
    """
    Shorten the given long URL for the authenticated user.
    """
    db_session = SessionLocal()
    try:
        existing_url = crud_url.get_by_original_url_and_user_id(
            db=db_session,
            original_url=payload.original_url,
            user_id=user.id
        )

        if existing_url:
            short_url = f"http://localhost:8000/{existing_url.short_code}"
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "URL already shortened for this user.",
                    "data": {
                        "short_url": short_url
                    }
                }
            )

        short_code = generate_short_code()

        new_url = crud_url.create_short_url(
            user_id=user.id,
            original_url=payload.original_url,
            short_code=short_code
        )

        redis_client.set(short_code, payload.original_url)

        short_url = f"http://localhost:8000/{short_code}"

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "URL shortened successfully.",
                "data": {
                    "short_url": short_url
                }
            }
        )

    except Exception as e:
        logger.error(f"Error in shorten_url endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Failed to shorten URL.",
                "data": None
            }
        )
    finally:
        db_session.close()


@router.get("/{short_code}")
def redirect_url(short_code: str):
    """
    Redirect to the original URL based on the short code provided.
    """
    cached_url = redis_client.get(short_code)
    if cached_url:
        logger.info("URL found in Redis cache.")
        url_obj = crud_url.get_url_by_short_code(short_code)
        if url_obj:
            increment_click_count(url_obj)
        return RedirectResponse(url=cached_url.decode("utf-8"))

    url_obj = crud_url.get_url_by_short_code(short_code)
    if not url_obj:
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": "URL not found.",
                "data": None
            }
        )

    redis_client.set(short_code, url_obj.original_url)

    increment_click_count(url_obj)

    return RedirectResponse(url=url_obj.original_url)
