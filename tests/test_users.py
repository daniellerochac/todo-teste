from http import HTTPStatus

from todo_teste.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        'users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'test@test.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testusername2',
            'email': 'test@test.com',
            'password': '123',
            'id': user.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testusername2',
        'email': 'test@test.com',
        'id': user.id,
    }


def test_update_wrong_user(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testusername2',
            'email': 'test@test.com',
            'password': '123',
            'id': user.id,
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}


def test_delete_wrong_user(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}
