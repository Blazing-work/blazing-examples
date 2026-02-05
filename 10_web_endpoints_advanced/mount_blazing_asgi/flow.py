import uvicorn
from fastapi import FastAPI
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
    api.mount('/blazing', blazing_asgi)

    uvicorn.run(api, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
