from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()


class User(Base):
    """
    This model stores user info, including a unique API key, daily request counts, etc.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    api_key = Column(String(100), unique=True, index=True, nullable=False)
    request_count = Column(Integer, default=0, nullable=False)
    last_request_date = Column(Date, default=date.today(), nullable=False)


class URL(Base):
    """
    This model stores shortened URL references tied to a user.
    """
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_url = Column(String(2048), nullable=False)
    short_code = Column(String(50), unique=True, index=True, nullable=False)
    click_count = Column(Integer, default=0, nullable=False)

    user = relationship("User", backref="urls")
