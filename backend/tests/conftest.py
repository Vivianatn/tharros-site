import os
import tempfile

os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["MEDIA_DIR"] = tempfile.mkdtemp()
os.environ["ENVIRONMENT"] = "test"
os.environ["MIN_FORM_SECONDS"] = "0"
os.environ["ADMIN_EMAIL"] = "admin@tharros-studio.fr"
os.environ["ADMIN_PASSWORD"] = "tharros-admin"
os.environ["SECRET_KEY"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def auth(client):
    r = client.post("/api/auth/login", json={"email": "admin@tharros-studio.fr", "password": "tharros-admin"})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
