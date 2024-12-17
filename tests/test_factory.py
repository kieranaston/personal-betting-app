from betting_app import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    # below line was added
    assert response.status_code == 200
    assert response.data == b'Hello, World!'