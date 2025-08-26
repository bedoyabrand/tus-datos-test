# backend/app/db/base_class.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base para modelos SQLAlchemy."""
    pass
