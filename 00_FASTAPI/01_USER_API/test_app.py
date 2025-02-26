from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


class TestApp:
    def test_default(self):
        res = client.get("/")
        assert res.status_code == 200
        assert res.json() == {"message": "This is a users API", "totalUsers": 0}
