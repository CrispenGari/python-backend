from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


class TestApp:
    def test_hello(self):
        res = client.get("/hello/jon")
        assert res.json() == {"message": "Hello jon."}

    def test_hi(self):
        res = client.get("/")
        assert res.json() == {"message": "hi"}

    def test_bye(self):
        res = client.get("/bye")
        assert res.json() == {"message": "bye"}
