from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo_teste.database import get_session
from todo_teste.models import Todo, TodoStatus
from todo_teste.schemas import (
    Message,
    TodoFilters,
    TodoList,
    TodoPublic,
    TodoSchema,
)
from todo_teste.security import get_current_user

router = APIRouter(prefix='/todo', tags=['todo'])


@router.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    todo_database = Todo(
        title=todo.title,
        description=todo.description,
        status=todo.status,
        user_id=current_user.id,
    )

    session.add(todo_database)
    session.commit()
    session.refresh(todo_database)

    return todo_database


@router.get('/', response_model=TodoList)
def list_todo(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    filters: TodoFilters = Depends(),
):
    query = select(Todo).where(Todo.user_id == current_user.id)

    if filters.title:
        query = query.where(Todo.title.contains(filters.title))
    if filters.description:
        query = query.where(Todo.description.contains(filters.description))
    if filters.status:
        query = query.where(Todo.status == filters.status)

    todos = session.scalars(query.offset(filters.offset).limit(filters.limit)).all()

    return {'todos': todos}


@router.put('/{todo_id}', response_model=TodoPublic)
def update_todo(
    todo_id: int,
    todo: TodoSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    todo_database = session.scalar(
        select(Todo).where(Todo.user_id == current_user.id, Todo.id == todo_id)
    )

    if not todo_database:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not Found')

    todo_database.title = todo.title
    todo_database.description = todo.description
    todo_database.status = todo.status

    if todo_database.status == TodoStatus.done and todo_database.done_at is None:
        todo_database.done_at = datetime.utcnow()

    if todo_database.status != TodoStatus.done and todo_database.done_at is not None:
        todo_database.done_at = None

    session.commit()
    session.refresh(todo_database)

    return todo_database


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == current_user.id, Todo.id == todo_id)
    )
    if not todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not Found')

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully'}
