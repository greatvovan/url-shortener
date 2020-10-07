from datetime import datetime


class UrlStorage:
    async def init(self):
        pass

    async def get_url(self, key: str) -> str:
        raise NotImplementedError()

    async def store_url(self, url: str, create_date: datetime, expiry_date: datetime) -> str:
        raise NotImplementedError()

    async def close(self):
        pass


class NotFoundError(Exception):
    pass
