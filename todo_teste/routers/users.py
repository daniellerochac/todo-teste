from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo_teste.database import get_session
from todo_teste.models import User
from todo_teste.schemas import UserData, UserList, UserPublic

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserData, session: Session = Depends(get_session)):
    user_database = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if user_database:
        if user_database.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif user_database.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    user_database = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    session.add(user_database)
    session.commit()
    session.refresh(user_database)

    return user_database


@router.get('/', response_model=UserList)
def read_users(
    skip: int = 0,
    limit=100,
    session: Session = Depends(get_session),
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}
