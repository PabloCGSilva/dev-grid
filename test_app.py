import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_post_collect(client):
    response = client.post('/collect', json={
        'user_id': 'test_user',
        'city_ids': [3439525, 3439781]
    })
    assert response.status_code == 202

def test_get_progress(client):
    response = client.get('/progress/test_user')
    assert response.status_code == 200 or response.status_code == 404
