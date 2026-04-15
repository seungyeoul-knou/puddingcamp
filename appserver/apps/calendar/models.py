
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from pydantic import AwareDatetime
from sqlalchemy import JSON, Text
from sqlalchemy_utc import UtcDateTime
from sqlmodel import Field, SQLModel, func, Relationship, Text, JSON
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from appserver.apps.account.models import User


class Calendar(SQLModel, table=True):
    __tablename__ = "calendars"

    id: int = Field(default=None, primary_key=True)
    topics: list[str] = Field(
        sa_type=JSON().with_variant(JSONB(astext_type=Text()), "postgresql"), 
        description="게스트와 나눌 주제들"
        )
    description: str = Field(sa_type=Text, description="게스트에게 보여 줄 설명")
    google_calendar_id: str = Field(max_length=1024, description="구글 캘린더 ID")

    host_id: int = Field(foregin_key="user.id", unique=True)
    host: "User" = Relationship(back_populates="calendar")

    created_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    updated_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )