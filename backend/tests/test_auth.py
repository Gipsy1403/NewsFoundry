def test_login_success(client):
    response = client.post("/login", json={
        "email": "test@test.com",
        "password": "test"
    })

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_fail(client):
    response = client.post("/login", json={
        "email": "wrong@test.com",
        "password": "wrong"
    })

    assert response.status_code == 401