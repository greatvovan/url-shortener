import logging
from datetime import datetime, timedelta
from aiocache import cached, Cache
from .storage import UrlStorage


logger = logging.getLogger(__name__)


class UrlShortener:
    def __init__(self, url_storage: UrlStorage):
        self.url_storage = url_storage

    async def init(self):
        await self.url_storage.init()
        logger.info(f'{type(self.url_storage).__name__} initialized.')

    async def shorten(self, url: str, retention: timedelta) -> str:
        now = datetime.utcnow()
        return await self.url_storage.store_url(url, now, now + retention)

    @cached(cache=Cache.MEMORY, ttl=20)
    async def elongate(self, key: str) -> str:
        return await self.url_storage.get_url(key)

    async def close(self):
        await self.url_storage.close()
