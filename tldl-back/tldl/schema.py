"""
Data structures, used in project.

You may do changes in tables here, then execute
`alembic revision --message="Your text" --autogenerate`
"""

from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import enum

from sqlalchemy import (
    DateTime,
    ForeignKey,
    MetaData,
    func,
)


# see https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__" "%(referred_table_name)s"),
    "pk": "pk__%(table_name)s",
}

# Registry for all tables
metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    pass


class VideoStatus(enum.Enum):
    created = "created"
    cleaned = "cleaned"
    notified = "notified"


class VideoProcessing(Base):
    __tablename__ = "video_processing"

    uid: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, type_=PGUUID, default=uuid.uuid4
    )
    status: Mapped[VideoStatus]

    chat_id: Mapped[str]
    msg_id: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=func.now(), type_=DateTime)
    finished_at: Mapped[datetime] = mapped_column(default=func.now(), type_=DateTime)

    meta: Mapped[dict] = mapped_column(nullable=False, server_default="{}", type_=JSONB)

    # NOTE raw_file_path has schema {bucket}/{object_uid}, ex: tldl-raw/1f1fe1b3-a54de49d-b177a18e-846496de.mp4
    raw_file_path: Mapped[str]
    # NOTE ready_file_path has schema {bucket}/{object_uid}, ex: tldl-raw/1f1fe1b3-a54de49d-b177a18e-846496de.mp4
    ready_file_path: Mapped[Optional[str]]
