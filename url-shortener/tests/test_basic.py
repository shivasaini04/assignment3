import pytest
from app.main import app
from app.models import url_store

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear URL store before each test
        url_store._urls.clear()
        yield client

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url(client):
    """Test URL shortening functionality"""
    # Test with valid URL
    response = client.post('/api/shorten', json={
        'url': 'https://www.example.com/very/long/url'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_code' in data
    assert len(data['short_code']) == 6
    assert data['original_url'] == 'https://www.example.com/very/long/url'
    
    # Test with invalid URL
    response = client.post('/api/shorten', json={
        'url': 'not-a-valid-url'
    })
    assert response.status_code == 400
    
    # Test with missing URL
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400

def test_url_redirect(client):
    """Test URL redirection"""
    # First, create a short URL
    response = client.post('/api/shorten', json={
        'url': 'https://www.example.com'
    })
    data = response.get_json()
    short_code = data['short_code']
    
    # Test redirection
    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.location == 'https://www.example.com'
    
    # Test non-existent short code
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_url_stats(client):
    """Test URL statistics"""
    # First, create a short URL
    response = client.post('/api/shorten', json={
        'url': 'https://www.example.com'
    })
    data = response.get_json()
    short_code = data['short_code']
    
    # Check initial stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['clicks'] == 0
    
    # Visit the URL a few times
    for _ in range(3):
        client.get(f'/{short_code}')
    
    # Check updated stats
    response = client.get(f'/api/stats/{short_code}')
    data = response.get_json()
    assert data['clicks'] == 3
    
    # Test stats for non-existent URL
    response = client.get('/api/stats/nonexistent')
    assert response.status_code == 404

def test_concurrent_clicks(client):
    """Test concurrent click tracking"""
    # Create a short URL
    response = client.post('/api/shorten', json={
        'url': 'https://www.example.com'
    })
    data = response.get_json()
    short_code = data['short_code']
    
    # Simulate concurrent access
    for _ in range(100):
        client.get(f'/{short_code}')
    
    # Verify click count
    response = client.get(f'/api/stats/{short_code}')
    data = response.get_json()
    assert data['clicks'] == 100