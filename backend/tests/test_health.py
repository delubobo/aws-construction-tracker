import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# In-memory SQLite for tests — StaticPool keeps a single connection so all
# sessions see the same tables created by the fixture.
TEST_DB_URL = "sqlite://"
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_list_rfi():
    payload = {
        "title": "Clarify concrete mix design",
        "status": "Open",
        "priority": "High",
        "assigned_gc": "Turner Construction",
        "submitted_date": "2025-01-15",
        "due_date": "2025-02-01",
        "spec_section": "03 30 00",
    }
    create_r = client.post("/api/rfis", json=payload)
    assert create_r.status_code == 201
    data = create_r.json()
    assert data["rfi_number"] == "RFI-001"
    assert data["title"] == payload["title"]

    list_r = client.get("/api/rfis")
    assert list_r.status_code == 200
    assert len(list_r.json()) == 1


def test_dashboard_empty():
    r = client.get("/api/dashboard")
    assert r.status_code == 200
    d = r.json()
    assert d["total_rfis"] == 0
    assert d["pending_co_value"] == 0.0
    assert d["ofm_compliance_pct"] == 0.0
