import requests
import conf_management as Conf


def test_have_connection():
    resp = requests.get('https://google.es')
    
    assert resp.status_code == 200


def test_tariff_url_runs():
    resp = requests.get(Conf.get_source())

    assert resp.status_code == 200
