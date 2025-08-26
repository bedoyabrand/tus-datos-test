from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Enum, UniqueConstraint
import enum

from app.db.base_class import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    organizer = "organizer"
    attendee = "attendee"


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.attendee)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    organized_events = relationship("Event", back_populates="organizer", cascade="all,delete")
    registrations = relationship("Registration", back_populates="user", cascade="all,delete")

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )
