from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import URL
from app.core.logging_config import logger


def get_by_original_url_and_user_id(
        db: Session,
        original_url: str,
        user_id: int):
    """ Get URL by original URL and user ID """

    return db.query(URL).filter(
        URL.original_url == original_url,
        URL.user_id == user_id
    ).first()


def create_short_url(user_id: int, original_url: str, short_code: str) -> URL:
    """
    Create a short URL record in the database.
    """
    db: Session = SessionLocal()
    try:
        new_url = URL(
            user_id=user_id,
            original_url=original_url,
            short_code=short_code
        )
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return new_url
    except Exception as e:
        logger.error(f"Error creating short URL: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_url_by_short_code(short_code: str) -> URL:
    """
    Fetch the URL object by short_code.
    """
    db: Session = SessionLocal()
    try:
        return db.query(URL).filter(URL.short_code == short_code).first()
    except Exception as e:
        logger.error(f"Error fetching short URL by code: {e}")
        db.rollback()
    finally:
        db.close()


def increment_click_count(url: URL):
    """
    Increment the click count of the given URL.
    """
    db: Session = SessionLocal()
    try:
        db_url = db.query(URL).filter(URL.id == url.id).first()
        if db_url:
            db_url.click_count += 1
            db.commit()
    except Exception as e:
        logger.error(f"Error incrementing click count: {e}")
        db.rollback()
    finally:
        db.close()
