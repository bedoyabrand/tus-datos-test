from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user, require_role, get_current_user_optional
from app.models import User, UserRole, Event, EventStatus
from app.schemas.event import EventCreate, EventUpdate, EventOut, PaginatedEvents, PageMeta
from app.services.events import validate_times, can_publish, can_archive, apply_search_and_pagination

router = APIRouter(prefix="/events", tags=["events"])


# Crear evento (organizer/admin)
@router.post("", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.organizer, UserRole.admin)),
):
    validate_times(payload.start_at, payload.end_at)
    evt = Event(
        organizer_id=user.id,
        name=payload.name,
        description=payload.description,
        start_at=payload.start_at,
        end_at=payload.end_at,
        venue=payload.venue,
        capacity_total=payload.capacity_total,
        status=EventStatus.draft,
    )
    db.add(evt)
    db.commit()
    db.refresh(evt)
    return evt


# Listado público (solo published); si viene autenticado con rol, puede ver más con filtros
@router.get("", response_model=PaginatedEvents)
def list_events(
    q: str | None = Query(default=None, description="Búsqueda por nombre (substring)"),
    status: EventStatus | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current: User | None = Depends(get_current_user_optional)
):
    # si no hay usuario autenticado → solo publicados
    only_published = current is None
    items, total = apply_search_and_pagination(db, q, status, page, page_size, only_published)
    return {"items": items, "meta": PageMeta(page=page, page_size=page_size, total=total)}


# Detalle: público si published; organizador/admin puede ver su draft/archived
@router.get("/{event_id}", response_model=EventOut)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current: User | None = Depends(get_current_user_optional),
):
    evt = db.get(Event, event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")
    if evt.status != EventStatus.published:
        if not current or (current.role not in (UserRole.admin, UserRole.organizer) or current.id != evt.organizer_id and current.role != UserRole.admin):
            raise HTTPException(status_code=404, detail="Event not found")
    return evt


# Actualizar (solo organizador dueño o admin)
@router.put("/{event_id}", response_model=EventOut)
def update_event(
    event_id: int,
    payload: EventUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.organizer, UserRole.admin)),
):
    evt = db.get(Event, event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")
    if user.role != UserRole.admin and evt.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    data = payload.model_dump(exclude_unset=True)
    if "start_at" in data or "end_at" in data:
        validate_times(data.get("start_at", evt.start_at), data.get("end_at", evt.end_at))
    for k, v in data.items():
        setattr(evt, k, v)
    db.commit()
    db.refresh(evt)
    return evt


# Publicar
@router.patch("/{event_id}/publish", response_model=EventOut)
def publish_event(
    event_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.organizer, UserRole.admin)),
):
    evt = db.get(Event, event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")
    if user.role != UserRole.admin and evt.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    can_publish(evt)
    evt.status = EventStatus.published
    db.commit()
    db.refresh(evt)
    return evt


# Archivar
@router.patch("/{event_id}/archive", response_model=EventOut)
def archive_event(
    event_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.organizer, UserRole.admin)),
):
    evt = db.get(Event, event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")
    if user.role != UserRole.admin and evt.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    can_archive(evt)
    evt.status = EventStatus.archived
    db.commit()
    db.refresh(evt)
    return evt


# Eliminar (suelo permitir solo admin; o dueño si está draft)
@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.organizer, UserRole.admin)),
):
    evt = db.get(Event, event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")

    if user.role == UserRole.admin:
        pass
    elif evt.organizer_id == user.id and evt.status == EventStatus.draft:
        pass
    else:
        raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(evt)
    db.commit()
    return
