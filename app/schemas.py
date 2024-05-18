from datetime import datetime

from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional


class URLCreate(BaseModel):
    url: HttpUrl
    ttl: Optional[int] = None


class URL(BaseModel):
    origin_url: HttpUrl
    short_key: str
    expires_at: Optional[datetime] = None
    click_cnt: int

    model_config = ConfigDict(from_attributes=True)


class URLResponse(BaseModel):
    short_url: str


class URLStats(BaseModel):
    origin_url: HttpUrl
    short_key: str
    click_cnt: int
