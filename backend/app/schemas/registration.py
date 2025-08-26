from __future__ import annotations
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class RegistrationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class RegistrationCreate(BaseModel):
    session_id: int | None = None  # opcional; si va a una sesión específica


class RegistrationOut(BaseModel):
    id: int
    user_id: int
    event_id: int
    session_id: int | None
    status: RegistrationStatus
    created_at: datetime

    class Config:
        from_attributes = True
