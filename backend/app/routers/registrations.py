from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import base as models_base  # asegura que los modelos estén cargados
from app.core.deps import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.registration import Registration, RegistrationStatus
from app.schemas.registration import RegistrationCreate, RegistrationOut
from app.services.registrations import create_registration

router = APIRouter(prefix="/events", tags=["registrations"])


# POST /events/{event_id}/register
@router.post("/{event_id}/register", response_model=RegistrationOut, status_code=status.HTTP_201_CREATED)
def register_to_event(
    event_id: int,
    payload: RegistrationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    reg = create_registration(db, user_id=user.id, event_id=event_id, session_id=payload.session_id)
    return reg


# GET /me/registrations  (lista registros del usuario autenticado)
@router.get("/me/registrations", response_model=list[RegistrationOut], tags=["me"])
def my_registrations(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return db.query(Registration).filter(Registration.user_id == user.id).order_by(Registration.created_at.desc()).all()


# PATCH /registrations/{id}/cancel
@router.patch("/registrations/{registration_id}/cancel", response_model=RegistrationOut)
def cancel_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    reg = db.get(Registration, registration_id)
    if not reg or (user.role != UserRole.admin and reg.user_id != user.id):
        raise HTTPException(status_code=404, detail="Registration not found")
    if reg.status == RegistrationStatus.cancelled:
        return reg
    reg.status = RegistrationStatus.cancelled
    db.commit()
    db.refresh(reg)
    return reg
