from dataclasses import asdict

from sqlalchemy import select

from todo_teste.models import User


def test_create_user(session):
    new_user = User(
        username='danielle',
        email='danielle@test.com',
        password='senha',
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'danielle'))

    assert asdict(user) == {
        'id': 1,
        'username': 'danielle',
        'email': 'danielle@test.com',
        'password': 'senha',
    }
