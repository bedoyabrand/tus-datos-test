from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, Enum, ForeignKey, Index
import enum

from app.db.base_class import Base


class EventStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    organizer_id: Mapped[int] = mapped_column(ForeignKey("user_account.id", ondelete="RESTRICT"))
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str | None] = mapped_column(Text())
    start_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_at: Mapped[datetime] = mapped_column(DateTime)
    venue: Mapped[str | None] = mapped_column(String(200))
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), default=EventStatus.draft, index=True)
    capacity_total: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    organizer = relationship("User", back_populates="organized_events")
    sessions = relationship("Session", back_populates="event", cascade="all,delete-orphan")
    registrations = relationship("Registration", back_populates="event", cascade="all,delete-orphan")


Index("ix_event_status_start", Event.status, Event.start_at)
