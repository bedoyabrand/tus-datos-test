def test_register_and_login(client):
    # register
    res = client.post("/auth/register", json={
        "email": "admin@mail.com",
        "password": "secret123",
        "role": "admin"
    })
    assert res.status_code == 201, res.text
    data = res.json()
    assert data["email"] == "admin@mail.com"

    # login
    res = client.post(
        "/auth/login",
        data={"username": "admin@mail.com", "password": "secret123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == 200, res.text
    token = res.json()["access_token"]
    assert isinstance(token, str) and len(token) > 20
