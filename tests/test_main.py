from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
import pytest

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.meatadata.drop_all(bind=engine)


def test_create_short_url_with_ttl(test_db):
    res = client.post("/shorten", json={"url": "https://github.com/MementoAI/Backend_Assginment", "ttl": 1})
    assert res.status_code == 200
    data = res.json()
    assert "short_url" in data
    assert "expire_at" in data


def test_create_short_url_without_ttl(test_db):
    res = client.post("/shorten", json={"url": "https://github.com/MementoAI"})
    data = res.json()
    assert res.status_code == 200
    assert "short_url" in data
    assert data["expire_at"] is None


def test_redirect_url(test_db):
    res = client.post("/shorten", json={"url": "https://github.com/"})
    short_url = res.json()["short_url"]
    res = client.get("/" + short_url)
    assert res.status_code == 301
    assert res.url == "https://github.com/"


def test_get_url_stats(test_db):
    res = client.post("/shorten", json={"url": "https://git-scm.com/"})
    short_url = res.json()["short_url"]
    client.get("/" + short_url)
    client.get("/" + short_url)
    client.get("/" + short_url)

    res = client.get("/stats/" + short_url)
    data = res.json()
    assert res.status_code == 200
    assert data["click_count"] == 3
