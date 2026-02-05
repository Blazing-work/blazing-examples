import uvicorn
from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()

    @app.endpoint(path='/square')
    @app.workflow
    async def square(value: int, services=None):
        return value * value

    await app.publish()
    fastapi_app = await create_asgi_app(app)
    uvicorn.run(fastapi_app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
