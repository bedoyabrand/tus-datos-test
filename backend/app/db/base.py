from sqlalchemy.orm import DeclarativeBase
from app.db.base_class import Base

from app.models.user import User  # noqa: F401
from app.models.event import Event  # noqa: F401
from app.models.session import Session  # noqa: F401
from app.models.registration import Registration  # noqa: F401
