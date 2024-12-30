from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import User
from datetime import date
from app.core.logging_config import logger


def get_user_by_api_key(api_key: str) -> User:
    """Return the user object with given api_key."""
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.api_key == api_key).first()
    except Exception as e:
        logger.error(f"Error fetching user by api_key: {e}")
        db.rollback()
    finally:
        db.close()


def create_user(username: str, api_key: str):
    """Create a new user if not exists."""
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            user = User(
                username=username,
                api_key=api_key,
                request_count=0,
                last_request_date=date.today()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        db.rollback()
    finally:
        db.close()


def update_request_count(user: User):
    """Update user request count in DB."""
    db: Session = SessionLocal()
    try:
        db_user = db.query(User).filter(User.id == user.id).first()
        if db_user:
            db_user.request_count = user.request_count
            db_user.last_request_date = user.last_request_date
            db.commit()
    except Exception as e:
        logger.error(f"Error updating request count: {e}")
        db.rollback()
    finally:
        db.close()
