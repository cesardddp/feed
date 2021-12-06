from feed import __version__
from feed.app import app


def test_version():
    assert __version__ == '0.1.0'

def test_index_route():
    response = app.test_client().get('/')
    
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Testing, Flask!'