def make_user_and_token(client, email, role="organizer"):
    client.post("/auth/register", json={"email": email, "password": "secret123", "role": role})
    r = client.post("/auth/login", data={"username": email, "password": "secret123"},
                    headers={"Content-Type": "application/x-www-form-urlencoded"})
    return r.json()["access_token"]


def test_create_publish_and_list_public_events(client):
    token = make_user_and_token(client, "org@mail.com", role="organizer")

    # crear (draft)
    evt = {
        "name": "TechConf 2025",
        "description": "Conferencia",
        "start_at": "2025-12-01T09:00:00Z",
        "end_at": "2025-12-01T18:00:00Z",
        "venue": "Bogota",
        "capacity_total": 100
    }
    r = client.post("/events", json=evt, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 201, r.text
    event_id = r.json()["id"]

    # publicar
    r = client.patch(f"/events/{event_id}/publish", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "published"

    # listado público SIN token
    r = client.get("/events?q=tech&page=1&page_size=10")
    assert r.status_code == 200
    data = r.json()
    assert data["meta"]["total"] == 1
    assert data["items"][0]["id"] == event_id

    # detalle público
    r = client.get(f"/events/{event_id}")
    assert r.status_code == 200
