import pytest

def test_register_and_login(client):
    # register
    r = client.post("/auth/register", json={"username": "admin", "password": "1234"})
    assert r.status_code in (200, 201)
    # login
    r = client.post("/auth/login", json={"username": "admin", "password": "1234"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data and data["token_type"] == "bearer"
