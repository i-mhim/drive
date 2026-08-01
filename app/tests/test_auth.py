from jose import jwt
from app.config import settings


def test_register_user(client):
    res = client.post(
        "/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "password123"
        }
    )

    assert res.status_code == 201

    body = res.json()

    assert body["email"] == "newuser@test.com"
    assert "id" in body

def test_login_success(client, test_user):
    res = client.post(
        "/auth/login",
        data={
            "username": test_user["user"].email,
            "password": test_user["password"]
        }
    )

    assert res.status_code == 200

    body = res.json()

    assert body["token_type"] == "Bearer"
    assert "access_token" in body

def test_login_token_contains_user_id(client, test_user):
    res = client.post(
        "/auth/login",
        data={
            "username": test_user["user"].email,
            "password": test_user["password"]
        }
    )

    token = res.json()["access_token"]

    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm]
    )

    assert payload["user_id"] == test_user["user"].id

def test_login_wrong_password(client, test_user):
    res = client.post(
        "/auth/login",
        data={
    "username": test_user["user"].email,
    "password": "wrongpassword"
    }
    )

    assert res.status_code == 403
    assert res.json()["detail"] == "Invalid Credentials"

def test_login_wrong_email(client, test_user):
    res = client.post(
        "/auth/login",
        data={
            "username": "idontexist@test.com",
            "password": test_user["password"]
}
        
    )

    assert res.status_code == 403
    assert res.json()["detail"] == "Invalid Credentials"

def test_login_empty_password(client, test_user):
    res = client.post(
        "/auth/login",
        data={
            "username": test_user["user"].email,
            "password": ""
        }
    )

    assert res.status_code == 422


def test_login_empty_username(client):
    res = client.post(
        "/auth/login",
        data={
            "username": "",
            "password": "password123"
        }
    )

    assert res.status_code == 422