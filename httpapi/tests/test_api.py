import random
from datetime import timedelta
from fastapi.testclient import TestClient
from service import api
from utils import get_long_url, get_random_string
from mock import UrlShortenerMock

srv_mock = UrlShortenerMock()
api.srv = srv_mock
client = TestClient(api.app)


def test_post_ok():
    srv_mock.short = get_random_string()
    long_url = get_long_url(random.randrange(200, 2000))
    retention_days = random.randrange(1, 1000)
    response = client.post(f'/?days={retention_days}', long_url.encode('utf-8'))
    assert srv_mock.url == long_url
    assert srv_mock.retention == timedelta(days=retention_days)
    assert response.status_code == 200
    assert response.text == api.LINK_TEMPLATE.format(srv_mock.short)


def test_post_too_long():
    srv_mock.short = get_random_string()
    response = client.post('/', get_long_url(2010).encode('utf-8'))
    assert response.status_code == 400


def test_redirect():
    srv_mock.long = get_random_string()
    key = get_random_string()
    response = client.get(f'/{key}', allow_redirects=False)
    assert srv_mock.long == response.headers.get('location')
    assert srv_mock.key == key
    assert response.status_code == 308


def test_not_found():
    response = client.get(f'/404', allow_redirects=False)
    assert response.status_code == 404
