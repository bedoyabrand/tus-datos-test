def make_user_token(client, email, role):
    client.post("/auth/register", json={"email": email, "password": "secret123", "role": role})
    r = client.post("/auth/login", data={"username": email, "password": "secret123"},
                    headers={"Content-Type": "application/x-www-form-urlencoded"})
    return r.json()["access_token"]


def setup_small_event(client, capacity=1):
    org_token = make_user_token(client, "org2@mail.com", "organizer")
    evt = {
        "name": "Cupo Limitado",
        "description": "test",
        "start_at": "2025-12-01T09:00:00Z",
        "end_at": "2025-12-01T10:00:00Z",
        "venue": "HQ",
        "capacity_total": capacity,
    }
    e = client.post("/events", json=evt, headers={"Authorization": f"Bearer {org_token}"}).json()
    client.patch(f"/events/{e['id']}/publish", headers={"Authorization": f"Bearer {org_token}"})
    return e["id"]


def test_registration_capacity_and_uniqueness(client):
    event_id = setup_small_event(client, capacity=1)

    # usuario 1 se registra
    t1 = make_user_token(client, "user1@mail.com", "attendee")
    r = client.post(f"/events/{event_id}/register", json={}, headers={"Authorization": f"Bearer {t1}"})
    assert r.status_code == 201, r.text
    reg_id = r.json()["id"]

    # mismo usuario intenta de nuevo -> 409
    r = client.post(f"/events/{event_id}/register", json={}, headers={"Authorization": f"Bearer {t1}"})
    assert r.status_code == 409

    # usuario 2 intenta -> 409 por capacidad llena
    t2 = make_user_token(client, "user2@mail.com", "attendee")
    r = client.post(f"/events/{event_id}/register", json={}, headers={"Authorization": f"Bearer {t2}"})
    assert r.status_code == 409

    # cancelar registro del usuario 1
    r = client.patch(f"/events/registrations/{reg_id}/cancel", headers={"Authorization": f"Bearer {t1}"})
    assert r.status_code == 200
    assert r.json()["status"] == "cancelled"

    # ahora usuario 2 puede registrarse
    r = client.post(f"/events/{event_id}/register", json={}, headers={"Authorization": f"Bearer {t2}"})
    assert r.status_code == 201
