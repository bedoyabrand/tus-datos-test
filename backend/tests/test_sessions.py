def setup_published_event(client):
    # organizer
    client.post("/auth/register", json={"email": "org@mail.com", "password": "secret123", "role": "organizer"})
    r = client.post("/auth/login", data={"username": "org@mail.com", "password": "secret123"},
                    headers={"Content-Type": "application/x-www-form-urlencoded"})
    token = r.json()["access_token"]

    # event
    evt = {
        "name": "Event",
        "description": "Desc",
        "start_at": "2025-12-01T09:00:00Z",
        "end_at": "2025-12-01T18:00:00Z",
        "venue": "HQ",
        "capacity_total": 10
    }
    e = client.post("/events", json=evt, headers={"Authorization": f"Bearer {token}"}).json()
    client.patch(f"/events/{e['id']}/publish", headers={"Authorization": f"Bearer {token}"})
    return token, e["id"]


def test_session_overlap(client):
    token, event_id = setup_published_event(client)

    # crea primera sesión
    s1 = {
        "title": "Apertura",
        "start_at": "2025-12-01T09:30:00Z",
        "end_at": "2025-12-01T10:30:00Z",
        "room": "Auditorio 1",
        "capacity": 50
    }
    r = client.post(f"/events/{event_id}/sessions", json=s1, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 201, r.text

    # intenta solapar MISMO room -> 409
    s2 = {
        "title": "Solapada",
        "start_at": "2025-12-01T10:00:00Z",
        "end_at": "2025-12-01T11:00:00Z",
        "room": "Auditorio 1",
        "capacity": 50
    }
    r = client.post(f"/events/{event_id}/sessions", json=s2, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 409, r.text

    # otro room mismo horario -> OK
    s3 = {**s2, "room": "Sala 2"}
    r = client.post(f"/events/{event_id}/sessions", json=s3, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 201, r.text

    # listado público
    r = client.get(f"/events/{event_id}/sessions")
    assert r.status_code == 200
    assert len(r.json()) == 2
