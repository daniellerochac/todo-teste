from http import HTTPStatus

from jwt import decode

from todo_teste.security import create_access_token, settings


def test_jwt(token):
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
