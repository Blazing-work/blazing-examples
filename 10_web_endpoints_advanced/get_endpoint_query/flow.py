import uvicorn
from blazing import Blazing
from blazing.web import create_asgi_app


async def main():
    app = Blazing()

    @app.endpoint(path='/greet', method='GET')
    @app.workflow
    async def greet(name: str = 'world', services=None):
        return {'message': f'Hello, {name}!'}

    await app.publish()
    fastapi_app = await create_asgi_app(app)
    uvicorn.run(fastapi_app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
