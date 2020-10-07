import asyncio
import pytest
import random
import config as config
from utils import get_long_url
from datetime import datetime, timedelta
from asynctnt import Connection
from service.storage import TarantoolUrlStorage, NotFoundError


@pytest.fixture(scope='module')
async def tnt_conn():
    conn = Connection(host=config.TARANTOOL_HOST, port=config.TARANTOOL_PORT)
    await conn.connect()
    yield conn
    await conn.disconnect()


@pytest.fixture(scope='module')
async def tnt_storage():
    storage = TarantoolUrlStorage(host=config.TARANTOOL_HOST, port=config.TARANTOOL_PORT)
    await storage.init()
    yield storage
    await storage.close()


@pytest.yield_fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_store_functionality(tnt_conn: Connection, tnt_storage: TarantoolUrlStorage):
    keys_count = await get_num_tuples(tnt_conn, 'keys')
    urls_count = await get_num_tuples(tnt_conn, 'urls')

    long_url = get_long_url(1000)
    key = await tnt_storage.store_url(long_url, datetime.now(), datetime.now() + timedelta(days=365))

    keys_count2 = await get_num_tuples(tnt_conn, 'keys')
    urls_count2 = await get_num_tuples(tnt_conn, 'urls')

    assert keys_count2 == keys_count - 1
    assert urls_count2 == urls_count + 1

    key_deleted = await tnt_conn.select('keys', (key,))
    url_stored = await tnt_conn.select('urls', (key,))

    assert len(key_deleted) == 0
    assert len(url_stored) == 1
    assert url_stored[0][1] == long_url


@pytest.mark.asyncio
async def test_store_api(tnt_storage: TarantoolUrlStorage):
    for _ in range(10):
        await check_store_and_get(tnt_storage)


@pytest.mark.asyncio
async def test_raises_on_missing_key(tnt_storage: TarantoolUrlStorage):
    with pytest.raises(NotFoundError):
        await tnt_storage.get_url('###')        # Impossible characters.


async def check_store_and_get(tnt_storage: TarantoolUrlStorage):
    long_url = get_long_url(length=random.randrange(200, 2000))
    key = await tnt_storage.store_url(long_url, datetime.now(), datetime.now() + timedelta(days=365))
    stored_url = await tnt_storage.get_url(key)
    assert long_url == stored_url


async def get_num_tuples(tnt: Connection, space_name: str):
    result = await tnt.call(f'box.space.{space_name}.index.primary:count', ())
    return result.body[0]


async def main():
    conn = Connection(host=config.TARANTOOL_HOST, port=config.TARANTOOL_PORT)
    await conn.connect()
    stor = TarantoolUrlStorage(host=config.TARANTOOL_HOST, port=config.TARANTOOL_PORT)
    await stor.init()
    await test_store_functionality(conn, stor)

if __name__ == '__main__':
    asyncio.run(main())
