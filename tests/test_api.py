import pytest

from sqli_lab import create_app
from sqli_lab.models import Challenge, User, db
from sqli_lab.auth_utils import hash_password


@pytest.fixture
def client():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "LAB_DB_PATH": ":memory:",
            "SECRET_KEY": "test-secret",
        }
    )
    with app.app_context():
        db.create_all()
        db.session.add(
            User(username="tester", password_hash=hash_password("password"))
        )
        db.session.add(
            Challenge(
                slug="test-ch",
                title="Test",
                sqli_type="error-based",
                difficulty="easy",
                points=50,
                flag="FLAG{test}",
                hints="[]",
                description="Test challenge",
                practice=False,
                order_index=1,
            )
        )
        db.session.commit()
    return app.test_client()


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["ok"] is True


def test_submit_requires_login(client):
    res = client.post("/api/challenges/test-ch/submit", json={"flag": "FLAG{test}"})
    assert res.status_code == 302 or res.status_code == 401
