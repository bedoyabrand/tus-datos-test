from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime


class SessionCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    start_at: datetime
    end_at: datetime
    room: str | None = None
    capacity: int | None = Field(default=None, ge=0)
    speaker_name: str | None = None
    speaker_bio: str | None = None


class SessionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    room: str | None = None
    capacity: int | None = Field(default=None, ge=0)
    speaker_name: str | None = None
    speaker_bio: str | None = None


class SessionOut(BaseModel):
    id: int
    event_id: int
    title: str
    description: str | None
    start_at: datetime
    end_at: datetime
    room: str | None
    capacity: int | None
    speaker_name: str | None
    speaker_bio: str | None

    class Config:
        from_attributes = True
