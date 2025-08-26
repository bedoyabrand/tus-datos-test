from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Index

from app.db.base_class import Base


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text())
    start_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_at: Mapped[datetime] = mapped_column(DateTime)
    room: Mapped[str | None] = mapped_column(String(100))
    capacity: Mapped[int | None] = mapped_column(Integer)  # None = sin límite por sesión
    speaker_name: Mapped[str | None] = mapped_column(String(200))
    speaker_bio: Mapped[str | None] = mapped_column(Text())

    event = relationship("Event", back_populates="sessions")
    registrations = relationship("Registration", back_populates="session", cascade="all,delete")


Index("ix_session_event_start", Session.event_id, Session.start_at)
