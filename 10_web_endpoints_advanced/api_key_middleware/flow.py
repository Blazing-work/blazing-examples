import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()

    @app.endpoint(path='/square', method='POST')
    @app.workflow
    async def square(value: int, services=None):
        return {'value': value * value}

    await app.publish()
    blazing_asgi = await create_asgi_app(app)

    api = FastAPI()
    api_key = os.getenv('BLAZING_API_KEY', 'dev-key')

    @api.middleware('http')
    async def api_key_middleware(request: Request, call_next):
        if request.url.path.startswith('/blazing'):
            if request.headers.get('x-api-key') != api_key:
                return JSONResponse({'detail': 'unauthorized'}, status_code=401)
        return await call_next(request)

    api.mount('/blazing', blazing_asgi)
    uvicorn.run(api, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
