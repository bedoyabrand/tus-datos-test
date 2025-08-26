from __future__ import annotations
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.event import Event, EventStatus


def validate_times(start_at, end_at):
    if start_at >= end_at:
        raise HTTPException(status_code=422, detail="start_at must be before end_at")


def can_publish(evt: Event):
    if evt.status != EventStatus.draft:
        raise HTTPException(status_code=409, detail="Only draft events can be published")
    validate_times(evt.start_at, evt.end_at)
    if evt.capacity_total is None or evt.capacity_total < 0:
        raise HTTPException(status_code=422, detail="capacity_total must be >= 0")


def can_archive(evt: Event):
    if evt.status == EventStatus.archived:
        raise HTTPException(status_code=409, detail="Event already archived")


def apply_search_and_pagination(
    db: Session, q: str | None, status: EventStatus | None, page: int, page_size: int, only_published: bool
):
    query = db.query(Event)
    if q:
        query = query.filter(Event.name.ilike(f"%{q}%"))
    if status:
        query = query.filter(Event.status == status)
    if only_published:
        query = query.filter(Event.status == EventStatus.published)

    total = query.count()
    items = (
        query.order_by(Event.start_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return items, total
