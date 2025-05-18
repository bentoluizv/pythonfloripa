from http import HTTPStatus

import pytest


@pytest.mark.anyio
async def test_create_event(client):
    event_data = {
        'edition': 1,
        'title': 'Event 1',
        'description': 'Description 1',
        'start_date': '2021-01-01',
        'end_date': '2021-01-02',
        'location': 'Location 1',
        'image_url': 'https://example.com/image.jpg',
    }
    response = await client.post('/events', json=event_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['title'] == 'Event 1'
    assert response.json()['talks'] == []


@pytest.mark.anyio
async def test_get_event(client, create_event):
    response = await client.get(f'/events/{create_event.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == create_event.title


@pytest.mark.anyio
async def test_update_event(client, create_event):
    update_data = {
        'title': 'Event 2',
    }
    response = await client.patch(f'/events/{create_event.id}', json=update_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == update_data['title']


@pytest.mark.anyio
async def test_delete_event(client, create_event):
    response = await client.delete(f'/events/{create_event.id}')
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.anyio
async def test_list_events(client, create_event):
    response = await client.get('/events')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['items']) > 0


@pytest.mark.anyio
async def test_already_exists_edition(client, create_event):
    event_data = {
        'edition': 1,
        'title': 'Event 2',
        'description': 'Description 2',
        'start_date': '2021-01-01',
        'end_date': '2021-01-02',
        'location': 'Location 2',
        'image_url': 'https://example.com/image.jpg',
    }
    response = await client.post('/events', json=event_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Event with this edition already exists'
