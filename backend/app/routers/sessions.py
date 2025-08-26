from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import base as models_base  # asegura modelos cargados
from app.core.deps import require_role, get_current_user, get_current_user_optional
from app.models.user import User, UserRole
from app.models.event import Event, EventStatus
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate, SessionUpdate, SessionOut
from app.services.sessions import validate_times, assert_no_overlap

router = APIRouter(prefix="/events/{event_id}/sessions", tags=["sessions"])


def assert_can_manage_event(event: Event, user: User):
    if user.role != UserRole.admin and event.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.post("", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(
    event_id: int,
    payload: SessionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.organizer, UserRole.admin)),
):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    assert_can_manage_event(event, user)
    validate_times(payload.start_at, payload.end_at)
    assert_no_overlap(db, event_id, payload.start_at, payload.end_at, payload.room)

    sess = SessionModel(event_id=event_id, **payload.model_dump())
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess


@router.get("", response_model=list[SessionOut])
def list_sessions(
    event_id: int,
    db: Session = Depends(get_db),
    current: User | None = Depends(get_current_user_optional),
):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Si el evento no es publicado, solo organizador o admin pueden verlas
    if event.status != EventStatus.published:
        if not current or (current.role != UserRole.admin and current.id != event.organizer_id):
            raise HTTPException(status_code=404, detail="Event not found")

    return db.query(SessionModel).where(SessionModel.event_id == event_id).order_by(SessionModel.start_at).all()


@router.put("/{session_id}", response_model=SessionOut)
def update_session(
    event_id: int,
    session_id: int,
    payload: SessionUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.organizer, UserRole.admin)),
):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    assert_can_manage_event(event, user)

    sess = db.get(SessionModel, session_id)
    if not sess or sess.event_id != event_id:
        raise HTTPException(status_code=404, detail="Session not found")

    data = payload.model_dump(exclude_unset=True)
    start = data.get("start_at", sess.start_at)
    end = data.get("end_at", sess.end_at)
    room = data.get("room", sess.room)
    validate_times(start, end)
    assert_no_overlap(db, event_id, start, end, room, exclude_id=session_id)

    for k, v in data.items():
        setattr(sess, k, v)
    db.commit()
    db.refresh(sess)
    return sess


@router.delete("/{session_id}", status_code=204)
def delete_session(
    event_id: int,
    session_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.organizer, UserRole.admin)),
):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    assert_can_manage_event(event, user)

    sess = db.get(SessionModel, session_id)
    if not sess or sess.event_id != event_id:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(sess)
    db.commit()
