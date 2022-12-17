import os
import sys
from aiofiles import open
from uuid import UUID, getnode
from sanic import Request, Sanic
from sanic.response import json
from sanic.exceptions import SanicException

app = Sanic('server')


class DefaultException(SanicException):
    message = 'error'
    quiet = True


@app.get('/ping')
async def ping(_: Request):
    return json({'ok': True})


@app.post('/upload')
async def upload(request: Request):
    try:
        j = request.json
        async with open(os.path.join(app.ctx.staticPath, f'{j["id"]}.json'),
                        'w') as f:
            await f.write(j['data'])
        return json({'ok': True})
    except Exception:
        raise DefaultException('upload err')


@app.post('/download/<id:uuid>')
async def download(_: Request, id: UUID):
    try:
        async with open(os.path.join(app.ctx.staticPath,
                                     f'{str(id)}.json')) as f:
            s = await f.read()
        return json({'ok': True, 'data': s})
    except Exception:
        raise DefaultException('download err')


@app.listener('before_server_start')
async def setToken(app: Sanic):
    tokenPath = os.path.join(sys.path[-1], 'token')
    app.ctx.staticPath = os.path.join(sys.path[-1], 'static')
    if (not os.path.isdir(app.ctx.staticPath)):
        os.mkdir(app.ctx.staticPath)
    if (not os.path.isdir(tokenPath)):
        os.mkdir(tokenPath)
    if (os.listdir(tokenPath) == []):
        app.ctx.token = str(getnode())
        f = await open(os.path.join(tokenPath, app.ctx.token), 'w')
        await f.close()
    else:
        app.ctx.token = os.listdir(tokenPath)[0]
    print('*' * 100)
    print(f'Your token is: {app.ctx.token}')
    print('*' * 100)


@app.middleware('request')
async def interceptor(request: Request):
    if (request.headers.get('token') != app.ctx.token):
        raise DefaultException('token err')


@app.exception(DefaultException)
async def defaultHandler(_: Request, exception: str):
    return json({'ok': False, 'err': str(exception)})
