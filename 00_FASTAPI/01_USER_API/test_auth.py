from fastapi.testclient import TestClient
from app import app
from random import randint

client = TestClient(app)


class TestAuth:
    def test_register(self):
        r = randint(0, 10000000)
        res = client.post(
            "api/v1/auth/register",
            json={
                "firstName": "Jonh",
                "password": "Password@15",
                "username": f"username{r}",
                "email": f"hello{r}@gmail.com",
                "lastName": "Doe",
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert data["jwt"] is not None
        assert data["error"] is None

    def test_login(self):
        res = client.post(
            "api/v1/auth/login",
            json={
                "usernameOrEmail": "crispengari@gmail.com",
                "password": "Password@15",
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert data["jwt"] is not None
        assert data["error"] is None
