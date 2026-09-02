"""
Pruebas de /auth/login.
"""


def test_login_success(client, test_user):
    payload = {
        "username": test_user["user"].username,
        "password": test_user["plain_password"],
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["access_token"]  # no vacío
    assert body["token_type"] == "bearer"


def test_login_invalid_password(client, test_user):
    payload = {
        "username": test_user["user"].username,
        "password": "clave-incorrecta",
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 401
