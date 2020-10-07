import pytest
import random
from datetime import datetime, timedelta
from service.url_shortener import UrlShortener
from mock import UrlStorageMock
from utils import get_random_string


storage_mock = UrlStorageMock()
url_shortener = UrlShortener(storage_mock)


@pytest.mark.asyncio
async def test_shorten():
    url = get_random_string()
    retention = timedelta(days=random.randrange(1, 1000))
    storage_mock.key = get_random_string()
    now = datetime.utcnow()

    key = await url_shortener.shorten(url, retention)

    assert storage_mock.key == key
    assert storage_mock.url == url

    delta = storage_mock.create_date - now
    if delta < timedelta(seconds=0):
        delta = -delta
    assert delta < timedelta(seconds=1)
    assert storage_mock.expiry_date == storage_mock.create_date + retention


@pytest.mark.asyncio
async def test_elongate():
    key = get_random_string()
    storage_mock.url = get_random_string()

    url = await url_shortener.elongate(key)

    assert url == storage_mock.url
    assert key == storage_mock.key


@pytest.mark.asyncio
async def test_init():
    storage_mock.init_called = False
    await url_shortener.init()
    assert storage_mock.init_called


@pytest.mark.asyncio
async def test_close():
    storage_mock.close_called = False
    await url_shortener.close()
    assert storage_mock.close_called
