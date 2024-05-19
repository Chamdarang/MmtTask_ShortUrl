from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .utils import url_encode
from . import models, schemas


def create_url(db: Session, url: schemas.URLCreate) -> str:
    for _ in range(10):  # 최대 10번 재시도
        short_key = url_encode(str(url.url))
        ttl = None
        if url.ttl and url.ttl > 0:
            ttl = datetime.utcnow() + timedelta(minutes=url.ttl)
        db_url = models.URL(
            short_key=short_key,
            origin_url=str(url.url),
            expires_at=ttl,
        )
        try:
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            return short_key
        except IntegrityError:
            db.rollback()
            continue  # 재시도
    raise HTTPException(status_code=500, detail="Failed to generate unique short URL")

def get_url_by_short_key(db: Session, short_key: str) -> models.URL or None:
    db_url = db.get(models.URL, short_key)
    if db_url and db_url.is_expired():
        db.delete(db_url)
        db.commit()
        return None
    if db_url:
        db_url.click_cnt += 1
        db.commit()
    return db_url


def get_url_stats(db: Session, short_key: str) -> models.URL or None:
    return db.get(models.URL, short_key)
