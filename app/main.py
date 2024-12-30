from fastapi import FastAPI
from app.api.endpoints import url_endpoints
from app.db.database import init_db
from app.db.crud.crud_user import create_user
from app.core.config import settings
from app.core.logging_config import logger
from app.core.rate_limit_middleware import DailyRateLimitMiddleware


def create_default_user():
    """
    Create the default user from environment variables if not exists.
    """
    logger.info("Creating default user if not exists...")
    create_user(settings.API_DEFAULT_USER_NAME, settings.API_DEFAULT_USER_KEY)


def start_app():
    """
    This function initializes DB, creates default user, and returns FastAPI app instance.
    """
    logger.info("Initializing database...")
    init_db()

    logger.info("Creating default user...")
    create_default_user()

    app = FastAPI(title="URL Shortener", version="1.0.0")
    app.add_middleware(DailyRateLimitMiddleware)
    app.include_router(url_endpoints.router, tags=["URL Shortener"])

    return app


app = start_app()
