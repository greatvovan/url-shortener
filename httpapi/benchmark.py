import os
import time
import asyncio
import aiohttp


api_url = os.getenv('API_URL', 'http://localhost:8080')
shortenings_limit = 1000
shortenings_count = 0
redirects_count = 0
long_url = ('http://example.com/' + 'long-long/' * 20).encode('utf-8')    # ~ 220 characters
keys = []


async def main():
    global redirects_count
    await bechmarch_shoertenings()
    await bechmarch_redirects()
    redirects_count = 0
    await bechmarch_redirects()


async def bechmarch_shoertenings():
    start = time.monotonic()
    await multiply(run_shortenings, 50)
    end = time.monotonic()
    dur = end - start
    rate = shortenings_count / dur
    print(f'{shortenings_count} shortenings done in {round(dur, 1)} ({round(rate)}/s)')


async def bechmarch_redirects():
    start = time.monotonic()
    await multiply(run_redirects, 50)
    end = time.monotonic()
    dur = end - start
    rate = shortenings_count / dur
    print(f'{shortenings_count} redirects done in {round(dur, 1)} ({round(rate)}/s)')


async def multiply(coroutine, number: int):
    tasks = []
    for _ in range(number):
        tasks.append(asyncio.create_task(coroutine()))
    await asyncio.gather(*tasks)


async def run_shortenings():
    global shortenings_count, shortenings_limit
    url = api_url + '/?rawkey=true'
    while shortenings_count < shortenings_limit:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=long_url) as response:
                assert response.status == 200
                keys.append(await response.text())
        shortenings_count += 1


async def run_redirects():
    global keys, redirects_count
    klen = len(keys)
    url = api_url + '/{}'
    while True:
        async with aiohttp.ClientSession() as session:
            if redirects_count < klen:
                key = keys[redirects_count]
                redirects_count += 1
            else:
                break
            async with session.get(url.format(key), allow_redirects=False) as response:
                assert response.status == 308


if __name__ == '__main__':
    asyncio.run(main())
