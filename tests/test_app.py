from http import HTTPStatus

import pytest


@pytest.mark.anyio
async def test_root(client):
    response = await client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
