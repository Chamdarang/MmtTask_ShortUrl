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
    Base.metadata.drop_all(bind=engine)


def test_create_short_url_with_ttl(test_db):
    res = client.post("/shorten", json={"url": "https://github.com/MementoAI/Backend_Assginment", "ttl": 1})
    assert res.status_code == 200
    data = res.json()
    assert "short_url" in data


def test_create_short_url_without_ttl(test_db):
    res = client.post("/shorten", json={"url": "https://github.com/MementoAI"})
    data = res.json()
    assert res.status_code == 200
    assert "short_url" in data


def test_redirect_url(test_db):
    res = client.post("/shorten", json={"url": "https://github.com/"})
    short_key = res.json()["short_url"].split("/")[-1]
    res = client.get(short_key)
    assert res.url == "https://github.com/"
    assert res.status_code == 301

def test_get_url_stats(test_db):
    res = client.post("/shorten", json={"url": "https://git-scm.com/"})
    short_key = res.json()["short_url"].split("/")[-1]
    client.get(short_key)
    client.get(short_key)
    client.get(short_key)

    res = client.get("/stats/" + short_key)
    assert res.status_code == 200
    data = res.json()
    assert data["click_cnt"] == 3
