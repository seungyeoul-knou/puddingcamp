from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, func
from pydantic import EmailStr, AwareDatetime
from sqlalchemy import UniqueConstraint
from sqlalchemy_utc import UtcDateTime

class User(SQLModel, table=True):
    __tablename__="users"
    __table_args__=(
        UniqueConstraint("email", name="uq_email"),
    )

    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=40, description="사용자 계정 ID")
    email: EmailStr = Field(max_length=128, description="사용자 이메일")
    display_name: str = Field(max_length=40, description="사용자 표시 이름")
    password: str = Field(max_length=128, description="사용자 비밀번호")
    is_host: bool = Field(default=False, description="사용자가 호스트인지 여부")
    created_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
        }
    )
    updated_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": lambda: datetime.now(timezone.utc)
        }
    )