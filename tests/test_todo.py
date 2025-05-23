from http import HTTPStatus

from todo_teste.models import Todo, TodoStatus


def test_create_todo(client, token):
    response = client.post(
        '/todo',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'test todo',
            'description': 'test todo description',
            'status': 'pending',
        },
    )

    json_response = response.json()
    assert 'id' in json_response
    assert json_response['title'] == 'test todo'
    assert json_response['description'] == 'test todo description'
    assert json_response['status'] == 'pending'
    assert 'created_at' in json_response
    assert 'updated_at' in json_response
    assert json_response['done_at'] is None


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    todos = [
        Todo(
            title=f'Task {i}',
            description='description',
            status=TodoStatus.done,
            user_id=user.id,
        )
        for i in range(expected_todos)
    ]

    session.add_all(todos)
    session.commit()

    response = client.get(
        '/todo',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'todos' in response.json()
    assert len(response.json()['todos']) == expected_todos

    for todo in response.json()['todos']:
        assert 'created_at' in todo
        assert 'updated_at' in todo
        assert 'done_at' in todo


def test_list_should_return_2_todos(session, client, user, token):
    expected_todos = 2
    total_todos = 5

    todos = [
        Todo(
            title=f'Task {i}',
            description='description',
            status=TodoStatus.pending,
            user_id=user.id,
        )
        for i in range(total_todos)
    ]

    session.add_all(todos)
    session.commit()

    response = client.get(
        '/todo/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'todos' in response.json()
    assert len(response.json()['todos']) == expected_todos

    for todo in response.json()['todos']:
        assert 'created_at' in todo
        assert 'updated_at' in todo
        assert 'done_at' in todo


def test_list_todo_filter_title(session, client, user, token):
    expected_todos = 5
    other_todos_count = 3

    todos = [
        Todo(
            title='Test todo title',
            description='description',
            status=TodoStatus.pending,
            user_id=user.id,
        )
        for _ in range(expected_todos)
    ]

    other_todos = [
        Todo(
            title='Test other title',
            description='description',
            status=TodoStatus.pending,
            user_id=user.id,
        )
        for _ in range(other_todos_count)
    ]

    session.add_all(todos + other_todos)
    session.commit()

    response = client.get(
        '/todo/?title=Test todo title',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'todos' in response.json()
    assert len(response.json()['todos']) == expected_todos

    for todo in response.json()['todos']:
        assert 'created_at' in todo
        assert 'updated_at' in todo
        assert 'done_at' in todo


def test_list_todo_filter_description(session, client, user, token):
    expected_todos = 5
    other_todos_count = 3
    filter_description = 'desc_filter'

    todos = [
        Todo(
            title=f'Task {i}',
            description=f'description {filter_description}',
            status=TodoStatus.running,
            user_id=user.id,
        )
        for i in range(expected_todos)
    ]

    other_todos = [
        Todo(
            title=f'Task {i}',
            description='other description',
            status=TodoStatus.running,
            user_id=user.id,
        )
        for i in range(other_todos_count)
    ]

    session.add_all(todos + other_todos)
    session.commit()

    response = client.get(
        f'/todo/?description={filter_description}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'todos' in response.json()
    assert len(response.json()['todos']) == expected_todos

    for todo in response.json()['todos']:
        assert 'created_at' in todo
        assert 'updated_at' in todo
        assert 'done_at' in todo


def test_list_todo_filter_state(session, client, user, token):
    expected_todos = 5
    other_todos_count = 3
    filter_status = TodoStatus.running

    todos = [
        Todo(
            title=f'Task {i}',
            description='description',
            status=filter_status,
            user_id=user.id,
        )
        for i in range(expected_todos)
    ]

    other_todos = [
        Todo(
            title=f'Task {i}',
            description='description',
            status=TodoStatus.done,
            user_id=user.id,
        )
        for i in range(other_todos_count)
    ]

    session.add_all(todos + other_todos)
    session.commit()

    response = client.get(
        f'/todo/?status={filter_status.value}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'todos' in response.json()
    assert len(response.json()['todos']) == expected_todos

    for todo in response.json()['todos']:
        assert todo['status'] == filter_status.value
        assert 'created_at' in todo
        assert 'updated_at' in todo
        assert 'done_at' in todo


def test_list_todo_filters_combined_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    other_todos_count = 3

    todos = [
        Todo(
            title='Test todo combined',
            description='combined description',
            status=TodoStatus.done,
            user_id=user.id,
        )
        for _ in range(expected_todos)
    ]

    other_todos = [
        Todo(
            title='Other title',
            description='other description',
            status=TodoStatus.pending,
            user_id=user.id,
        )
        for _ in range(other_todos_count)
    ]

    session.add_all(todos + other_todos)
    session.commit()

    response = client.get(
        '/todo/?title=Test todo combined&description=combined&status=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'todos' in response.json()
    assert len(response.json()['todos']) == expected_todos

    for todo in response.json()['todos']:
        assert todo['title'] == 'Test todo combined'
        assert 'combined' in todo['description']
        assert todo['status'] == TodoStatus.done.value
        assert 'created_at' in todo
        assert 'updated_at' in todo
        assert 'done_at' in todo


def test_update_todo(session, client, user, token):
    todo = Todo(
        title='test todo',
        description='test todo description',
        status=TodoStatus.running,
        user_id=user.id,
    )

    session.add(todo)
    session.commit()

    updated_data = {
        'title': 'updated todo',
        'description': 'updated todo description',
        'status': TodoStatus.done.value,
    }

    response = client.put(
        f'/todo/{todo.id}',
        json=updated_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

    json_response = response.json()

    assert json_response['title'] == updated_data['title']
    assert json_response['description'] == updated_data['description']
    assert json_response['status'] == updated_data['status']
    assert 'created_at' in json_response
    assert 'updated_at' in json_response
    assert 'done_at' in json_response
    assert json_response['done_at'] is not None


def test_update_todo_error(client, token):
    updated_data = {
        'title': 'test title',
        'description': 'test description',
        'status': 'pending',
    }

    response = client.put(
        '/todo/9999',
        json=updated_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_delete_todo(session, client, user, token):
    todo = Todo(
        title='delete to do',
        description='this will be deleted',
        status=TodoStatus.pending,
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(
        f'/todo/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully'}


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/todo/{100}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}