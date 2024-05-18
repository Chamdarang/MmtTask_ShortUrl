from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shorten")
def create_short_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    short_url = crud.create_url(db, url)
    return {"short_url": short_url}


@app.get("/{short_key}")
def redirect_url(short_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_short_key(db, short_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="Invalid URL")
    return RedirectResponse(db_url.origin_url, status_code=301)


@app.get("/stats/{short_key}")
def get_stats(short_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_stats(db, short_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="Invalid URL")
    return {
        "origin_url": db_url.origin_url,
        "short_key": db_url.short_key,
        "click_cnt": db_url.click_cnt
    }