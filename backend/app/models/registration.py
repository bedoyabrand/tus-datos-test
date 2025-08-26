from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, Enum, ForeignKey, UniqueConstraint
import enum

from app.db.base_class import Base


class RegistrationStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Registration(Base):
    __tablename__ = "registration"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id", ondelete="CASCADE"), index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[int | None] = mapped_column(ForeignKey("session.id", ondelete="SET NULL"), index=True)
    status: Mapped[RegistrationStatus] = mapped_column(Enum(RegistrationStatus), default=RegistrationStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
    session = relationship("Session", back_populates="registrations")

    __table_args__ = (
        # Evita duplicar registro del mismo usuario al mismo evento (independiente de sesión)
        UniqueConstraint("user_id", "event_id", name="uq_registration_user_event"),
    )
