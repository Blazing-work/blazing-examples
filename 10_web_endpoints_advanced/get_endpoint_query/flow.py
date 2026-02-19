"""
GET Endpoint Query

Demonstrates creating a Blazing workflow exposed as an HTTP GET endpoint that accepts
query string parameters with a default value.  create_asgi_app() wraps the app and
uvicorn serves the resulting ASGI application.

Patterns shown:
  1. @app.endpoint(path='/greet', method='GET') to declare a GET-only route
  2. Workflow parameter with a default value (name: str = 'world') for optional query params
  3. create_asgi_app(app) + uvicorn.run() to serve the endpoint
"""
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
