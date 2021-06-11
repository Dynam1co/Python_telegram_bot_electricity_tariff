import requests


def test_have_connection():
    resp = requests.get('https://google.es')
    
    assert resp.status_code == 200