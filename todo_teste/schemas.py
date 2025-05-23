from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from todo_teste.models import TodoStatus


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoSchema(BaseModel):
    title: str
    description: str
    status: TodoStatus


class TodoPublic(TodoSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    done_at: datetime | None


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoFilters(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TodoStatus | None = None
    offset: int | None = 0
    limit: int | None = 100
