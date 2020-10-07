from typing import Optional
from random import randrange
from datetime import datetime
from .storage import UrlStorage, NotFoundError
from asynctnt import Connection


class TarantoolUrlStorage(UrlStorage):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._conn = None   # type: Optional[Connection]

    async def init(self):
        self._conn = Connection(host=self.host, port=self.port)
        await self._conn.connect()

    async def get_url(self, key: str) -> str:
        tup = await self._conn.select('urls', (key,))
        if len(tup) == 0:
            raise NotFoundError(key)
        return tup[0][1]

    async def store_url(self, url: str, create_date: datetime, expiry_date: datetime) -> str:
        create_ts, expiry_ts = int(create_date.timestamp()), int(expiry_date.timestamp())
        key = await self._conn.call('store_url', (url, create_ts, expiry_ts, randrange(0, 2**31)))
        return key.body[0]

    async def close(self):
        await self._conn.disconnect()
