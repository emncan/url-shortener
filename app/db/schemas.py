from pydantic import BaseModel, HttpUrl
from typing import Optional


class URLCreate(BaseModel):
    """
    This schema is for creating a new shortened URL request.
    """
    original_url: HttpUrl


class URLResponse(BaseModel):
    """
    Response schema for the shortened URL.
    """
    short_url: str


class URLInfo(BaseModel):
    """
    Additional info schema for debug or analytics.
    """
    original_url: HttpUrl
    short_url: str
    click_count: int


class UserBase(BaseModel):
    """
    Base user schema.
    """
    username: str
    api_key: str
    request_count: int
