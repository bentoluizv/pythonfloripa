from http import HTTPStatus

import pytest


@pytest.mark.anyio
async def test_create_talk(client, create_event, create_speaker):
    talk_data = {
        'title': 'Talk 1',
        'description': 'Description 1',
        'speaker_id': create_speaker.id,
        'start_time': '2021-01-01T07:00:00Z',
        'end_time': '2021-01-01T09:45:00Z',
        'event_id': create_event.id,
    }

    response = await client.post('/talks', json=talk_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['title'] == 'Talk 1'
    assert response.json()['description'] == 'Description 1'
    assert response.json()['speaker_id'] == create_speaker.id
    assert response.json()['start_time'] == '2021-01-01T07:00:00Z'
    assert response.json()['end_time'] == '2021-01-01T09:45:00Z'
    assert response.json()['event_id'] == create_event.id


@pytest.mark.anyio
async def test_get_talk(client, create_talk, create_speaker):
    response = await client.get(f'/talks/{create_talk.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == create_talk.title
    assert response.json()['description'] == create_talk.description
    assert response.json()['speaker_id'] == create_speaker.id
    assert response.json()['start_time'] == create_talk.start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    assert response.json()['end_time'] == create_talk.end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    assert response.json()['event_id'] == create_talk.event_id


@pytest.mark.anyio
async def test_update_talk(client, create_talk, create_speaker):
    talk_data = {
        'title': 'Updated Talk',
        'description': 'Updated Description',
        'speaker_id': create_speaker.id,
        'start_time': '2021-01-01T07:00:00Z',
        'end_time': '2021-01-01T09:45:00Z',
        'event_id': create_talk.event_id,
    }

    response = await client.patch(f'/talks/{create_talk.id}', json=talk_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'Updated Talk'
    assert response.json()['description'] == 'Updated Description'
    assert response.json()['speaker_id'] == create_speaker.id
    assert response.json()['start_time'] == '2021-01-01T07:00:00Z'
    assert response.json()['end_time'] == '2021-01-01T09:45:00Z'
    assert response.json()['event_id'] == create_talk.event_id


@pytest.mark.anyio
async def test_delete_talk(client, create_talk):
    response = await client.delete(f'/talks/{create_talk.id}')

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.anyio
async def test_list_talks(client, create_talk, create_speaker):
    response = await client.get('/talks')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['items']) == 1
    assert response.json()['items'][0]['id'] == create_talk.id
    assert response.json()['items'][0]['title'] == create_talk.title
    assert response.json()['items'][0]['description'] == create_talk.description
    assert response.json()['items'][0]['speaker_id'] == create_speaker.id
    assert response.json()['items'][0]['start_time'] == create_talk.start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    assert response.json()['items'][0]['end_time'] == create_talk.end_time.strftime('%Y-%m-%dT%H:%M:%SZ')


@pytest.mark.anyio
async def test_create_talk_with_existing_title(client, create_talk, create_speaker):
    talk_data = {
        'title': 'Talk 1',
        'description': 'Description 1',
        'speaker_id': create_speaker.id,
        'start_time': '2021-01-01T07:00:00Z',
        'end_time': '2021-01-01T09:45:00Z',
        'event_id': create_talk.event_id,
    }

    response = await client.post('/talks', json=talk_data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Talk with this title already exists'


@pytest.mark.anyio
async def test_get_non_existent_talk(client):
    response = await client.get('/talks/non-existent-id')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Talk not found'


@pytest.mark.anyio
async def test_update_non_existent_talk(client, create_speaker):
    talk_data = {
        'title': 'Updated Talk',
        'description': 'Updated Description',
        'speaker_id': create_speaker.id,
        'start_time': '2021-01-01T07:00:00Z',
        'end_time': '2021-01-01T09:45:00Z',
        'event_id': 'non-existent-id',
    }

    response = await client.patch('/talks/non-existent-id', json=talk_data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Talk not found'


@pytest.mark.anyio
async def test_delete_non_existent_talk(client):
    response = await client.delete('/talks/non-existent-id')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Talk not found'


@pytest.mark.anyio
async def test_create_talk_with_invalid_event_id(client, create_speaker):
    talk_data = {
        'title': 'Talk 1',
        'description': 'Description 1',
        'speaker_id': create_speaker.id,
        'start_time': '2021-01-01T07:00:00Z',
        'end_time': '2021-01-01T09:45:00Z',
        'event_id': 'invalid-id',
    }

    response = await client.post('/talks', json=talk_data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Event does not exist'
