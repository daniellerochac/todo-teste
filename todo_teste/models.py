from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


class TodoStatus(str, Enum):
    pending = ('pending',)
    running = ('running',)
    done = 'done'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[TodoStatus]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    done_at: Mapped[datetime | None] = mapped_column(init=False, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
