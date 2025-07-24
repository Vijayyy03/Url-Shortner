import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url_success(client):
    response = client.post('/api/shorten', json={'url': 'https://www.example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data

    # Save for later tests
    global short_code
    short_code = data['short_code']


def test_shorten_url_invalid(client):
    response = client.post('/api/shorten', json={'url': 'not-a-valid-url'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_redirect_success(client):
    # Use the short_code from the previous test
    response = client.post('/api/shorten', json={'url': 'https://www.example.com/redirect'})
    code = response.get_json()['short_code']
    response = client.get(f'/{code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'] == 'https://www.example.com/redirect'


def test_redirect_not_found(client):
    response = client.get('/nonexistent', follow_redirects=False)
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data


def test_analytics_and_click_count(client):
    # Shorten a URL
    response = client.post('/api/shorten', json={'url': 'https://www.example.com/stats'})
    code = response.get_json()['short_code']
    # Click it 3 times
    for _ in range(3):
        client.get(f'/{code}')
    # Check stats
    response = client.get(f'/api/stats/{code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['url'] == 'https://www.example.com/stats'
    assert data['clicks'] == 3
    assert 'created_at' in data