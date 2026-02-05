import uvicorn
from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()

    @app.endpoint(path='/add')
    @app.workflow
    async def add(x: int, y: int, services=None):
        return x + y

    await app.publish()
    asgi_app = await create_asgi_app(app)
    uvicorn.run(asgi_app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
