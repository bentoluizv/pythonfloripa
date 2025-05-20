from http import HTTPStatus

import pytest


@pytest.mark.anyio
async def test_create_speaker(client):
    speaker_data = {
        'name': 'Speaker 1',
        'email': 'speaker1@example.com',
        'linkedin_url': 'https://www.linkedin.com/in/speaker1',
        'github_url': 'https://github.com/speaker1',
        'twitter_url': 'https://twitter.com/speaker1',
        'website_url': 'https://speaker1.com',
        'bio': 'Speaker 1 bio',
        'image_url': 'https://speaker1.com/image.jpg',
    }

    response = await client.post('/speakers', json=speaker_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Speaker 1'
    assert response.json()['email'] == 'speaker1@example.com'
    assert response.json()['linkedin_url'] == 'https://www.linkedin.com/in/speaker1'
    assert response.json()['github_url'] == 'https://github.com/speaker1'
    assert response.json()['twitter_url'] == 'https://twitter.com/speaker1'
    assert response.json()['website_url'] == 'https://speaker1.com'
    assert response.json()['bio'] == 'Speaker 1 bio'
    assert response.json()['image_url'] == 'https://speaker1.com/image.jpg'


@pytest.mark.anyio
async def test_get_speaker(client, create_speaker):
    response = await client.get(f'/speakers/{create_speaker.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == create_speaker.name
    assert response.json()['email'] == create_speaker.email
    assert response.json()['linkedin_url'] == create_speaker.linkedin_url
    assert response.json()['github_url'] == create_speaker.github_url
    assert response.json()['twitter_url'] == create_speaker.twitter_url
    assert response.json()['website_url'] == create_speaker.website_url
    assert response.json()['bio'] == create_speaker.bio
    assert response.json()['image_url'] == create_speaker.image_url


@pytest.mark.anyio
async def test_update_speaker(client, create_speaker):
    speaker_data = {
        'name': 'Updated Speaker',
        'email': 'updated@example.com',
        'linkedin_url': 'https://www.linkedin.com/in/updated',
        'github_url': 'https://github.com/updated',
        'twitter_url': 'https://twitter.com/updated',
        'website_url': 'https://updated.com',
        'bio': 'Updated Speaker bio',
        'image_url': 'https://updated.com/image.jpg',
    }

    response = await client.patch(f'/speakers/{create_speaker.id}', json=speaker_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'Updated Speaker'
    assert response.json()['email'] == 'updated@example.com'
    assert response.json()['linkedin_url'] == 'https://www.linkedin.com/in/updated'
    assert response.json()['github_url'] == 'https://github.com/updated'
    assert response.json()['twitter_url'] == 'https://twitter.com/updated'
    assert response.json()['website_url'] == 'https://updated.com'
    assert response.json()['bio'] == 'Updated Speaker bio'
    assert response.json()['image_url'] == 'https://updated.com/image.jpg'


@pytest.mark.anyio
async def test_delete_speaker(client, create_speaker):
    response = await client.delete(f'/speakers/{create_speaker.id}')

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.anyio
async def test_list_speakers(client, create_speaker):
    response = await client.get('/speakers')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['items']) == 1
    assert response.json()['items'][0]['id'] == create_speaker.id
    assert response.json()['items'][0]['name'] == create_speaker.name
    assert response.json()['items'][0]['email'] == create_speaker.email
    assert response.json()['items'][0]['linkedin_url'] == create_speaker.linkedin_url
    assert response.json()['items'][0]['github_url'] == create_speaker.github_url
    assert response.json()['items'][0]['twitter_url'] == create_speaker.twitter_url
    assert response.json()['items'][0]['website_url'] == create_speaker.website_url
    assert response.json()['items'][0]['bio'] == create_speaker.bio
    assert response.json()['items'][0]['image_url'] == create_speaker.image_url


@pytest.mark.anyio
async def test_create_speaker_that_already_exists(client, create_speaker):
    speaker_data = {
        'name': 'Speaker 1',
        'email': create_speaker.email,
        'linkedin_url': 'https://www.linkedin.com/in/speaker1',
        'github_url': 'https://github.com/speaker1',
        'twitter_url': 'https://twitter.com/speaker1',
        'website_url': 'https://speaker1.com',
        'bio': 'Speaker 1 bio',
        'image_url': 'https://speaker1.com/image.jpg',
    }

    response = await client.post('/speakers', json=speaker_data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Speaker with this email already exists'


@pytest.mark.anyio
async def test_get_non_existent_speaker(client):
    response = await client.get('/speakers/non-existent-id')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Speaker not found'


@pytest.mark.anyio
async def test_update_non_existent_speaker(client):
    speaker_data = {
        'name': 'Updated Speaker',
        'email': 'updated@example.com',
        'linkedin_url': 'https://www.linkedin.com/in/updated',
        'github_url': 'https://github.com/updated',
        'twitter_url': 'https://twitter.com/updated',
        'website_url': 'https://updated.com',
        'bio': 'Updated Description',
        'image_url': 'https://updated.com/image.jpg',
    }

    response = await client.patch('/speakers/non-existent-id', json=speaker_data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Speaker not found'


@pytest.mark.anyio
async def test_delete_non_existent_speaker(client):
    response = await client.delete('/speakers/non-existent-id')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Speaker not found'
