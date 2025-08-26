from __future__ import annotations
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.session import Session as SessionModel


def validate_times(start_at, end_at):
    if start_at >= end_at:
        raise HTTPException(status_code=422, detail="start_at must be before end_at")


def assert_no_overlap(db: Session, event_id: int, start_at, end_at, room: str | None, exclude_id: int | None = None):
    q = db.query(SessionModel).filter(SessionModel.event_id == event_id)
    if exclude_id is not None:
        q = q.filter(SessionModel.id != exclude_id)
    # Solapamiento cuando start < other.end y end > other.start (mismo room si se especifica)
    overlap_filter = and_(SessionModel.start_at < end_at, SessionModel.end_at > start_at)
    if room:
        q = q.filter(SessionModel.room == room).filter(overlap_filter)
    else:
        q = q.filter(overlap_filter)
    if db.query(q.exists()).scalar():
        raise HTTPException(status_code=409, detail="Session time overlaps with another session")
