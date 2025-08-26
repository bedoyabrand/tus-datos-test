from __future__ import annotations
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class EventStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class EventCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str | None = None
    start_at: datetime
    end_at: datetime
    venue: str | None = None
    capacity_total: int = Field(ge=0)


class EventUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    venue: str | None = None
    capacity_total: int | None = Field(default=None, ge=0)


class EventOut(BaseModel):
    id: int
    organizer_id: int
    name: str
    description: str | None
    start_at: datetime
    end_at: datetime
    venue: str | None
    status: EventStatus
    capacity_total: int
    created_at: datetime

    class Config:
        from_attributes = True


class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int


class PaginatedEvents(BaseModel):
    items: list[EventOut]
    meta: PageMeta
