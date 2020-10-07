import logging
from datetime import timedelta
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse, PlainTextResponse
from .url_shortener import UrlShortener
from .storage import TarantoolUrlStorage, NotFoundError
from .config import *


app = FastAPI(title='URL Shortener Service', version='0.1')
logger = logging.getLogger(__name__)
srv = None


@app.on_event('startup')
async def startup():
    global srv
    srv = build_service()
    await srv.init()
    logger.info('Service initialized. Ready to accept connections.')


@app.get('/')
async def main():
    return 'POST / to store a long URL. Get /{key} to redirect.'


@app.get("/{key}")
async def redirect(key: str) -> RedirectResponse:
    try:
        url = await srv.elongate(key)
        return RedirectResponse(url, status_code=308)
    except NotFoundError:
        return Response(status_code=404)


@app.post('/')
async def shorten(request: Request, days: int = 365, rawkey: bool = False) -> Response:
    if int(request.headers.get('Content-Length', '0')) > URL_MAX_LENGTH:
        return Response(status_code=400, content='URL is too long')

    long_url = await request.body()
    key = await srv.shorten(long_url.decode('utf-8'), timedelta(days=days))

    if rawkey:
        result = key
    else:
        result = LINK_TEMPLATE.format(key)

    return PlainTextResponse(result)


@app.on_event("shutdown")
async def shutdown():
    await srv.close()


def build_service():
    url_storage = TarantoolUrlStorage(TARANTOOL_HOST, TARANTOOL_PORT)
    url_shortener = UrlShortener(url_storage)
    return url_shortener
