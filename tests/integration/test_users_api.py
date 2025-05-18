from http import HTTPStatus

import pytest


@pytest.mark.anyio
async def test_create_user(client):
    user_data = {
        'username': 'bento',
        'email': 'bento@test.com',
        'password': 'an!RW9j7654321',
    }
    response = await client.post('/users', json=user_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['email'] == 'bento@test.com'


@pytest.mark.anyio
async def test_get_user(client, create_user):
    response = await client.get(f'/users/{create_user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['email'] == create_user.email


@pytest.mark.anyio
async def test_update_user(client, create_user):
    update_data = {
        'username': 'douglas312',
    }
    response = await client.patch(f'/users/{create_user.id}', json=update_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == update_data['username']


@pytest.mark.anyio
async def test_delete_user(client, create_user):
    response = await client.delete(f'/users/{create_user.id}')
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.anyio
async def test_list_users(client, create_user):
    response = await client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['items']) > 0


@pytest.mark.anyio
async def test_already_exists_email(client, create_user):
    user_data = {
        'username': 'teste',
        'email': 'bento@test.com',
        'password': 'an!RW9j7654321',
    }
    response = await client.post('/users', json=user_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'User with this email already exists'


@pytest.mark.anyio
async def test_already_exists_username(client, create_user):
    user_data = {
        'username': 'bento',
        'email': 'teste@test.com',
        'password': 'an!RW9j7654321',
    }
    response = await client.post('/users', json=user_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'User with this username already exists'


@pytest.mark.anyio
async def test_create_user_with_profile(client):
    user_data = {
        'username': 'bento',
        'email': 'bento@test.com',
        'password': 'an!RW9j7654321',
        'profile': {
            'full_name': 'Bento',
            'linkedin_url': 'https://linkedin.com/in/bento',
            'github_url': 'https://github.com/bento',
            'phone_number': '+5511999999999',
            'bio': 'teste',
        },
    }
    response = await client.post('/users', json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['profile']['full_name'] == 'Bento'
    assert response.json()['profile']['linkedin_url'] == 'https://linkedin.com/in/bento'
    assert response.json()['profile']['github_url'] == 'https://github.com/bento'
    assert response.json()['profile']['phone_number'] == '+5511999999999'
    assert response.json()['profile']['bio'] == 'teste'


@pytest.mark.anyio
async def test_update_user_with_profile(client, create_user):
    update_data = {
        'profile': {
            'full_name': 'Douglas',
        },
    }
    response = await client.patch(f'/users/{create_user.id}', json=update_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['profile']['full_name'] == 'Douglas'


@pytest.mark.anyio
async def test_not_exists_user(client):
    response = await client.get('/users/123')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


@pytest.mark.anyio
async def test_invalid_password(client):
    user_data = {
        'username': 'bento',
        'email': 'bento@test.com',
        'password': 'an',
    }
    response = await client.post('/users', json=user_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'String should have at least 8 characters'
