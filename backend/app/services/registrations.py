from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.event import Event, EventStatus
from app.models.session import Session as SessionModel
from app.models.registration import Registration, RegistrationStatus


def assert_event_can_register(db: Session, event_id: int):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.status != EventStatus.published:
        raise HTTPException(status_code=409, detail="Event is not open for registration")
    return event


def assert_session_belongs_to_event(db: Session, event_id: int, session_id: int | None) -> SessionModel | None:
    if session_id is None:
        return None
    sess = db.get(SessionModel, session_id)
    if not sess or sess.event_id != event_id:
        raise HTTPException(status_code=404, detail="Session not found")
    return sess


def current_event_registrations(db: Session, event_id: int) -> int:
    return db.query(func.count(Registration.id)).filter(
        Registration.event_id == event_id,
        Registration.status != RegistrationStatus.cancelled,
    ).scalar() or 0


def current_session_registrations(db: Session, session_id: int) -> int:
    return db.query(func.count(Registration.id)).filter(
        Registration.session_id == session_id,
        Registration.status != RegistrationStatus.cancelled,
    ).scalar() or 0


def ensure_capacity(db: Session, event, session: SessionModel | None):
    # Capacidad a nivel de evento
    if event.capacity_total is not None:
        taken = current_event_registrations(db, event.id)
        if taken >= event.capacity_total:
            raise HTTPException(status_code=409, detail="Event capacity reached")

    # Capacidad a nivel de sesión (si aplica)
    if session and session.capacity is not None:
        taken_sess = current_session_registrations(db, session.id)
        if taken_sess >= session.capacity:
            raise HTTPException(status_code=409, detail="Session capacity reached")


def create_registration(db: Session, user_id: int, event_id: int, session_id: int | None) -> Registration:
    # Verificaciones
    event = assert_event_can_register(db, event_id)
    session = assert_session_belongs_to_event(db, event_id, session_id)
    ensure_capacity(db, event, session)

    reg = Registration(user_id=user_id, event_id=event_id, session_id=session_id, status=RegistrationStatus.confirmed)
    db.add(reg)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Unicidad por (user_id, event_id)
        raise HTTPException(status_code=409, detail="User already registered for this event")
    db.refresh(reg)
    return reg
