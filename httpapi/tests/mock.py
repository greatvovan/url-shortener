from datetime import datetime, timedelta
from service.storage import UrlStorage, NotFoundError


class UrlShortenerMock:
    def __init__(self):
        self.url = None
        self.retention = None
        self.key = None
        self.short = None
        self.long = None

    async def shorten(self, url: str, retention: timedelta) -> str:
        self.url = url
        self.retention = retention
        return self.short

    async def elongate(self, key: str) -> str:
        if key == '404':
            raise NotFoundError(key)
        self.key = key
        return self.long


class UrlStorageMock(UrlStorage):
    def __init__(self):
        self.key = None
        self.url = None
        self.create_date = None
        self.expiry_date = None
        self.init_called = None
        self.close_called = None

    async def get_url(self, key: str) -> str:
        self.key = key
        return self.url

    async def store_url(self, url: str, create_date: datetime, expiry_date: datetime) -> str:
        self.url = url
        self.create_date = create_date
        self.expiry_date = expiry_date
        return self.key

    async def init(self):
        self.init_called = True

    async def close(self):
        self.close_called = True
