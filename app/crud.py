from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .utils import url_encode
from . import models, schemas


def create_url(db: Session, url: schemas.URLCreate):
    short_key = url_encode(str(url.url))
    ttl = None
    if url.ttl and url.ttl > 0:
        ttl = datetime.utcnow() + timedelta(minutes=url.ttl)
    db_url = models.URL(
        origin_url=str(url.url),
        short_key=short_key,
        expires_at=ttl,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return short_key


def get_url_by_short_key(db: Session, short_key: str):
    db_url = db.get(models.URL, short_key)
    if db_url and db_url.is_expired():
        db.delete(db_url)
        db.commit()
        return None
    if db_url:
        db_url.click_cnt += 1
        db.commit()
    return db_url


def get_url_stats(db: Session, short_key: str):
    return db.get(models.URL, short_key)
