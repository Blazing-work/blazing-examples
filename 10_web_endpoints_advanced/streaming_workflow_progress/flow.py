import asyncio
import uvicorn
from blazing import Blazing
from blazing.web import create_asgi_app
from blazing.endpoints.streaming import progress, log


async def main():
    app = Blazing()

    @app.endpoint(path='/process', response_mode='stream')
    @app.workflow
    async def process(items: list, services=None):
        total = len(items)
        await log('info', f'Starting {total} items')
        results = []
        for idx, item in enumerate(items, start=1):
            await asyncio.sleep(0.2)
            results.append(item * 2)
            await progress(step=idx, total=total, message=f'Processed {idx}/{total}')
        return {'results': results}

    await app.publish()
    fastapi_app = await create_asgi_app(app)
    uvicorn.run(fastapi_app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
