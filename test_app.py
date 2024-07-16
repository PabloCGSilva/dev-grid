import pytest
import json
import subprocess
import time
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_post_collect_valid_data(client):
    data = {'user_id': 'test_user', 'city_ids': [3439525]}
    response = client.post('/collect', json=data)
    assert response.status_code == 202

def test_post_collect_missing_data(client):
    data = {'user_id': 'test_user'}
    response = client.post('/collect', json=data)
    assert response.status_code == 400

def test_post_collect_invalid_city_ids(client):
    data = {'user_id': 'test_user', 'city_ids': 'invalid'}
    response = client.post('/collect', json=data)
    assert response.status_code == 400

def test_post_collect_empty_city_ids(client):
    data = {'user_id': 'test_user', 'city_ids': []}
    response = client.post('/collect', json=data)
    assert response.status_code == 400

def test_post_collect_exceeded_city_ids(client):
    data = {'user_id': 'test_user', 'city_ids': list(range(1001))}
    response = client.post('/collect', json=data)
    assert response.status_code == 400

def test_post_collect_nonexistent_user_id(client):
    data = {'user_id': 'nonexistent_user', 'city_ids': [3439525]}
    response = client.post('/collect', json=data)
    assert response.status_code == 404

def test_collect_endpoint_bad_request(client):
    response = client.post('/collect')
    assert response.status_code == 400

def test_collect_endpoint_invalid_content_type(client):
    headers = {'Content-Type': 'text/plain'}
    response = client.post('/collect', headers=headers, data=json.dumps({}))
    assert response.status_code == 415

def test_app_run():
    try:
        proc = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)  # Wait for server to start
        assert proc.poll() is None, f"Server process failed to start. Return code: {proc.returncode}. Stderr: {proc.stderr.read().decode()}"

    except Exception as e:
        pytest.fail(f"Failed to start server process: {str(e)}")

    finally:
        if proc:
            proc.terminate()
            proc.wait(timeout=2)  # Wait for server to terminate
            assert proc.returncode == 0, f"Server process did not terminate correctly. Return code: {proc.returncode}"
